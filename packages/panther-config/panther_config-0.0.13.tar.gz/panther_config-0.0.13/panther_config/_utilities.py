# Copyright (C) 2022 Panther Labs Inc
#
# Panther Enterprise is licensed under the terms of a commercial license available from
# Panther Labs Inc ("Panther Commercial License") by contacting contact@runpanther.com.
# All use, distribution, and/or modification of this software, whether commercial or non-commercial,
# falls under the Panther Commercial License to the extent it is permitted.

# coding=utf-8
# *** WARNING: generated file
import os
import ast
import json
import types
import base64
import inspect
import textwrap
import datetime
import dataclasses
from typing import List, Dict, Any, Callable, Union, cast


@dataclasses.dataclass(frozen=True)
class ConfigNodeOrigin:
    pkg: str = "none"
    name: str = "none"

    def to_dict(self) -> Dict[str, str]:
        return dict(pkg=self.pkg, name=self.name)


def origin_factory() -> ConfigNodeOrigin:
    stack = inspect.stack()
    frame = stack[2]

    if not frame:
        return ConfigNodeOrigin()

    module = inspect.getmodule(frame[0])

    if not module:
        return ConfigNodeOrigin()

    module_name = module.__name__ or "none"
    return ConfigNodeOrigin(
        pkg=module.__package__ or "none",
        name=f"{module_name}.{frame.function}",
    )


@dataclasses.dataclass(frozen=True)
class ConfigNode:
    _origin: ConfigNodeOrigin = dataclasses.field(
        default_factory=origin_factory, init=False
    )

    def __post_init__(self) -> None:
        if self._output_key():
            cache.add(self._output_key(), self)

    def _typename(self) -> str:
        return "ConfigNode"

    def _output_key(self) -> str:
        return ""

    def _fields(self) -> List[str]:
        return []


class _Cache:
    _data: Dict[str, List[ConfigNode]]
    _cache_dir: str
    _cache_file: str

    def __init__(self) -> None:
        self._data = dict()
        self._cache_dir = os.path.abspath(
            os.environ.get("PANTHER_CACHE_DIR") or os.path.join(".", ".panther")
        )
        self.prep_cache_dir()

        cache_file_name = (
            os.environ.get("PANTHER_CONFIG_CACHE_FILENAME") or "panther-config-cache"
        )

        self._cache_file = os.path.join(self._cache_dir, cache_file_name)

        self.prep_cache_file()

    def prep_cache_dir(self) -> None:
        if not os.path.exists(self._cache_dir):
            os.mkdir(self._cache_dir)

    def prep_cache_file(self) -> None:
        with open(self._cache_file, "w") as f:
            pass

    def add(self, key: str, node: ConfigNode) -> None:
        if self._cache_file is None:
            return

        with open(self._cache_file, "a") as f:
            f.write(
                json.dumps(
                    dict(
                        key=key,
                        created_at=datetime.datetime.now(
                            datetime.timezone.utc
                        ).strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
                        panther_config_version="2022-08-17",
                        val=to_intermediate(node),
                    )
                )
            )
            f.write("\n")


cache = _Cache()


class FuncTransformer(ast.NodeTransformer):
    def __init__(self, ns: Dict[Any, Any], local_names: List[str] = None):
        self._ns = ns
        self._local_names = local_names or []

    # remove type annotations and decorators
    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.AST:
        self._local_names.append(node.name)

        node.returns = None
        if node.args.args:
            for arg in node.args.args:
                self._local_names.append(arg.arg)
                arg.annotation = None

        node.decorator_list.clear()

        return self._closure_delve(node)

    # read imports into _local_names
    def visit_Import(self, node: ast.Import) -> ast.AST:
        for name in node.names:
            self._local_names.append(name.asname or name.name)

        return self.generic_visit(node)

    # read from-imports into _local_names
    def visit_ImportFrom(self, node: ast.ImportFrom) -> ast.AST:
        for name in node.names:
            self._local_names.append(name.asname or name.name)

        return self.generic_visit(node)

    # auto-resolve attributes to constant values
    def visit_Attribute(self, node: ast.Attribute) -> ast.AST:
        root_name = self._attribute_root(node)
        if isinstance(node.ctx, ast.Load) and (root_name not in self._local_names):
            return self._const_replace(node)

        return self.generic_visit(node)

    # auto-resolve names to constant values
    def visit_Name(self, node: ast.Name) -> ast.AST:
        if isinstance(node.ctx, ast.Store):
            self._local_names.append(node.id)
            return self.generic_visit(node)

        if isinstance(node.ctx, ast.Load) and (node.id not in self._local_names):
            return self._const_replace(node)

        return self.generic_visit(node)

    def visit_Lambda(self, node: ast.Lambda) -> ast.AST:
        return self._closure_delve(node)

    def _closure_delve(self, node: Union[ast.Lambda, ast.FunctionDef]) -> ast.AST:
        prev_args = self._local_names.copy()
        for arg in node.args.args:
            self._local_names.append(arg.arg)

        new_node = self.generic_visit(node)
        self._local_names = prev_args

        return new_node

    def _const_replace(self, node: ast.AST) -> Union[ast.Constant, ast.AST]:
        try:
            c = ast.unparse(node)
            x = eval(c, self._ns)

            const_node = ast.Constant(x)

            if inspect.isbuiltin(x):
                return self.generic_visit(node)

            if ast.unparse(cast(ast.AST, const_node))[0] == "<":
                return self.generic_visit(node)

            return const_node
        except Exception:
            return self.generic_visit(node)

    def _attribute_root(self, node: Union[ast.AST, ast.expr]) -> str:
        if isinstance(node, ast.Name):
            return node.id

        if isinstance(node, ast.Attribute):
            return self._attribute_root(node.value)

        if isinstance(node, ast.Call):
            return self._attribute_root(node.func)

        raise RuntimeError(
            "failed to recurse to attribute root. unhandled node: " + repr(node)
        )


def snapshot_func(target_func: Callable) -> str:
    original_src = textwrap.dedent(inspect.getsource(target_func))
    original_tree = ast.parse(
        original_src,
        filename=(inspect.getsourcefile(target_func) or "unknown"),
        mode="exec",
    )
    v_nonlocal, v_global, v_builtins, v_unbound = inspect.getclosurevars(target_func)
    parsed_tree = FuncTransformer(ns={**v_nonlocal, **v_global}).visit(original_tree)
    parsed_src = ast.unparse(parsed_tree)
    return parsed_src


def to_intermediate(obj: Any) -> Any:
    if isinstance(obj, ConfigNode):
        field_data = dict()

        for field_name in obj._fields():
            field_data[field_name] = to_intermediate(getattr(obj, field_name))

        return dict(
            o=obj._origin.to_dict(),
            t=obj._typename(),
            d=field_data,
        )

    if isinstance(obj, list):
        return [*map(to_intermediate, obj)]

    if isinstance(obj, types.FunctionType):
        return dict(
            src=base64.b64encode(snapshot_func(obj).encode("utf-8")).decode("utf-8"),
            name=obj.__name__,
        )

    return obj
