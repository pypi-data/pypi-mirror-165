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

from calct.duration import Duration


def test_duration_str_24h45():
    assert "24h45" == str(Duration(hours=24, minutes=45))


def test_duration_str_null():
    assert "0h00" == str(Duration(hours=0, minutes=0))


def test_duration_default_is_null():
    assert "0h00" == str(Duration())


def test_duration_repr():
    assert repr(Duration()) == "Duration(hours=0, minutes=0)"
