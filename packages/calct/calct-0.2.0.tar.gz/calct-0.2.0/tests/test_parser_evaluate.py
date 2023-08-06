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

import pytest

from calct.parser import Duration, deque, evaluate_rpn


def test_triple_sum():
    assert evaluate_rpn(
        deque(
            [
                "2h",
                "3h",
                "+",
                "4h12",
                "+",
                "3h10",
                "+",
            ]
        )
    ) == Duration(hours=12, minutes=22)


def test_double_difference():
    assert evaluate_rpn(deque(["2h12", "1h56", "-", "12m", "-"])) == Duration(minutes=4)


def test_simple_to_operator():
    assert evaluate_rpn(deque(["1h12", "1h56", "@"])) == Duration(minutes=44)


def test_product_difference():
    assert evaluate_rpn(deque(["2h12", "2", "*", "12m", "-"])) == Duration(hours=4, minutes=12)


def test_division_addition():
    assert evaluate_rpn(deque(["2h12", "2", "/", "12m", "-"])) == Duration(minutes=54)


def test_double_product():
    assert evaluate_rpn(deque(["2", "2h12", "*", "3", "*"])) == Duration(hours=12, minutes=72)
    assert evaluate_rpn(deque(["2h12", "2", "*", "3", "*"])) == Duration(hours=12, minutes=72)
    assert evaluate_rpn(deque(["2", "3", "*", "2h12", "*"])) == Duration(hours=12, minutes=72)


def test_double_division():
    assert evaluate_rpn(deque(["2h12", "2", "/", "3", "/"])) == Duration(minutes=22)


def test_parens():
    assert evaluate_rpn(
        deque(
            [
                "2",
                "2h",
                "12m",
                "-",
                "*",
            ]
        )
    ) == Duration(hours=2, minutes=96)


def test_prececence():
    assert evaluate_rpn(deque(["2h12", "12m", "2", "*", "-"])) == Duration(hours=1, minutes=48)
    assert evaluate_rpn(deque(["2", "2h12", "3h14", "@", "*"])) == Duration(hours=2, minutes=4)
    assert evaluate_rpn(deque(["2", "1h02", "*", "3h14", "@"])) == Duration(hours=1, minutes=10)


@pytest.mark.skip("Scope changed, valid now, test needs to be fixed")
def test_invalid_expression():
    with pytest.raises(ValueError):
        evaluate_rpn(deque(["2", "3", "*"]))
