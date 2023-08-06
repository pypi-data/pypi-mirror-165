#   calct: Easily do calculations on hours and minutes using the command line
#   Copyright (C) 2022  Philippe Warren
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

from __future__ import annotations

import logging
from collections import deque
from enum import Enum
from operator import add, mul, sub, truediv
from typing import Any, Callable, Union, cast

from calct.common import (
    DIGITS_STR,
    FLOAT_CHARS_STR,
    FLOAT_EXPONENT_STR,
    FLOAT_SEPARATOR_EXPONENT_STR,
    OPS_PAREN_STR,
    OPS_STR,
    SIGN_STR,
    WHITESPACE_STR,
    Number,
)
from calct.duration import Duration


def lex(input_str: str) -> list[str]:
    """Lexes the input string into a list of tokens"""
    tokens: list[str] = []
    buffer: list[str] = []

    logging.debug(input_str)

    def add_token():
        if len(buffer) > 0:
            tokens.append("".join(buffer))
            buffer.clear()

    last_char = None

    for char in input_str:

        logging.debug(f"{char=}, {buffer=}, {tokens=}")
        if char in OPS_PAREN_STR:
            if last_char and last_char in FLOAT_EXPONENT_STR:
                if char in SIGN_STR:
                    buffer.append(char)
                else:
                    raise ValueError(
                        f"`{char}` is following `{FLOAT_EXPONENT_STR}` "
                        f"and is not a digit `{DIGITS_STR}` or a sign `{SIGN_STR}`"
                    )

            else:
                add_token()
                tokens.append(char)
        elif char in WHITESPACE_STR:
            add_token()
        elif char in FLOAT_CHARS_STR:
            buffer.append(char)
        elif char in Duration.get_hour_and_minute_seps():
            buffer.append(char)
        else:
            raise ValueError(
                f"`{char}` is not a digit `{DIGITS_STR}`, "
                f"an operator or parenthesis `{OPS_PAREN_STR}`, "
                f"a whitespace, a digit separator or exponent `{FLOAT_SEPARATOR_EXPONENT_STR}`, "
                f"or a time unit or separator `{''.join(Duration.get_hour_and_minute_seps())}`"
            )
        last_char = char

    add_token()

    return tokens


class Associativity(Enum):
    """Enum for associativity"""

    LEFT = 1
    RIGHT = 2


def op_to(val1: Any, val2: Any) -> Any:
    """Implements the `to` operator"""
    return val2 - val1


class Operation(Enum):
    """Enum for operations"""

    ADD = "+"
    SUB = "-"
    MUL = "*"
    DIV = "/"
    TO = "@"

    @property
    def operation(self) -> Callable[[Any, Any], Any]:
        """Dispatches the operation to the correct function"""
        if self is Operation.ADD:
            return add

        if self is Operation.SUB:
            return sub

        if self is Operation.MUL:
            return mul

        if self is Operation.DIV:
            return truediv

        if self is Operation.TO:
            return op_to

        return NotImplemented

    @property
    def precedence(self) -> int:
        """Returns the precedence of the operation"""
        if self is Operation.ADD:
            return 2

        if self is Operation.SUB:
            return 2

        if self is Operation.MUL:
            return 3

        if self is Operation.DIV:
            return 3

        if self is Operation.TO:
            return 4

        return NotImplemented

    @property
    def associativity(self) -> Associativity:
        """Returns the associativity of the operation"""
        if self is Operation.ADD:
            return Associativity.LEFT

        if self is Operation.SUB:
            return Associativity.LEFT

        if self is Operation.MUL:
            return Associativity.LEFT

        if self is Operation.DIV:
            return Associativity.LEFT

        if self is Operation.TO:
            return Associativity.RIGHT

        return NotImplemented


def parse(tokens: list[str]) -> deque[str]:
    """Parses the tokens into a Reverse Polish Notation (RPN) stack"""
    logging.debug(tokens)

    out_queue: deque[str] = deque()
    op_stack: deque[str] = deque()

    for token in tokens:
        if token not in OPS_PAREN_STR:
            out_queue.append(token)
        elif token in OPS_STR:
            while (len(op_stack) > 0 and op_stack[-1] in OPS_STR) and (
                (Operation(op_stack[-1]).precedence > Operation(token).precedence)
                or (
                    (Operation(op_stack[-1]).precedence == Operation(token).precedence)
                    and Operation(token).associativity == Associativity.LEFT
                )
            ):
                out_queue.append(op_stack.pop())
            op_stack.append(token)
        elif token == "(":
            op_stack.append(token)
        elif token == ")":
            if len(op_stack) == 0:
                raise ValueError("Unmatched closing parenthesis")
            while op_stack[-1] != "(":
                out_queue.append(op_stack.pop())
                if len(op_stack) == 0:
                    raise ValueError("Unmatched closing parenthesis")
            op_stack.pop()

    while len(op_stack) > 0:
        if op_stack[-1] == "(":
            raise ValueError("Unmatched opening parenthesis")
        out_queue.append(op_stack.pop())

    return out_queue


def evaluate_rpn(rpn: deque[str]) -> Union[Number, Duration]:
    """Evaluates the Reverse Polish Notation (RPN) stack"""
    eval_stack: deque[Union[str, Number, Duration]] = deque()

    for element in rpn:
        logging.debug(f"{element=}")
        if element in OPS_STR:
            logging.debug(f"op1={eval_stack[-1]!r}, op2={eval_stack[-2]!r}")
            op2 = eval_stack.pop()
            op1 = eval_stack.pop()
            eval_stack.append(Operation(element).operation(op1, op2))
            logging.debug(f"t is {element}, {eval_stack=}")
        else:
            if (common := (set(element) & Duration.get_hour_and_minute_seps())) != set():
                eval_stack.append(Duration.parse(element))
                logging.debug(f"t is a time because it contains {common}, {eval_stack=}")
            else:
                try:
                    eval_stack.append(int(element))
                except ValueError:
                    try:
                        eval_stack.append(float(element))
                    except ValueError as ex:
                        raise ValueError(f"`{element}` is not a valid number") from ex
                logging.debug(f"t is a number, {eval_stack=}")

    if not isinstance(eval_stack[-1], (Duration, int, float)):
        raise ValueError("Invalid expression: the result is not a duration or a number")
    return cast(Union[Number, Duration], eval_stack[-1])


def compute(expr: str) -> Union[Number, Duration]:
    """Computes the value of the expression"""

    # TODO: add error messages to raised exception for each case and remove all try-except blocks here
    try:
        tokens = lex(expr)
    except ValueError as ex:
        raise ex

    try:
        rpn = parse(tokens)
    except ValueError as ex:
        raise ex
    except TypeError as ex:
        print("TypeError IN PARSING")
        raise ex

    try:
        val = evaluate_rpn(rpn)
    except ValueError as ex:
        print("ValueError IN RPN EVALUATION")
        raise ex
    except TypeError as ex:
        print("TypeError IN RPN EVALUATION")
        raise ex

    return val
