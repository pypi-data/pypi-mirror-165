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


def test_duration_mul_int():
    assert Duration(hours=1) * 2 == Duration(hours=2)
    assert 2 * Duration(hours=1) == Duration(hours=2)


def test_duration_mul_float():
    assert Duration(hours=1) * 2.5 == Duration(hours=2.5)
    assert 2.5 * Duration(hours=1) == Duration(hours=2.5)


def test_duration_mul_duration():
    with pytest.raises(TypeError):
        _ = Duration(hours=1) * Duration(hours=2)  # type: ignore


def test_duration_add_duration():
    assert Duration(hours=1) + Duration(minutes=34) == Duration(hours=1, minutes=34)


def test_duration_add_number():
    with pytest.raises(TypeError):
        _ = Duration(hours=1) + 2  # type: ignore


def test_duration_sub_duration():
    assert Duration(hours=3) - Duration(minutes=12) == Duration(hours=2, minutes=48)


def test_duration_sub_duration_negative_result():
    assert Duration(hours=2) - Duration(hours=3) == Duration(hours=-1)


def test_duration_sub_negative_duration():
    assert Duration(hours=2) - Duration(hours=-3) == Duration(hours=5)


def test_duration_sub_number():
    with pytest.raises(TypeError):
        _ = Duration(hours=2) - 2  # type: ignore


def test_duration_div_int():
    assert Duration(hours=2.5) / 2 == Duration(hours=1.25)


def test_duration_div_float():
    assert Duration(hours=2.5) / 2.5 == Duration(hours=1)


def test_duration_div_duration():
    with pytest.raises(TypeError):
        _ = Duration(hours=2) / Duration(hours=2)  # type: ignore
