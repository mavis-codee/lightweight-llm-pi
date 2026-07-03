from __future__ import annotations

import ast
from dataclasses import dataclass
import math
import operator
import re
from typing import Callable


class CalculationError(ValueError):
    """Raised when an expression is not safe or cannot be calculated."""


@dataclass(frozen=True)
class CalculationResult:
    expression: str
    value: float

    def format(self) -> str:
        if self.value == int(self.value):
            value = str(int(self.value))
        else:
            value = f"{self.value:.10g}"
        return f"{self.expression} = {value}"


_BIN_OPS: dict[type[ast.operator], Callable[[float, float], float]] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

_UNARY_OPS: dict[type[ast.unaryop], Callable[[float], float]] = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

_NAMES = {
    "pi": math.pi,
    "e": math.e,
}

_FUNCS: dict[str, Callable[..., float]] = {
    "abs": abs,
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log10,
    "ln": math.log,
    "round": round,
}

_COMMAND_PREFIX = re.compile(r"^\s*(/calc|calc:|计算|算一下|帮我算|请计算)\s*", re.I)
_EXPR_CHARS = re.compile(r"^[0-9eEpiPI+\-*/%().,\s_a-zA-Z]+$")


def try_calculate(text: str) -> CalculationResult | None:
    expression = extract_expression(text)
    if not expression:
        return None
    return CalculationResult(expression=expression, value=calculate(expression))


def extract_expression(text: str) -> str | None:
    cleaned = _COMMAND_PREFIX.sub("", text.strip()).strip()
    if not cleaned:
        return None

    if "=" in cleaned:
        cleaned = cleaned.split("=", 1)[0].strip()

    if not _EXPR_CHARS.fullmatch(cleaned):
        return None

    has_operator = any(op in cleaned for op in ["+", "-", "*", "/", "%", "sqrt", "sin", "cos", "tan", "log", "ln"])
    if not has_operator:
        return None
    return cleaned


def calculate(expression: str) -> float:
    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError as exc:
        raise CalculationError("表达式格式不正确。") from exc

    value = _eval_node(tree.body)
    if not math.isfinite(value):
        raise CalculationError("结果不是有限数字。")
    if abs(value) > 1e18:
        raise CalculationError("结果过大，请拆成更小的计算。")
    return float(value)


def _eval_node(node: ast.AST) -> float:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)

    if isinstance(node, ast.Name):
        if node.id in _NAMES:
            return float(_NAMES[node.id])
        raise CalculationError(f"不支持的变量：{node.id}")

    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in _BIN_OPS:
            raise CalculationError("不支持的运算符。")
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        if op_type is ast.Pow and (abs(right) > 12 or abs(left) > 1e6):
            raise CalculationError("指数计算过大，请拆成更小的计算。")
        try:
            return float(_BIN_OPS[op_type](left, right))
        except ZeroDivisionError as exc:
            raise CalculationError("不能除以 0。") from exc

    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in _UNARY_OPS:
            raise CalculationError("不支持的一元运算。")
        return float(_UNARY_OPS[op_type](_eval_node(node.operand)))

    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name) or node.func.id not in _FUNCS:
            raise CalculationError("不支持的函数。")
        args = [_eval_node(arg) for arg in node.args]
        if len(args) > 2:
            raise CalculationError("函数参数过多。")
        return float(_FUNCS[node.func.id](*args))

    raise CalculationError("表达式包含不安全或不支持的内容。")
