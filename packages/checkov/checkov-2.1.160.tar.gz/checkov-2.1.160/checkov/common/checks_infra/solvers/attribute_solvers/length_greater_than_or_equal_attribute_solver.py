from typing import Optional, Any, Dict
from collections.abc import Sized
from checkov.common.util.type_forcers import force_int
from .length_less_than_attribute_solver import LengthLessThanAttributeSolver
from checkov.common.graph.checks_infra.enums import Operators


class LengthGreaterThanOrEqualAttributeSolver(LengthLessThanAttributeSolver):
    operator = Operators.LENGTH_GREATER_THAN_OR_EQUAL  # noqa: CCE003  # a static attribute

    def _get_operation(self, vertex: Dict[str, Any], attribute: Optional[str]) -> bool:  # type:ignore[override]
        attr = vertex.get(attribute)  # type:ignore[arg-type]  # due to attribute can be None
        if attr is None:
            return False

        # if this value contains an underendered variable, then we cannot evaluate the check,
        # so return True (since we cannot return UNKNOWN)
        if self._is_variable_dependant(attr, vertex['source_']):
            return True

        value_int = force_int(self.value)

        if value_int is None:
            return False
        if isinstance(attr, Sized):
            return len(attr) >= value_int

        return False
