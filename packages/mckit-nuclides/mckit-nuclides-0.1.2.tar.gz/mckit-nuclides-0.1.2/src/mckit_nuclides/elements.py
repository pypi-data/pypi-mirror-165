"""Module `elements` provides access to information on chemical element level."""

from typing import Union

from dataclasses import InitVar, dataclass, field

import pandas as pd

from mckit_nuclides.utils.resource import path_resolver
from multipledispatch import dispatch


def _load_elements() -> pd.DataFrame:
    path = path_resolver("mckit_nuclides")("data/elements.csv")
    return pd.read_csv(path, index_col="symbol")


ELEMENTS_TABLE = _load_elements()


@dataclass
class Element:
    """Accessor to a chemical element information."""

    element: InitVar[Union[int, str]]
    atomic_number: int = field(init=False)

    def __post_init__(self, element: Union[int, str]) -> None:
        """Create an Element either from symbol or atomic number (Z).

        Args:
            element: symbol or atomic number for new Element.

        Raises:
            TypeError: if element type is not str or int.
        """
        if isinstance(element, str):
            self.atomic_number = ELEMENTS_TABLE.loc[element]["atomic_number"]
        elif isinstance(element, int):
            self.atomic_number = element
        else:
            raise TypeError(f"Illegal parameter symbol {element}")

    @property
    def z(self) -> int:
        """Atomic number and Z are synonymous.

        Returns:
            atomic number
        """
        return self.atomic_number

    @property
    def symbol(self) -> str:
        """Get periodical table symbol for the Element.

        Returns:
            Chemical symbol of the element.
        """
        return ELEMENTS_TABLE.index[self.atomic_number - 1]  # type: ignore[no-any-return]

    def __getattr__(self, item):
        """Use columns of ELEMENTS_TABLE as properties of the Element accessor.

        The `column` can be anything selecting a column or columns from ELEMENTS_TABLE.

        Args:
            item: column of ELEMENTS_TABLE

        Returns:
            content selected for this Element instance.
        """
        return ELEMENTS_TABLE.iloc[self.atomic_number - 1][item]


@dispatch(int)
def get_atomic_mass(atomic_number: int) -> float:
    """Get standard atomic mass for and Element by atomic number.

    Args:
        atomic_number: define Element by atomic number

    Returns:
        Average atomic mass of the Element with the atomic number.
    """
    return ELEMENTS_TABLE.iloc[atomic_number - 1]["atomic_mass"]


@dispatch(str)  # type: ignore[no-redef]
def get_atomic_mass(symbol: str) -> float:  # noqa: F811
    """Get standard atomic mass for and Element by symbol.

    Args:
        symbol: define Element by symbol.

    Returns:
        Average atomic mass of the Element with the atomic number.
    """
    return ELEMENTS_TABLE.loc[symbol]["atomic_mass"]
