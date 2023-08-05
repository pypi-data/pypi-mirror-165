#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------------
import re
import warnings
from datetime import date
from datetime import datetime
from typing import Any
from typing import Dict
from typing import Optional
from typing import Tuple
from uuid import UUID
from uuid import uuid4

from pydantic import Field
from pydantic import root_validator
from pydantic import validator
from ramodels.base import RABase
from ramodels.base import tz_isodate

try:
    import zoneinfo
except ImportError:  # pragma: no cover
    from backports import zoneinfo  # type: ignore

UTC = zoneinfo.ZoneInfo("UTC")

# Type aliases
DictStrAny = Dict[str, Any]

# --------------------------------------------------------------------------------------
# MOBase
# --------------------------------------------------------------------------------------


class UUIDBase(RABase):
    """Base model with autogenerated UUID."""

    def __new__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls is UUIDBase:
            raise TypeError("UUIDBase may not be instantiated")
        return super().__new__(cls)

    uuid: UUID = Field(
        None, description="UUID to be created. Will be autogenerated if not specified."
    )

    # Autogenerate UUID if necessary
    @validator("uuid", pre=True, always=True)
    def set_uuid(cls, _uuid: Optional[UUID]) -> UUID:
        return _uuid or uuid4()


class MOBase(UUIDBase):
    """Base model for MO data models."""

    def __new__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls is MOBase:
            raise TypeError("MOBase may not be instantiated")
        return super().__new__(cls)

    user_key: str = Field(
        None, description="Short, unique key. Defaults to object UUID."
    )

    @validator("user_key", pre=True, always=True)
    def set_user_key(cls, user_key: Optional[Any], values: DictStrAny) -> str:
        return user_key or str(values["uuid"])

    @root_validator
    def validate_type(cls, values: DictStrAny) -> DictStrAny:
        if "type_" in cls.__fields__ and "type_" in values:
            field = cls.__fields__["type_"]

            if not field.required and values["type_"] != field.default:
                raise ValueError(f"type may only be its default: '{field.default}'")
        return values


# --------------------------------------------------------------------------------------
# Shared models
# --------------------------------------------------------------------------------------


class MORef(RABase):
    """Reference base.

    Yes, this is a weird layer of indirection. It is simply modelled
    after how MO's API for writing is and not out of necessity.
    """

    uuid: UUID = Field(description="The UUID of the reference.")


class AddressType(MORef):
    """Address type reference."""


class EmployeeRef(MORef):
    """Employee reference."""


class EngagementAssociationType(MORef):
    """Engagement Association type reference."""


class EngagementRef(MORef):
    """Engagement reference."""


class EngagementType(MORef):
    """Engagement type reference."""


class AssociationType(MORef):
    """Association type reference."""


class DynamicClasses(MORef):
    """Attached classes reference."""


class ITSystemRef(MORef):
    """IT System reference."""


class ITUserRef(MORef):
    """IT User reference."""


class JobFunction(MORef):
    """Job function reference."""


class LeaveType(MORef):
    """Leave type reference."""


class LeaveRef(MORef):
    """Leave reference"""


class KLENumberRef(MORef):
    """KLE number reference.

    The klasse for the number facet have up to three levels
    - main group
    - group
    - topic
    as defined in http://www.kle-online.dk/emneplan/
    """


class KLEAspectRef(MORef):
    """KLE aspect reference.

    The klasse for the aspect facet can be one of three predefined strings
    - "Executive"
    - "Responsible"
    - "Insight"
    """


class ManagerLevel(MORef):
    """Manager level reference."""


class ManagerType(MORef):
    """Manager type reference."""


class OrganisationRef(MORef):
    """Organisation reference."""


class OrgUnitHierarchy(MORef):
    """Organisation unit hierarchy reference."""


class OrgUnitLevel(MORef):
    """Organisation unit level reference."""


class OrgUnitRef(MORef):
    """Organisation unit reference."""


class OrgUnitType(MORef):
    """Organisation unit type."""


class ParentRef(MORef):
    """Parent reference."""


class PersonRef(MORef):
    """Person reference."""


class Primary(MORef):
    """Primary type reference."""


class Responsibility(MORef):
    """Responsibility type reference."""


class RoleType(MORef):
    """Role type reference."""


class TimePlanning(MORef):
    """Time planning reference"""


class OpenValidity(RABase):
    """Validity of a MO object with optional `from_date`."""

    from_date: Optional[datetime] = Field(
        alias="from", description="Start date of the validity."
    )
    to_date: Optional[datetime] = Field(
        alias="to", description="End date of the validity, if applicable."
    )

    @validator("from_date", pre=True, always=True)
    def parse_from_date(cls, from_date: Optional[Any]) -> Optional[datetime]:
        return tz_isodate(from_date) if from_date is not None else None

    @validator("to_date", pre=True, always=True)
    def parse_to_date(cls, to_date: Optional[Any]) -> Optional[datetime]:
        return tz_isodate(to_date) if to_date is not None else None

    @root_validator
    def check_from_leq_to(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        # Note: the values of from_date & to_date are not changed here
        # just leq compared.
        _from_dt, _to_dt = values.get("from_date"), values.get("to_date")
        cmp_from_dt = _from_dt if _from_dt else datetime.min.replace(tzinfo=UTC)
        cmp_to_dt = _to_dt if _to_dt else datetime.max.replace(tzinfo=UTC)
        if all([cmp_from_dt, cmp_to_dt]) and not (cmp_from_dt <= cmp_to_dt):
            raise ValueError(
                f"from_date {cmp_from_dt} must be less than "
                f"or equal to to_date {cmp_to_dt}"
            )
        return values


class Validity(OpenValidity):
    """Validity of a MO object with required `from_date`."""

    from_date: datetime = Field(alias="from", description="Start date of the validity.")


class TerminateValidity(OpenValidity):
    to_date: datetime = Field(
        alias="to",
        description="When the validity should end " "- required when terminating",
    )


class Visibility(MORef):
    """Visbility type reference."""

    pass


# --------------------------------------------------------------------------------------
# Auxiliary validator functions
# --------------------------------------------------------------------------------------


def deprecation(message: str) -> None:
    """Raise a deprecation warning with `message` at stacklevel 2."""
    warnings.warn(message, DeprecationWarning, stacklevel=2)


def split_name(name: str) -> Tuple[str, str]:
    """Split a name into first and last name.

    Args:
        name: The name to split.

    Returns:
        A 2-tuple containing first and last name.
    """
    split = name.rsplit(" ", maxsplit=1)
    if len(split) == 1:
        split.append("")
    givenname, surname = split
    return givenname, surname


def validate_names(
    values: DictStrAny, name_key: str, givenname_key: str, surname_key: str
) -> DictStrAny:
    """Validate a name value from a dictionary. Used in the Employee model validator.

    Args:
        values: Value dict to validate.
        name_key: The key for the name value.
        givenname_key: The key for the first name value.
        surname_key: The key for the last name value.

    Raises:
        ValueError: If both `name_key` and any of the `givenname_key`, `surname_key`
            are given, as they are mutually exclusive.

    Returns:
        The value dict, untouched.
    """
    if values.get(name_key) is not None:
        # Both name and given/surname are given erroneously
        if values.get(givenname_key) is not None or values.get(surname_key) is not None:
            raise ValueError(
                f"{name_key} and {givenname_key}/{surname_key} are mutually exclusive"
            )
        # If only name is given, raise a deprecation warning and generate given/surname
        else:
            deprecation(
                f"{name_key} will be deprecated in a future version. "
                f"Prefer {givenname_key}/{surname_key} where possible"
            )
            values[givenname_key], values[surname_key] = split_name(values[name_key])

    return values


def validate_cpr(cpr_no: Optional[str]) -> Optional[str]:
    """Validate a Danish CPR number.
    Note that this function does not check whether a CPR number *exists*,
    just that it is valid according to the spec.

    Args:
        cpr_no (Optional[str]): CPR to check.

    Raises:
        ValueError: If the given CPR number does not conform to the spec.

    Returns:
        Optional[str]: The validated CPR number.
    """
    if cpr_no is None:
        return None

    if not re.match(r"^\d{10}$", cpr_no):
        raise ValueError("CPR string is invalid.")

    # We only obtain the most significant digit of the code part, since it's
    # what we need for century calculations,
    # cf. https://da.wikipedia.org/wiki/CPR-nummer
    day, month = map(int, (cpr_no[0:2], cpr_no[2:4]))
    year, code_msd = map(int, (cpr_no[4:6], cpr_no[6]))

    # Allows "fictitious" birthdates
    # https://modst.dk/media/17386/fiktive-cpr-numre.pdf
    if day >= 60:
        day -= 60

    # TODO: let's do pattern matching in 3.10:
    # https://www.python.org/dev/peps/pep-0622/ <3
    century: int = 0
    if code_msd < 4:
        century = 1900
    elif code_msd in {4, 9}:
        if 0 <= year <= 36:
            century = 2000
        else:
            century = 1900
    elif 5 <= code_msd <= 8:
        if 0 <= year <= 57:
            century = 2000
        else:
            century = 1800

    try:
        date(year=century + year, month=month, day=day)
    except Exception:
        raise ValueError("CPR number is invalid.")
    return cpr_no
