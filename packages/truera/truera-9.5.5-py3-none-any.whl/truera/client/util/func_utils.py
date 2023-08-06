from abc import ABCMeta
from abc import abstractmethod
import functools
import inspect
from types import FunctionType
from typing import Any, Callable, Dict, List, TypeVar
import warnings

C = TypeVar("C")
U = TypeVar("U")
V = TypeVar("V")


class Deprecate:

    @staticmethod
    def module(name, message, dep_version, remove_version):
        """
        Immediately issue a warning that the module with the given `name` is
        deprecated.
        """

        warnings.warn(
            message=
            f"Module {name} is deprecated since version {dep_version} and will be removed in {remove_version}. {message}",
            category=DeprecationWarning
        )

    @staticmethod
    def method(message, dep_version, remove_version):
        """
        Mark the given method as being deprecated since `dep_version` and that it
        will be removed in version `remove_version`.
        """

        def wrapper(thing):
            if isinstance(thing, classmethod):
                func = thing.__func__
                extra_decorator = classmethod
            elif isinstance(thing, Callable):
                func = thing
                extra_decorator = lambda x: x
            else:
                raise RuntimeError(
                    f"Do not know how to wrap object of type {type(thing)}."
                )

            dep_message = f"Method {func.__name__} is deprecated since version {dep_version} and will be removed in {remove_version}. {message}"

            @functools.wraps(func)
            @extra_decorator
            def f(*args, **kwargs):
                warnings.warn(message=dep_message, category=DeprecationWarning)
                return func(*args, **kwargs)

            # Also add depreciation message to the doc string.
            f.__doc__ = dep_message + (f.__doc__ or "")
            return f

        return wrapper


class WrapperMeta(ABCMeta):
    """
    ABC to help enforce some rules regarding wrappers. 
    
    - Attribute protection: classes that mark attributes with "__protected__"
      cannot have those attributes overridden by child classes.
    
    - Initialization requirements: methods marked with "__require__" need to be
      executed during an objects initialization. Mark parent initializers to
      require children to call the parent initializer.

    - Abstract method deprecation. Allows for wrappers to accept old methods in
      place of new renamed ones while issuing deprecation warnings.
    """

    @staticmethod
    def deprecates(oldfunc_name: str, dep_version: str, remove_version: str):
        """
        Mark an abstract method as deprecating the given method (name). During
        class construction, the marked field will be filled in using the oldfunc
        method if it exists, issuing a deprecation warning.
        """

        def wrapper(absfunc):
            # TODO: figure out a working way to detect whether absfunc is an
            # abstractmethod.

            #  assert isinstance(absfunc, abstractmethod), "This deprecation wrapper is meant for abstract methods only."

            absfunc.__func__.__deprecates__ = (
                oldfunc_name, dep_version, remove_version
            )

            return absfunc

        return wrapper

    @staticmethod
    def protect(obj) -> Any:
        """Decorator to mark the given object as protected."""

        if isinstance(obj, Callable) or isinstance(obj, classmethod):
            obj.__protected__ = True

        elif isinstance(obj, property):
            if obj.fset is not None:
                obj.fset.__protected__ = True
            if obj.fget is not None:
                obj.fget.__protected__ = True
            if obj.fdel is not None:
                obj.fdel.__protected__ = True

        else:
            raise ValueError(f"Unhandled object type to protect: {type(obj)}")

        return obj

    def __check_protect(obj, attr, base_name, class_name):
        """
        Check if the given object is marked protected and if so, throw an error
        with the other args as debugging info.
        """

        if hasattr(obj, "__protected__") and getattr(obj, "__protected__"):
            raise AttributeError(
                f"Attribute {attr} of {base_name} should not be overriden in child class {class_name}."
            )

    def __check_deprecates(base_val, attr, attrs):
        """
        Check if an abstractmethod in `base_val` named `attr` is defined in
        `attrs` by its old name.
        """

        if hasattr(base_val.__func__, "__deprecates__"):

            oldmethod_name, dep_version, remove_version = getattr(
                base_val.__func__, "__deprecates__"
            )

            if oldmethod_name in attrs:
                # Issue warning.
                warnings.warn(
                    f"Method {oldmethod_name} is deprecated since {dep_version} and will be removed in {remove_version}. "
                    f"The method was renamed to {base_val.__func__.__name__}.",
                    DeprecationWarning
                )

                # Replace the abstract method with concrete implementation from `oldmethod_name`.
                attrs[attr] = attrs[oldmethod_name]
            else:
                # Leave abstract, will cause abstractmethod undefined in parent __new__ .
                pass
        else:
            # This should cause abstracmethod needs to be defined in the parent __new__ .
            pass

    @staticmethod
    def require(func) -> Any:
        """
        Decorator to mark the given method as required during initialization and
        must be overriden.
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            wrapper.__require__ = False
            return func(*args, **kwargs)

        wrapper.__require__ = True

        return wrapper

    @staticmethod
    def require_if_extended(func) -> Any:
        """
        Decorator to mark the given method as required during initialization but
        does not need to be overriden.
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            wrapper.__require__ = False
            return func(*args, **kwargs)

        wrapper.__require__ = True
        wrapper.__extend_optional__ = True

        return wrapper

    def __init__(cls, name, bases, attrs):
        """
        When instantiating an object, do some checks and wraps some methods
        depending on what the object is.
        """

        if len(bases) == 0:
            # If instantiating metaclass itself, do nothing.
            super().__init__(name, bases, attrs)
            return

        # Otherwise the instantiated object has some parent class base.
        # TODO: What if they have more than one?

        if not "__init__" in attrs:
            # If the child class has no initializer of its own, check if we wanted it to.

            if hasattr(bases[0], "__init__") and hasattr(
                bases[0], "__require__"
            ) and not hasattr(bases[0].__init__, "__extend_optional__"):
                # If your parent has an init with is required, you need to have an init (and call the parent).
                raise AttributeError(
                    f"Wrapper class {name} needs to define __init__."
                )
            else:
                # If we did not want child class to have __init__ of its own, nothing else to do.

                super().__init__(name, bases, attrs)
                return

        init = attrs['__init__']

        if hasattr(init, "__require__"):
            # If the child we are looking at is one annotated with require, we
            # are in one of the base wrapper classes. No more enforcements for
            # those.

            super().__init__(name, bases, attrs)
            return

        # Otherwise we have a child class that has an init and extended one of the wrapper classes.
        # We wraper the init method as follows:

        @functools.wraps(init)
        def wrapper(self, *args, **kwargs):
            nonlocal init

            # Set the __require__ mark for all base classes that have the mark to True.
            for base in bases:
                if hasattr(base, "__init__"):
                    baseinit = getattr(base, "__init__")
                    if hasattr(baseinit, "__require__"):
                        baseinit.__require__ = True

            # Call the child initializer.
            init(self, *args, **kwargs)

            # Check that __required__ marks have now been changed to False. Note that this is done
            # by the wrapper in the @require decorator.
            for base in bases:
                if hasattr(base, "__init__"):
                    baseinit = getattr(base, "__init__")
                    if hasattr(baseinit, "__require__"):
                        if baseinit.__require__:
                            raise RuntimeError(
                                f"Class {base.__name__} initializer must be called by child class {name}."
                            )

        # Update the created class' initializer with the wrapper.
        cls.__init__ = wrapper
        attrs['__init__'] = wrapper  # not sure if this is needed too

        super().__init__(name, bases, attrs)

    def __new__(meta, name, bases, attrs):
        """
        When creating a new instance, check if any attributes are defined in the
        parent class and are labeled as protected. If so, throw an error. Also
        check for deprecated abstractmethods to point them to new names while
        issuing warnings.
        """

        for base in bases:
            # Check all the bases.

            for attr, base_val in base.__dict__.items():
                if hasattr(base_val, "__func__"):
                    # if abstract, check if for deprecated methods that can be renamed

                    meta.__check_deprecates(base_val, attr, attrs)

            for attr in attrs:
                # For each attribute in the created class.

                if hasattr(base, attr):
                    # Check if the base class also has that attribute.

                    base_val = getattr(base, attr)

                    # Checks need to be done differently for some objects than others.
                    # property in particular does not like creating new attributes to mark
                    # protection, hence this condition here.

                    # print("base_val=", base_val)

                    if isinstance(base_val, Callable
                                 ) or isinstance(base_val, classmethod):

                        # And if so, whether it is marked as protected.
                        meta.__check_protect(
                            base_val, attr, base.__name__, name
                        )

                    elif isinstance(base_val, property):
                        # If attribute in base class was a property, check whether any of its
                        # constituent methods were marked protected.
                        if base_val.fget is not None:
                            meta.__check_protect(
                                base_val.fget, attr, base.__name__, name
                            )
                        if base_val.fset is not None:
                            meta.__check_protect(
                                base_val.fset, attr, base.__name__, name
                            )
                        if base_val.fdel is not None:
                            meta.__check_protect(
                                base_val.fdel, attr, base.__name__, name
                            )
                    else:
                        pass

        return super().__new__(meta, name, bases, attrs)


# method decorator
def derive(**derivations: Dict[str, 'decorator']):
    """
    A decorator that creates multiple methods based on the given `func`, each as
    named and wrapped by the given set of `derivations`. Each derivation must be
    a method decorator. Methods derived in this way will need pylint exceptions
    for E1101 at call sites. For example, using:

    # pylint: disable=E1101
    """

    # TODO: modify docstring

    frame = inspect.currentframe()
    try:
        # get the caller's locals so we can give them the derived methods
        locals = frame.f_back.f_locals

        def wrapper(func):
            for name, decorator in derivations.items():
                locals[name] = decorator()(func)

            # Returned function is added to caller's locals as per decorator
            # semantics assuming `derive` is used as a decorator.
            return func

        return wrapper
    finally:
        del frame


# method decorator
def singlefun_of_manyfun():
    """
    Convert a method that accepts and returns a list of items to instead
    accept and return a single item. Any args other than the first are preserved.
    """

    # TODO: modify docstring

    def wrapper(func: Callable[[List[U]], List[V]]) -> Callable[[U], V]:

        @functools.wraps(func)
        def ret_fun(item: U, *args, **kwargs) -> V:
            results: List[V] = func([item], *args, **kwargs)
            return results[0]

        return ret_fun

    return wrapper


# method decorator
def self_singlefun_of_self_manyfun():
    """
    Convert a member method that accepts and returns a list of items to instead
    accept and return a single item. Self and args other than the first non-self
    arg are preserved.
    """

    # TODO: modify docstring

    def wrapper(func: Callable[[C, List[U]], List[V]]) -> Callable[[C, U], V]:

        @functools.wraps(func)
        def ret_fun(self: C, item: U, *args, **kwargs) -> V:
            results: List[V] = func(self, [item], *args, **kwargs)
            return results[0]

        return ret_fun

    return wrapper
