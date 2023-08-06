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

from calct.duration import Duration


def test_get_separator():
    assert Duration.get_string_hour_minute_separator()


def test_set_separator():
    Duration.set_string_hour_minute_separator(":")
    assert str(Duration()) == "0:00"
    Duration.del_string_hour_minute_separator()


def test_parse_custom_separator():
    Duration.set_string_hour_minute_separator("!")
    time_str = "3!34"
    assert Duration.parse(time_str) == Duration(hours=3, minutes=34)
    Duration.del_string_hour_minute_separator()


def test_set_separator_to_none():
    with pytest.raises(TypeError):
        Duration.set_string_hour_minute_separator(None)  # type: ignore


def test_set_separator_to_number():
    with pytest.raises(TypeError):
        Duration.set_string_hour_minute_separator(12)  # type: ignore
    with pytest.raises(TypeError):
        Duration.set_string_hour_minute_separator(1.23)  # type: ignore


def test_set_separator_to_type():
    with pytest.raises(TypeError):
        Duration.set_string_hour_minute_separator(type)  # type: ignore
    with pytest.raises(TypeError):
        Duration.set_string_hour_minute_separator(object)  # type: ignore
    with pytest.raises(TypeError):
        Duration.set_string_hour_minute_separator(Duration)  # type: ignore


def test_set_separator_to_operators_or_parens():
    with pytest.raises(ValueError):
        Duration.set_string_hour_minute_separator("+")
    with pytest.raises(ValueError):
        Duration.set_string_hour_minute_separator("-")
    with pytest.raises(ValueError):
        Duration.set_string_hour_minute_separator("*")
    with pytest.raises(ValueError):
        Duration.set_string_hour_minute_separator("/")
    with pytest.raises(ValueError):
        Duration.set_string_hour_minute_separator("(")
    with pytest.raises(ValueError):
        Duration.set_string_hour_minute_separator(")")
