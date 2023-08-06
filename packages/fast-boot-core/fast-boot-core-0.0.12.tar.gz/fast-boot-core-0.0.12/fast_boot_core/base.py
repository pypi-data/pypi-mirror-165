import inspect
from typing import (
    Any, Callable, Dict, List, Type, TypeVar, Union, get_type_hints
)

from fast_boot.schemas import Schema
from fastapi import Depends
from pydantic.error_wrappers import ErrorWrapper, flatten_errors
from pydantic.errors import PydanticErrorMixin
from pydantic.typing import is_classvar
from sqlalchemy.orm import Session
from starlette.requests import Request

from .beans import Beans
from .exception import LOSError

T = TypeVar("T")
CBV_CLASS_KEY = "__cbv_class__"


def errors(self) -> List[Dict[str, Any]]:
    if self._error_cache is None:
        try:
            config = self.model.__config__  # type: ignore
        except AttributeError:
            config = self.model.__pydantic_model__.__config__  # type: ignore
        self._error_cache = list(flatten_errors(self.raw_errors, config))
    return self._error_cache


def append_error(self, loc: List[Union[str, float]], code: str = None, msg_template: str = None, error: PydanticErrorMixin = None, **kwargs) -> None:
    """
    mặc định sử dụng LOSError phải có code vs msg_template tương ứng
    :param loc: vị trí của field lỗi
    :param code: error_code
    :param msg_template:
    :param error: sử dụng error có sẵn trong package errors của pydantic
    :return:
    """
    # assert hasattr(message, error.), "Không tìm thấy msg error"
    assert (code or error), "Required code or error"
    if code:
        if msg_template is None:
            msg_template = Beans.MSG_TEMPLATE.get(code)
        assert msg_template, f"Required msg_template for code: {code}"
        self.raw_errors.append(ErrorWrapper(exc=LOSError(code=code, msg_template=str(msg_template), **kwargs), loc=tuple(loc)))
    elif error:
        self.raw_errors.append(ErrorWrapper(exc=error, loc=tuple(loc)))


def has_error(self) -> bool:
    return bool(self.raw_errors)


def count_errors(self) -> int:
    return len(self.raw_errors)


def service(cls: Type[T]) -> Type[T]:
    """
    def errors(self) -> List[Dict[str, Any]]:

    def append_error(self, loc: List[Union[str, float]], code: str = None, msg_template: str = None, error: PydanticErrorMixin = None, **kwargs) -> None:

    def has_error(self) -> bool:

    def count_errors(self) -> int:
    """
    _init_base(cls)
    return cls


def repos(cls):
    orig_bases = cls.__orig_bases__
    generic_type = orig_bases[0]
    type_, id_ = getattr(generic_type, "__args__")
    setattr(cls, "type_", type_)
    setattr(cls, "id_", id_)
    _init_base(cls)
    return cls


def default_dependencies():
    return {
        "session": {"hint": Session, "default": Depends(Beans.SESSION_DEPENDENCY)},
        "request": {"hint": Request, "default": None}
    }


def _init_base(cls: Type[Any]) -> None:
    """
    Idempotently modifies the provided `cls`, performing the following modifications:
    * The `__init__` function is updated to set any class-annotated dependencies as instance attributes
    * The `__signature__` attribute is updated to indicate to FastAPI what arguments should be passed to the initializer
    """
    if getattr(cls, CBV_CLASS_KEY, False):  # pragma: no cover
        return  # Already initialized
    old_init: Callable[..., Any] = cls.__init__
    old_signature = inspect.signature(old_init)
    old_parameters = list(old_signature.parameters.values())[1:]  # drop `self` parameter
    new_parameters = [
        x for x in old_parameters if x.kind not in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD)
    ]
    dependency_names: List[str] = []
    for name, hint in get_type_hints(cls).items():
        if is_classvar(hint):
            continue
        parameter_kwargs = {"default": getattr(cls, name, Ellipsis)}
        dependency_names.append(name)
        new_parameters.append(
            inspect.Parameter(name=name, kind=inspect.Parameter.KEYWORD_ONLY, annotation=hint, **parameter_kwargs)
        )
    for name, value in default_dependencies().items():
        dependency_names.append(name)
        new_parameters.append(
            inspect.Parameter(name=name, kind=inspect.Parameter.KEYWORD_ONLY, annotation=value["hint"], default=value["default"])
        )
    new_signature = old_signature.replace(parameters=new_parameters)

    def new_init(self: Any, *args: Any, **kwargs: Any) -> None:
        setattr(self, "raw_errors", [])
        setattr(self, "model", Schema)
        setattr(self, "_error_cache", None)
        for dep_name in dependency_names:
            dep_value = kwargs.pop(dep_name)
            setattr(self, dep_name, dep_value)
        old_init(self, *args, **kwargs)

    setattr(cls, "__signature__", new_signature)
    setattr(cls, "__init__", new_init)
    setattr(cls, "errors", errors)
    setattr(cls, "append_error", append_error)
    setattr(cls, "has_error", has_error)
    setattr(cls, "count_errors", count_errors)
    setattr(cls, CBV_CLASS_KEY, True)
