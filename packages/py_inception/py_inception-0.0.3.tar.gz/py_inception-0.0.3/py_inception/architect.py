from __future__ import annotations
from typing import Any

import inspect
import types

from .abstract import AArchitect


class CoreArchitect(AArchitect):
    """Core Architect extract common information from object of any type"""

    def parse(
        self,
        var: Any,
        parse_as: str = "object",
        *,
        metadata: dict | None = None,
    ):
        # CoreArchitect stops chain for "object" and "attr"
        if parse_as in ("object", "attr"):
            return self.parse_object(var, metadata=metadata)

        return self.parse_next(var, parse_as, metadata=metadata)

    def parse_object(self, var: Any, *, metadata: dict | None = None):
        if self.e is None or self.e.maze is None:
            return

        id_ = id(var)
        maze = self.e.maze

        # Check if already parsed
        if id_ in maze.objects:
            return {"id": id_, "mode": "object"}

        obj: dict = {}
        maze.objects[id_] = obj

        try:
            obj["name"] = var.__name__
            if obj["name"].startswith("py_inception."):
                return
        except Exception:
            pass

        try:
            obj["module"] = var.__module__
            if obj["module"].startswith("py_inception"):
                return {"id": id_, "mode": "object"}
        except Exception:
            pass

        try:
            obj["qualname"] = var.__qualname__
        except Exception:
            pass

        try:
            obj["class"] = id(var.__class__)
            self.e.parse(var.__class__, "object")
        except Exception:
            pass

        try:
            obj["mro"] = []
            for i in var.__mro__:
                obj["mro"].append(id(i))
                self.e.parse(i, "object")
        except Exception:
            del obj["mro"]

        try:
            obj["bases"] = []
            for i in list(var.__bases__):
                obj["bases"].append(id(i))
                self.e.parse(i, "object")
        except Exception:
            del obj["bases"]

        try:
            d = var.__dict__
            obj["dict"] = {}
            for i in d:
                res = self.e.parse(d[i], "attr", metadata={
                                   "object": var, "attr": i})
                if res is not None:
                    obj["dict"][i] = res
        except Exception:
            pass

        return {"id": id_, "mode": "object"}


class StdTypesArchitect(AArchitect):
    """StdTypes Architect extract data from python standard types objects:
    * Value: str, int, float, bool, None;
    * Sequence: list, set, frozenset, tuple
    * Array: dict

    Extract values for presentation in a convenient form.
    """

    def __init__(self, transparent: bool = False, **kwargs):
        super().__init__(**kwargs)
        self.transparent = transparent

    def parse(
        self,
        var: Any,
        parse_as: str = "object",
        *,
        metadata: dict | None = None,
    ):
        parsed = self.parse_stdtype(var, parse_as, metadata=metadata)

        # If not standard type var, pass to next Architect
        # If parsing as object - CoreArchitect must create full record in Maze
        if not parsed or parse_as == "object":
            return self.parse_next(var, parse_as, metadata=metadata)

        # Pass to next Architect in transparent mode
        # but returned data will be overwritten
        if self.transparent:
            self.parse_next(var, parse_as, metadata=metadata)

        return parsed

    def parse_stdtype(
        self,
        var: Any,
        parse_as: str = "object",
        *,
        metadata: dict | None = None,
    ):
        if self.e is None or self.e.maze is None:
            return

        id_ = id(var)
        maze = self.e.maze

        if type(var) == str:
            maze.strings[id_] = var
            return {"mode": "str", "type": "str", "id": id_}
        elif type(var) in (int, float):
            return {"mode": "dir", "type": type(var).__name__, "val": var}
        elif var is None:
            return {"mode": "dir", "type": "NoneType", "val": "None"}
        elif type(var) == bool:
            return {"mode": "dir", "type": "bool", "val": str(var)}
        elif type(var) in (list, set, frozenset, tuple):
            if id_ not in maze.lists:
                maze.lists[id_] = {"type": type(var).__name__, "items": []}
                for i in var:
                    maze.lists[id_]["items"].append(self.e.parse(i, "attr"))
            return {
                "mode": "list",
                "type": type(var).__name__,
                "id": id_,
                "len": len(var),
            }

        elif type(var) == dict:
            if id_ not in maze.dicts:
                maze.dicts[id_] = {"type": type(var).__name__, "items": []}
                for (i, j) in var.items():
                    maze.dicts[id_]["items"].append(
                        (
                            self.e.parse(i, "attr"),
                            self.e.parse(j, "attr"),
                        )
                    )
            return {
                "mode": "dict",
                "type": type(var).__name__,
                "id": id_,
                "len": len(var),
            }

        elif type(var) == property:
            maze.dicts[id_] = {"type": "property", "items": []}
            if getattr(var, "__doc__", None):
                maze.dicts[id_]["items"].append(
                    (
                        {"mode": "dir", "type": "str", "val": "doc"},
                        self.e.parse(var.__doc__, "attr"),
                    )
                )
            if getattr(var, "fget", None):
                maze.dicts[id_]["items"].append(
                    (
                        {"mode": "dir", "type": "str", "val": "fget"},
                        self.e.parse(var.fget, "attr"),
                    )
                )
            if getattr(var, "fset", None):
                maze.dicts[id_]["items"].append(
                    (
                        {"mode": "dir", "type": "str", "val": "fset"},
                        self.e.parse(var.fset, "attr"),
                    )
                )
            if getattr(var, "fdel", None):
                maze.dicts[id_]["items"].append(
                    (
                        {"mode": "dir", "type": "str", "val": "fdel"},
                        self.e.parse(var.fdel, "attr"),
                    )
                )
            return {
                "mode": "dict",
                "type": "property",
                "id": id_,
                "len": len(maze.dicts[id_]["items"]),
            }
        return None


class FuncArchitect(AArchitect):
    """Func Architect extract data from python standard functions"""

    def __init__(self, transparent: bool = False, **kwargs):
        super().__init__(**kwargs)
        self.transparent = transparent

    def parse(
        self,
        var: Any,
        parse_as: str = "object",
        *,
        metadata: dict | None = None,
    ):
        parsed = self.parse_func(var, parse_as, metadata=metadata)

        # If not function, pass to next Architect
        # If parsing as object - CoreArchitect must create full record in Maze
        if not parsed or parse_as == "object":
            return self.parse_next(var, parse_as, metadata=metadata)

        # Pass to next Architect in transparent mode
        # but returned data will be overwritten
        if self.transparent:
            self.parse_next(var, parse_as, metadata=metadata)

        return parsed

    def parse_func(
        self,
        var: Any,
        parse_as: str = "object",
        *,
        metadata: dict | None = None,
    ):
        if self.e is None or self.e.maze is None:
            return

        id_ = id(var)
        maze = self.e.maze
        func_types = (
            types.FunctionType,
            types.BuiltinMethodType,
            types.BuiltinFunctionType,
            types.MethodType,
            types.MethodDescriptorType,
            types.ClassMethodDescriptorType,
            types.MethodWrapperType,
            types.WrapperDescriptorType,
            types.GetSetDescriptorType,
            types.MemberDescriptorType,
        )

        if type(var) not in func_types:
            return None

        if id_ not in maze.funcs:
            maze.funcs[id_] = {"type": type(var).__name__}

            def dict_if_notnone(var, name, dic, dicname):
                _val = getattr(var, name, None)
                if _val:
                    dic[dicname] = _val

            dict_if_notnone(var, "__name__", maze.funcs[id_], "name")
            dict_if_notnone(var, "__module__", maze.funcs[id_], "module")
            dict_if_notnone(var, "__qualname__", maze.funcs[id_], "qualname")

            try:
                _d = self.e.parse(
                    var.__doc__, "attr", metadata={"object": var, "attr": "__doc__"}
                )
                if _d:
                    maze.funcs[id_]["doc"] = _d
            except Exception:
                pass

            if getattr(var, "__code__", None):
                _c = var.__code__

                # Function arguments
                pos_args = []
                kw_args = []
                _cdef = getattr(var, "__defaults__", None) or []
                _ckwdef = getattr(var, "__kwdefaults__", None) or {}
                start_default = _c.co_argcount - len(_cdef)
                names = iter(enumerate(_c.co_varnames))

                # Position arguments
                for _ in range(_c.co_argcount):
                    i, name = next(names)
                    val = {"name": name}
                    if i >= start_default:
                        val["def"] = str(_cdef[i - start_default])
                    if name in var.__annotations__:
                        val["ann"] = str(var.__annotations__[name])
                    pos_args.append(val)

                # Key-value arguments
                for _ in range(_c.co_kwonlyargcount):
                    name = next(names)[1]
                    val = {"name": name}
                    if name in _ckwdef:
                        val["def"] = str(_ckwdef[name])
                    if name in var.__annotations__:
                        val["ann"] = str(var.__annotations__[name])
                    kw_args.append(val)

                # *arg
                if _c.co_flags & inspect.CO_VARARGS:
                    name = next(names)[1]
                    val = {"name": "*" + name}
                    if name in var.__annotations__:
                        val["ann"] = str(var.__annotations__[name])
                    pos_args.append(val)

                # **kwarg
                if _c.co_flags & inspect.CO_VARKEYWORDS:
                    name = next(names)[1]
                    val = {"name": "**" + name}
                    if name in var.__annotations__:
                        val["ann"] = str(var.__annotations__[name])
                    kw_args.append(val)

                maze.funcs[id_]["pos_args"] = pos_args
                maze.funcs[id_]["kw_args"] = kw_args
                maze.funcs[id_]["posonlyargcount"] = _c.co_posonlyargcount

                # File information
                dict_if_notnone(_c, "co_filename",
                                maze.funcs[id_], "co_filename")
                dict_if_notnone(_c, "co_name", maze.funcs[id_], "co_name")
                dict_if_notnone(_c, "co_firstlineno",
                                maze.funcs[id_], "co_firstlineno")

        return {"mode": "func", "type": type(var).__name__, "id": id_}
