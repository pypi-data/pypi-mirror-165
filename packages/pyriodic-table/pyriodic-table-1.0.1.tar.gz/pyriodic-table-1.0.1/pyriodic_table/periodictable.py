"""
This module holds the PeriodicTable class, which
unsurprisingly, has data on all 118 elements.

It also providides utility methods to seamlessly iterate through
the elements, and identify them with various data points.

There is also a function to save data of elements to a CSV file,
which can be useful for data analysis.
"""
import json
import csv
from typing import Callable, Union, Literal

from . import chemelements
from .exceptions import ElementDoesNotExist


# As of August 2022.
NUMBER_OF_ELEMENTS = 118

CSV_HEADERS = (
    "name", "symbol", "atomic_number", "atomic_mass",
    "electrons_per_shell", "state", "group", "period", "protons", "electrons",
    "melting_point_k", "melting_point_c", "melting_point_f",
    "boiling_point_k", "boiling_point_c", "boiling_point_f",
    "density", "natural", "has_stable_isotope", "discovery", "discovery_year")


def save_elements_data_to_csv(
    file_location: str,
    elements: Union[list[chemelements.Element], None] = None) -> None:
    """
    Saves data on the elements in a CSV file. A great way to analyse
    elements data (using libraries such as pandas and matplotlib).

    To only save data for certain elements, pass in a list of
    Element objects which represent the elements to be included.
    If 'elements' is passed in as None, all the elements will be
    included in the CSV.

    Warning: if the file already exists, it will be overwritten.
    """
    if elements is None:
        elements = PeriodicTable().elements

    elements_data = [element.asdict() for element in elements]
    
    with open(file_location, "w", encoding="utf8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
        writer.writeheader()
        writer.writerows(elements_data)
    

class PeriodicTable:
    """
    Holds the data for all 118 elements.
    """

    def __init__(self) -> None:
        """
        Creates a new instance of the periodic table.
        Gets all the elements of the periodic table in order
        by atomic number.
        """
        self._elements = []

        # Various element categories.

        self._natural_elements = []
        self._synthetic_elements = []
        self._elements_with_stable_isotope = []
        self._elements_without_stable_isotope = []

        self._alkali_metals = []
        self._alkaline_earth_metals = []
        self._lanthanides = []
        self._actinides = []
        self._halogens = []
        self._noble_gases = []

        for atomic_number in range(1, NUMBER_OF_ELEMENTS + 1):
            element = chemelements.Element(atomic_number)

            # Multiple ways of accessing an element as an attribute.
            setattr(self, element.name, element)
            setattr(self, element.symbol.lower(), element)
            setattr(self, element.symbol.title(), element)

            self._elements.append(element)

            # Adds elements into relevant categories.

            if element.group == 1 and element.atomic_number != 1:
                self._alkali_metals.append(element)
            elif element.group == 2:
                self._alkaline_earth_metals.append(element)
            elif element.group == 17:
                self._halogens.append(element)
            elif element.group == 18:
                self._noble_gases.append(element)

            if 57 <= element.atomic_number <= 71:
                self._lanthanides.append(element)
            elif 89 <= element.atomic_number <= 103:
                self._actinides.append(element)
            
            if element.natural:
                self._natural_elements.append(element)
            else:
                self._synthetic_elements.append(element)

            if element.has_stable_isotope:
                self._elements_with_stable_isotope.append(element)
            else:
                self._elements_without_stable_isotope.append(element)
    
    def get_element_by_name(self, name: str) -> chemelements.Element:
        """
        Finds an element by its name. Case-insensitive.
        """
        name = name.lower()

        for element in self:
            if element.name == name:
                return element

        raise ElementDoesNotExist(f"No such element with the name: {name}")
    
    def get_elements_by_name(
        self, function_check: Callable) -> list[chemelements.Element]:
        """
        Finds elements whose name evaluates to True
        when passed into a filter-like function.

        For example, given the following functions:

        lambda name: name.startswith("bo")

        [boron, bohrium] would be returned.

        lambda x: len(x) < 4

        [tin] would be returned.

        Note that the names of the elements are passed into the function.
        """
        return [element for element in self if function_check(element.name)]
    
    def get_element_by_atomic_number(
        self, atomic_number: int) -> chemelements.Element:
        """
        Finds an element by its atomic number (number of protons).
        """
        if 1 <= atomic_number <= NUMBER_OF_ELEMENTS:
            return self._elements[atomic_number - 1]
        
        raise ElementDoesNotExist(
            f"No such element with the atomic number: {atomic_number}")
    
    def get_elements_by_atomic_number(
        self, start: int, stop: int, step: int = 1
        ) -> list[chemelements.Element]:
        """
        Finds the elements which have an atomic number
        within a particular range.

        Works similarly to the range() function,
        so the 'stop' atomic number is not included.
        """
        if start < 1:
            # First atomic number is one, so no point in checking lower.
            start = 1

        if stop > NUMBER_OF_ELEMENTS + 1:
            # Last atomic number is 118, so no point in checking higher.
            stop = NUMBER_OF_ELEMENTS + 1

        return [
            self._elements[atomic_number - 1]
            for atomic_number in range(start, stop, step)]
    
    def get_element_by_symbol(self, symbol: str) -> chemelements.Element:
        """
        Finds an element by its symbol. Case-insensitive.
        """
        symbol = symbol.title()
        
        for element in self:
            if element.symbol == symbol:
                return element
        
        raise ElementDoesNotExist(f"No such element with the symbol: {symbol}")
    
    def get_elements_by_symbol(
        self, function_check: Callable) -> list[chemelements.Element]:
        """
        Finds the elements whose symbol evaluates to True
        when passed into a filter-like function.

        For example, given the following function:

        lambda symbol: len(symbol) == 1

        [hydrogen, boron, carbon, nitrogen, oxygen, fluorine,
        phosphorus,sulfur, potassium, vanadium, yttrium,
        iodine, tungsten, uranium] would be returned.

        Note that the symbols of the elements
        are passed into the function.
        """
        return [element for element in self if function_check(element.symbol)]
    
    def get_elements_by_state(
        self, state: Literal["solid", "liquid", "gas"]
    ) -> list[chemelements.Element]:
        """
        Finds the elements at a particular state at room temperature.

        State must either be 'solid', 'liquid' or 'gas',
        or their corresponding shorthands - 's', 'l', 'g'.

        Case-insensitive.
        """
        state = state.lower()

        # Accepts shorthand for each of the 3 states.
        state = {"s": "solid", "l": "liquid", "g": "gas"}.get(state, state)

        if state not in ("solid", "liquid", "gas"):
            raise ValueError(
                "State must either be 'solid', 'liquid' or 'gas'")

        return [
            element for element in self if element.state == state]
    
    def get_elements_by_group(
        self, group: Union[int, None]) -> list[chemelements.Element]:
        """
        Finds the elements in a particular Group (column).

        If 'group' is passed as None, all the elements not in
        a group are returned, such as some of the lanthanides.
        """
        return [element for element in self if element.group == group]

    def get_elements_by_period(
        self, period: int) -> list[chemelements.Element]:
        """
        Finds the elements in a particular Period (row).
        """
        return [element for element in self if element.period == period]
    
    def _get_elements_by_temperature(func: Callable) -> Callable:
        # Decorator function supporting both getting elements
        # by melting/boiling point.
        def wrap(
            self, minimum: Union[int, float], maximum: Union[int, float],
            unit: Literal["k", "c", "f"] = "k") -> list[chemelements.Element]:

            unit = unit.lower()

            if unit not in ("k", "c", "f"):
                raise ValueError("Unit must either be 'k', 'f' or 'c'")
            
            elements = []
            target_attribute = func()

            for element in self:
                # Gets required melting/boiling point in required unit.
                temperature = getattr(element, f"{target_attribute}_{unit}")

                if temperature and minimum <= temperature <= maximum:
                    elements.append(element)  

            return elements
        return wrap

    @_get_elements_by_temperature
    def get_elements_by_melting_point():
        """
        Finds the elements with a melting point in a given range.

        The temperature unit must either be 
        'k' (kelvin), 'c' (celsius), or 'f' (fahrenheit).

        Case-insensitive.
        """
        return "melting_point"
    
    @_get_elements_by_temperature
    def get_elements_by_boiling_point():
        """
        Finds the elements with a boiling point in a given range.

        The temperature unit must either be 
        'k' (kelvin), 'c' (celsius), or 'f' (fahrenheit).

        Case-insensitive.
        """
        return "boiling_point"
    
    def get_elements_by_density(
        self, minimum: Union[int, float], maximum: Union[int, float]
    ) -> list[chemelements.Element]:
        """
        Finds the elements with a density in a given range.
        Unit = g/cm^3
        """
        return [
            element for element in self
            if element.density is not None
            and minimum <= element.density <= maximum]
    
    def get_elements_by_discovery_year(
        self, minimum: int, maximum: int) -> list[chemelements.Element]:
        """
        Finds the elements discovered within a given time period.
        For BC years, use negative integers.

        For example, for 5000 BC, use -5000;
        but for 2022, simply use 2022
        """
        return [
            element for element in self
            if element.discovery_year is not None
            and minimum <= element.discovery_year <= maximum]
        
    @property
    def elements(self) -> list[chemelements.Element]:
        # All 118 elements.
        return self._elements
    
    @property
    def natural_elements(self) -> list[chemelements.Element]:
        # Elements which can be found in nature.
        return self._natural_elements
    
    @property
    def synthetic_elements(self) -> list[chemelements.Element]:
        # Man-made elements.
        return self._synthetic_elements
    
    @property
    def elements_with_stable_isotope(self) -> list[chemelements.Element]:
        # Non-radioactive elements.
        return self._elements_with_stable_isotope
    
    @property
    def elements_without_stable_isotope(self) -> list[chemelements.Element]:
        # Radioactive elements.
        return self._elements_without_stable_isotope
    
    @property
    def alkali_metals(self) -> list[chemelements.Element]:
        # Reactive, Group 1 metals.
        return self._alkali_metals
    
    @property
    def alkaline_earth_metals(self) -> list[chemelements.Element]:
        # Fairly reactive, Group 2 metals.
        return self._alkaline_earth_metals
    
    @property
    def lanthanides(self) -> list[chemelements.Element]:
        # Metals from atomic numbers 57 to 71.
        return self._lanthanides
    
    @property
    def actinides(self) -> list[chemelements.Element]:
        # Radioactive elements from atomic numbers 89 to 103.
        return self._actinides
    
    @property
    def halogens(self) -> list[chemelements.Element]:
        # Reactive Group 17 gases, except astatine and tennessine
        # which have unknown states.
        return self._halogens
    
    @property
    def noble_gases(self) -> list[chemelements.Element]:
        # Unreactive Group 18 gases (except oganesson - unknown state).
        return self._noble_gases

    def __len__(self) -> int:
        """
        Returns the number of elements in the periodic table (118).
        """
        return len(self._elements)
    
    def __iter__(self) -> None:
        """
        Iterates through the elements of the periodic table.
        """
        for element in self._elements:
            yield element
    
    def __reversed__(self) -> list[chemelements.Element]:
        """
        Returns the elements in reverse order.
        """
        return self._elements[::-1]
    
    def __repr__(self) -> str:
        """
        Displays basic data for each element as a string: 
        atomic number, name, symbol.
        """
        return " | ".join(
            ["{} {} ({})".format(
            element.atomic_number, element.name, element.symbol)
            for element in self]
        )
    
    def __contains__(self, info: str) -> bool:
        """
        Checks if a string matches the name or symbol
        of an existing element.

        Case-insensitive.
        """
        # For name check.
        lower = info.lower()
        # For symbol check.
        title = info.title()
    
        return any(
            lower == element.name or title == element.symbol
            for element in self)
    
    def _get_element_dicts(
        self, elements: list[chemelements.Element], dicts: dict
    ) -> list[dict]:
        # Gets corresponding dictionaries for a category of elements.
        return [dicts[element.name] for element in elements]

    def asdict(
        self, elements_to_dict: bool = True, elements_only: bool = False
        ) -> dict:
        """
        Returns a dictionary of the periodic table data; 
        also casting element data into dictionaries if specified.

        If 'elements_only' is passed as True, only a dictionary
        of the elements will be returned, not the different
        categories of elements alongside.
        """
        if elements_only:
            
            if not elements_to_dict:
                return {element.name: element for element in self}
            
            return {element.name: element.asdict() for element in self}


        if not elements_to_dict:
            return {
                "elements": {element.name: element for element in self},
                "natural_elements": self._natural_elements,
                "synthetic_elements": self._synthetic_elements,
                "elements_with_stable_isotope":
                self._elements_with_stable_isotope,
                "elements_without_stable_isotope":
                self.elements_without_stable_isotope,
                "alkali_metals": self._alkali_metals,
                "alkaline_earth_metals": self._alkaline_earth_metals,
                "lanthanides": self._lanthanides,
                "actinides": self._actinides,
                "halogens": self._halogens,
                "noble_gases": self._noble_gases
            }

        # Converts all elements' data into dicts once
        # for repeated usage below.
        element_dicts = {element.name: element.asdict() for element in self}

        return {
            "elements": element_dicts,

            "natural_elements": self._get_element_dicts(
                self._natural_elements, element_dicts),

            "synthetic_elements": self._get_element_dicts(
                self._synthetic_elements, element_dicts),

            "elements_with_stable_isotope": self._get_element_dicts(
                self._elements_with_stable_isotope, element_dicts),

            "elements_without_stable_isotope": self._get_element_dicts(
                self._elements_without_stable_isotope, element_dicts),

            "alkali_metals": self._get_element_dicts(
                self._alkali_metals, element_dicts),

            "alkaline_earth_metals": self._get_element_dicts(
                self._alkaline_earth_metals, element_dicts),

            "lanthanides": self._get_element_dicts(
                self._lanthanides, element_dicts),

            "actinides": self._get_element_dicts(
                self._actinides, element_dicts),

            "halogens": self._get_element_dicts(
                self._halogens, element_dicts),

            "noble_gases": self._get_element_dicts(
                self._noble_gases, element_dicts),
        }
    
    def to_json(
        self, elements_only: bool = False,
        indent: Union[int, None] = None, compact: bool = False) -> str:
        """
        Returns periodic table data as a JSON string
        (first converted into a dictionary).

        If 'elements_only' is passed as True, only JSON
        data for the elements will be returned, not the different
        categories of elements alongside.

        'compact' to True removes all unnecessary whitespace in
        the JSON string.
        """
        dict_data = self.asdict(elements_only=elements_only)

        if compact:
            return json.dumps(dict_data, indent=indent, separators=(",", ":"))

        return json.dumps(dict_data, indent=indent)