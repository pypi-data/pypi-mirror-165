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

from calct.parser import Associativity, Operation, add, mul, op_to, sub, truediv


def test_add():
    assert Operation.ADD == Operation("+")
    assert Operation.ADD.operation is add
    assert Operation.ADD.operation(1, 2) == 3
    assert Operation.ADD.associativity == Associativity.LEFT


def test_sub():
    assert Operation.SUB == Operation("-")
    assert Operation.SUB.operation is sub
    assert Operation.SUB.operation(1, 2) == -1
    assert Operation.SUB.associativity == Associativity.LEFT


def test_mul():
    assert Operation.MUL == Operation("*")
    assert Operation.MUL.operation is mul
    assert Operation.MUL.operation(3, 2) == 6
    assert Operation.MUL.associativity == Associativity.LEFT


def test_div():
    assert Operation.DIV == Operation("/")
    assert Operation.DIV.operation is truediv
    assert Operation.DIV.operation(1, 2) == 0.5
    assert Operation.DIV.associativity == Associativity.LEFT


def test_to():
    assert Operation.TO == Operation("@")
    assert Operation.TO.operation is op_to
    assert Operation.TO.operation(2, 5) == 3
    assert Operation.TO.associativity == Associativity.RIGHT


def test_order_of_operations():
    assert Operation.ADD.precedence == Operation.SUB.precedence
    assert Operation.MUL.precedence == Operation.DIV.precedence

    assert Operation.ADD.precedence < Operation.MUL.precedence

    assert Operation.TO.precedence > Operation.MUL.precedence
