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

from calct.parser import deque, parse


def test_triple_sum():
    assert parse(["2h", "+", "3h", "+", "4h12", "+", "3h10"]) == deque(
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


def test_double_difference():
    assert parse(["2h12", "-", "1h56", "-", "12m"]) == deque(["2h12", "1h56", "-", "12m", "-"])


def test_product_difference():
    assert parse(["2h12", "*", "2", "-", "12m"]) == deque(["2h12", "2", "*", "12m", "-"])


def test_divide_addition():
    assert parse(["2h12", "/", "2", "-", "12m"]) == deque(["2h12", "2", "/", "12m", "-"])


def test_double_product():
    assert parse(["2", "*", "2h12", "*", "3"]) == deque(["2", "2h12", "*", "3", "*"])
    assert parse(["2h12", "*", "2", "*", "3"]) == deque(["2h12", "2", "*", "3", "*"])
    assert parse(["2", "*", "3", "*", "2h12"]) == deque(["2", "3", "*", "2h12", "*"])


def test_double_divide():
    assert parse(["2h12", "/", "2", "/", "3"]) == deque(["2h12", "2", "/", "3", "/"])


def test_parens():
    assert parse(["2", "*", "(", "2h", "-", "12m", ")"]) == deque(
        [
            "2",
            "2h",
            "12m",
            "-",
            "*",
        ]
    )


def test_prececence():
    assert parse(["2h12", "-", "12m", "*", "2"]) == deque(["2h12", "12m", "2", "*", "-"])
    assert parse(["2", "*", "2h12", "@", "3h14"]) == deque(["2", "2h12", "3h14", "@", "*"])
    assert parse(["(", "2", "*", "1h02", ")", "@", "3h14"]) == deque(["2", "1h02", "*", "3h14", "@"])


def test_unmatched_opening_paren_at_beginning():
    with pytest.raises(ValueError):
        assert parse(["(", "2", "*", "1h02"])


def test_unmatched_opening_paren_at_end():
    with pytest.raises(ValueError):
        assert parse(["2", "*", "1h02", "("])


def test_unmatched_opening_paren_in_middle_before_op():
    with pytest.raises(ValueError):
        assert parse(["2", "(", "*", "1h02"])


def test_unmatched_opening_paren_in_middle_before_val():
    with pytest.raises(ValueError):
        assert parse(["2", "*", "(", "1h02"])


def test_unmatched_closing_paren_at_end():
    with pytest.raises(ValueError):
        assert parse(["2", "*", "1h02", ")"])


def test_unmatched_closing_paren_at_beginning():
    with pytest.raises(ValueError):
        assert parse([")", "2", "*", "1h02"])


def test_unmatched_closing_paren_in_middle_before_op():
    with pytest.raises(ValueError):
        assert parse(["2", ")", "*", "1h02"])


def test_unmatched_closing_paren_in_middle_before_val():
    with pytest.raises(ValueError):
        assert parse(["2", "*", ")", "1h02"])


def test_unmatched_closing_paren_alone():
    with pytest.raises(ValueError):
        assert parse([")"])
