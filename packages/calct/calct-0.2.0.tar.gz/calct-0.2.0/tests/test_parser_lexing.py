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

from calct.parser import lex


def test_simple_sum():
    assert lex("2h + 3h + 4h12 + 3h10") == ["2h", "+", "3h", "+", "4h12", "+", "3h10"]


def test_operators():
    assert lex("+-*/()") == ["+", "-", "*", "/", "(", ")"]


def test_paren():
    assert lex("((2*3h))") == ["(", "(", "2", "*", "3h", ")", ")"]


def test_float():
    assert lex("3.2 * 1h") == ["3.2", "*", "1h"]


def test_exponential():
    assert lex("3e2 * 1h") == ["3e2", "*", "1h"]
    assert lex("3E2 * 1h") == ["3E2", "*", "1h"]
    assert lex("3e-2 * 1h") == ["3e-2", "*", "1h"]
