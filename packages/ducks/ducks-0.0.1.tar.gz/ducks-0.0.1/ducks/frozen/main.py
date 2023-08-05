from bisect import bisect_left
from typing import Optional, Any, Dict, Union, Callable, Iterable, Set

import pickle
import numpy as np
import sortednp as snp

from filterbox.btree import range_expr_to_args
from filterbox.frozen.frozen_attr import FrozenAttrIndex
from filterbox.frozen.utils import snp_difference
from filterbox.utils import (
    make_empty_array,
    split_query,
    standardize_expr,
    validate_query,
    validate_and_standardize_operators,
)


class FrozenFilterBox:

    def __init__(self, objs: Iterable[Any], on: Iterable[Union[str, Callable]]):
        """Create a FrozenFilterBox containing the ``objs``, queryable by the ``on`` attributes.

        Args:
            objs: The objects that FrozenFilterBox will contain.

            on: The attributes that will be used for finding objects.
                Must contain at least one.

        It's OK if the objects in ``objs`` are missing some or all of the attributes in ``on``. They will still be
        stored, and can found with ``find()``.

        For the objects that do contain the attributes on ``on``, those attribute values must be hashable and sortable.
        Most Python objects are hashable. Implement the function ``__lt__(self, other)`` to make a class sortable.
        An attribute value of ``None`` is acceptable as well, even though None is not sortable.
        """
        if not on:
            raise ValueError("Need at least one attribute.")
        if isinstance(on, str):
            on = [on]

        self.obj_arr = np.empty(len(objs), dtype="O")
        self.dtype = "uint32" if len(objs) < 2 ** 32 else "uint64"
        for i, obj in enumerate(objs):
            self.obj_arr[i] = obj

        self._indexes = {}
        for attr in on:
            self._indexes[attr] = FrozenAttrIndex(attr, self.obj_arr, self.dtype)

        # only used during contains() checks
        self.sorted_obj_ids = np.sort([id(obj) for obj in self.obj_arr])

    def _find(
        self,
        match: Optional[Dict[Union[str, Callable], Any]] = None,
        exclude: Optional[Dict[Union[str, Callable], Any]] = None,
    ) -> np.ndarray:
        """Find objects in the FrozenFilterBox that satisfy the match and exclude constraints.

        Args:
            match: Dict of ``{attribute: expression}`` defining the subset of objects that match.
                If ``None``, all objects will match.

                Each attribute is a string or Callable. Must be one of the attributes specified in the constructor.

                The expression can be any of the following:
                 - A dict of ``{operator: value}``, such as ``{'==': 1}`` ``{'>': 5}``, or ``{'in': [1, 2, 3]}``.
                 - A single value, which is a shorthand for `{'==': value}`.
                 - A list of values, which is a shorthand for ``{'in': [list_of_values]}``.
                 - ``ducks.ANY``, which matches all objects having the attribute.

                 Valid operators are '==' 'in', '<', '<=', '>', '>='.
                 The aliases 'eq' 'lt', 'le', 'lte', 'gt', 'ge', and 'gte' work too.
                 To match a None value, use ``{'==': None}``. There is no separate operator for None values.

            exclude: Dict of ``{attribute: expression}`` defining the subset of objects that do not match.
                If ``None``, no objects will be excluded.

                Each attribute is a string or Callable. Must be one of the attributes specified in the constructor.
                Valid expressions are the same as in ``match``.

        Returns:
            Numpy array of objects matching the constraints. Array will be in the same order as the original objects.
        """
        # validate input and convert expressions to dict
        validate_query(self._indexes, match, exclude)
        for arg in [match, exclude]:
            if arg:
                for key in arg:
                    arg[key] = standardize_expr(arg[key])

        # perform 'match' query
        if match:
            hit_arrays = []
            for attr, expr in match.items():
                hit_array = self._match_attr_expr(attr, expr)
                if len(hit_array) == 0:
                    # this attr had no matches, therefore the intersection will be empty. We can stop here.
                    return make_empty_array("O")
                hit_arrays.append(hit_array)

            # intersect all the hit_arrays, starting with the smallest
            for i, hit_array in enumerate(sorted(hit_arrays, key=len)):
                if i == 0:
                    hits = hit_array
                else:
                    hits = snp.intersect(hits, hit_array)
        else:
            hits = np.arange(len(self.obj_arr), dtype=self.dtype)

        # perform 'exclude' query
        if exclude:
            exc_arrays = []
            for attr, expr in exclude.items():
                exc_arrays.append(self._match_attr_expr(attr, expr))

            # subtract each of the exc_arrays, starting with the largest
            for exc_array in sorted(exc_arrays, key=len, reverse=True):
                hits = snp_difference(hits, exc_array)
                if len(hits) == 0:
                    break

        return self.obj_arr[hits]

    def _match_attr_expr(self, attr: Union[str, Callable], expr: dict) -> np.ndarray:
        """Look at an attr, handle its expr appropriately"""
        validate_and_standardize_operators(expr)
        matches = None
        # handle 'in' and '=='
        eq_expr = {op: val for op, val in expr.items() if op in ["==", "in"]}
        for op, val in eq_expr.items():
            if op == "==":
                op_matches = self._indexes[attr].get(val)
            elif op == "in":
                op_matches = self._match_any_value_in(attr, expr["in"])
            matches = (
                op_matches if matches is None else snp.intersect(op_matches, matches)
            )

        # handle range query
        range_expr = {
            op: val for op, val in expr.items() if op in ["<", ">", "<=", ">="]
        }
        if range_expr:
            min_key, max_key, include_min, include_max = range_expr_to_args(range_expr)
            range_matches = self._indexes[attr].get_ids_by_range(
                min_key, max_key, include_min, include_max
            )
            matches = (
                range_matches
                if matches is None
                else snp.intersect(range_matches, matches)
            )
        return matches

    def get_values(self, attr: Union[str, Callable]) -> Set:
        """Get the set of unique values we have for the given attribute.

        Args:
            attr: The attribute to get values for.

        Returns:
            Set of all unique values for this attribute.
        """
        return self._indexes[attr].get_values()

    def _match_any_value_in(
        self, attr: Union[str, Callable], values: Iterable[Any]
    ) -> np.ndarray:
        """"Get the union of object ID matches for the values."""
        matches = [self._indexes[attr].get(v) for v in values]
        if matches:
            return np.sort(np.concatenate(matches))
        else:
            return make_empty_array(self.dtype)

    def __contains__(self, obj):
        obj_id = id(obj)
        idx = bisect_left(self.sorted_obj_ids, obj_id)
        if idx < 0 or idx >= len(self.sorted_obj_ids):
            return False
        return self.sorted_obj_ids[idx] == obj_id

    def __iter__(self):
        return iter(self.obj_arr)

    def __len__(self):
        return len(self.obj_arr)

    def __getitem__(self, query: Dict) -> np.ndarray:
        """Find objects in the FrozenFilterBox that satisfy the constraints.

                Args:
                    query: Dict of ``{attribute: expression}`` defining the subset of objects that match.
                        If ``{}``, all objects will match.

                        Each attribute is a string or Callable. Must be one of the attributes specified in the constructor.

                        The expression can be any of the following:
                         - A dict of ``{operator: value}``, such as ``{'==': 1}`` ``{'>': 5}``, or ``{'in': [1, 2, 3]}``.
                         - A single value, which is a shorthand for `{'==': value}`.
                         - A list of values, which is a shorthand for ``{'in': [list_of_values]}``.

                         The expression ``{'==': ducks.ANY}`` will match all objects having the attribute.
                         The expression ``{'!=': ducks.ANY}`` will match all objects without the attribute.

                         Valid operators are '==', '!=', 'in', 'not in', '<', '<=', '>', '>='.
                         The aliases 'eq', 'ne', 'lt', 'le', 'lte', 'gt', 'ge', and 'gte' work too.
                         To match a None value, use ``{'==': None}``. There is no separate operator for None values.

                Returns:
                    Numpy array of objects matching the constraints. Array will be in the same order as the original objects.
        """
        if not isinstance(query, dict):
            raise TypeError(f"Got {type(query)}; expected a dict.")
        std_query = dict()
        for attr, expr in query.items():
            std_query[attr] = standardize_expr(expr)
        match_query, exclude_query = split_query(std_query)
        return self._find(match_query, exclude_query)


def save(box: FrozenFilterBox, filepath: str):
    """Saves this object to a pickle file."""
    with open(filepath, "wb") as fh:
        pickle.dump(box, fh)


def load(box: FrozenFilterBox):
    """Creates a FrozenFilterBox from the pickle file contents."""
    # If this was created by one Python process and loaded by another, the object IDs will no longer
    # correspond to the objects. Re-create the object ID array with the correct IDs.
    box.sorted_obj_ids = np.sort([id(obj) for obj in box.obj_arr])
