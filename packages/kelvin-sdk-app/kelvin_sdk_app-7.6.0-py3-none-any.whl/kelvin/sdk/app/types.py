"""Types."""

from __future__ import annotations

import logging
import re
import sys
from enum import IntEnum
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    Iterator,
    List,
    Mapping,
    Optional,
    Type,
    TypeVar,
    Union,
)

from pydantic import BaseConfig, Field, ValidationError, parse_obj_as, root_validator, validator
from pydantic.generics import GenericModel
from pydantic.main import ErrorWrapper, ModelField
from typing_inspect import get_args

from kelvin.sdk.datatype import Model

if sys.version_info >= (3, 8):
    from typing import Literal
else:  # pragma: no cover
    from typing_extensions import Literal  # type: ignore


T = TypeVar("T")


class SchemaError(Model):
    is_valid: bool
    error: str


class BoolSchema(Model):
    title: Optional[str]
    data_type: Literal["raw.boolean"]

    def check(self, value: bool) -> SchemaError:
        valid: bool = True
        err: str = ""
        if not isinstance(value, bool) and value is not None:
            valid = False
            err = f"wrong typed value in parameter"
        return parse_obj_as(SchemaError, {"is_valid": valid, "error": err})


class StringSchema(Model):
    title: Optional[str]
    min_length: Optional[int] = Field(..., alias="minLength")
    max_length: Optional[int] = Field(..., alias="maxLength")
    pattern: Optional[str]
    data_type: Literal["raw.text"]

    def check(self, value: str) -> SchemaError:
        valid: bool = True
        err: str = ""
        try:
            if not isinstance(value, str) and value is not None:
                valid = False
                err = f"wrong typed value in parameter"
            if self.min_length and len(value) < self.min_length:
                valid = False
                err = f"length {len(value)} below minimum {self.min_length}"
            if self.max_length and len(value) > self.max_length:
                valid = False
                err = f"length {len(value)} above maximum {self.max_length}"
            if self.pattern and not re.match(self.pattern, value):
                valid = False
                err = f"{value} did not match {self.pattern}"
        except Exception as e:
            valid = False
            err = f"value {value} encountered validation error {e}"
        return parse_obj_as(SchemaError, {"is_valid": valid, "error": err})


class IntSchema(Model):
    title: Optional[str]
    minimum: Optional[int]
    maximum: Optional[int]
    data_type: Literal["raw.int32", "raw.uint32"]

    def check(self, value: int) -> SchemaError:
        valid: bool = True
        err: str = ""
        try:
            if not isinstance(value, int) and value is not None:
                valid = False
                err = f"wrong typed value in parameter"
            if value and self.minimum and value < self.minimum:
                valid = False
                err = f"value {value} below minimum {self.minimum}"
            if value and self.maximum and value > self.maximum:
                valid = False
                err = f"value {value} above maximum {self.maximum}"
        except Exception as e:
            valid = False
            err = f"value {value} encountered validation error {e}"
        return parse_obj_as(SchemaError, {"is_valid": valid, "error": err})


class FloatSchema(Model):
    title: Optional[str]
    minimum: Optional[Union[float, int]]
    maximum: Optional[Union[float, int]]
    data_type: Literal["raw.float64", "raw.float32"]

    def check(self, value: float) -> SchemaError:
        valid: bool = True
        err: str = ""
        try:
            if not isinstance(value, float) and not isinstance(value, int) and value is not None:
                valid = False
                err = f"wrong typed value in parameter"
            if value and self.minimum and value < self.minimum:
                valid = False
                err = f"value {value} below minimum {self.minimum}"
            if value and self.maximum and value > self.maximum:
                valid = False
                err = f"value {value} above maximum {self.maximum}"
        except Exception as e:
            valid = False
            err = f"value {value} encountered validation error {e}"
        return parse_obj_as(SchemaError, {"is_valid": valid, "error": err})


class Parameter(Model):
    value: Any
    name: str
    param_schema: Optional[Union[StringSchema, FloatSchema, IntSchema, BoolSchema]] = Field(
        discriminator="data_type"
    )
    data_type: str
    default: Optional[Mapping[str, Any]]

    def check(self) -> Optional[SchemaError]:
        if self.param_schema:
            return self.param_schema.check(self.value)
        return None

    @root_validator(pre=True)
    def prepare_validation(cls: Parameter, values: Dict[str, Any]) -> Any:
        if "schema" in values.keys():
            values["param_schema"] = {**values["schema"]}
            del values["schema"]

        if "value" not in values.keys():
            if values.get("default", None) is not None:
                values["value"] = values["default"]["value"]
        if values.get("param_schema", None):
            values["param_schema"]["data_type"] = values["data_type"]
        else:
            values["param_schema"] = {}
            values["param_schema"]["data_type"] = values["data_type"]

        return values


class TypedModel(GenericModel, Model, Generic[T]):
    """Typed model."""

    __slots__ = ("_type",)

    _type: T
    _TYPE_FIELD = "type"

    type: str = Field(
        ...,
        name="Type",
        description="Type.",
    )

    @root_validator(pre=True)
    def validate_type(cls: Type[TypedModel], values: Dict[str, Any]) -> Any:  # type: ignore
        """Validate type."""

        fields = cls.__fields__
        aliases = {x.alias: name for name, x in fields.items()}

        type_field = fields[cls._TYPE_FIELD]

        type_name = values.get(cls._TYPE_FIELD, type_field.default)
        if type_name is None:
            return values

        type_names = {*get_args(type_field.type_)}

        if type_name not in type_names:
            return values

        errors: List[ErrorWrapper] = []

        if type_name not in values:
            field_type = fields[aliases[type_name]].type_
            if any(x.required for x in field_type.__fields__.values()):
                errors += [ErrorWrapper(ValueError(f"{type_name!r} missing"), loc=(type_name,))]
            else:
                values[type_name] = {}

        for name in {*values} & type_names:
            if name == type_name:
                continue
            errors += [
                ErrorWrapper(ValueError(f"{name!r} doesn't match type {type_name!r}"), loc=(name,))
            ]

        if errors:
            raise ValidationError(errors, model=cls) from None  # type: ignore

        return values

    def __init__(self, **kwargs: Any) -> None:
        """Initialise typed-model."""

        super().__init__(**kwargs)

        aliases = {x.alias: name for name, x in self.__fields__.items()}

        object.__setattr__(self, "_type", self[aliases[self.type]])

    __iter__: Callable[[], Iterator[str]]  # type: ignore

    @property
    def _(self) -> T:
        """Selected type."""

        return self._type


class LogLevel(IntEnum):
    """Logging level."""

    DEBUG = logging.DEBUG
    WARNING = logging.WARNING
    INFO = logging.INFO
    ERROR = logging.ERROR
    TRACE = logging.ERROR

    @classmethod
    def __get_validators__(cls) -> Iterator[Callable[[Any, ModelField, BaseConfig], Any]]:
        """Get pydantic validators."""

        yield cls.validate

    @classmethod
    def validate(cls, value: Any, field: ModelField, config: BaseConfig) -> int:
        """Validate data."""

        if isinstance(value, int):
            return cls(value)
        elif not isinstance(value, str):
            raise TypeError(f"Invalid value {value!r}") from None

        try:
            return cls.__members__[value.upper()]
        except KeyError:
            raise ValueError(f"Invalid value {value!r}") from None
