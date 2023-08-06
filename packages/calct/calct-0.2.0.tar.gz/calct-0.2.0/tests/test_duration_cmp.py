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


def test_duration_lt():
    assert Duration(hours=1) < Duration(minutes=61)


def test_duration_gt():
    assert Duration(hours=1) > Duration(minutes=59)


def test_duration_le():
    assert Duration(hours=1) <= Duration(minutes=61)
    assert Duration(hours=1) <= Duration(minutes=60)


def test_duration_ge():
    assert Duration(hours=1) >= Duration(minutes=59)
    assert Duration(hours=1) >= Duration(minutes=60)


def test_duration_eq():
    assert Duration(hours=1) == Duration(minutes=60)


def test_duration_ne():
    assert Duration(hours=1) != Duration(minutes=61)
    assert Duration(hours=1) != Duration(minutes=59)


def test_duration_eq_num():
    with pytest.raises(TypeError):
        _ = Duration(hours=1) == 1  # type:ignore


def test_duration_ne_num():
    with pytest.raises(TypeError):
        _ = Duration(hours=1) != 1  # type:ignore


def test_duration_lt_num():
    with pytest.raises(TypeError):
        _ = Duration(hours=1) < 2  # type:ignore


def test_duration_gt_num():
    with pytest.raises(TypeError):
        _ = Duration(hours=2) > 1  # type:ignore


def test_duration_le_num():
    with pytest.raises(TypeError):
        _ = Duration(hours=1) <= 2  # type:ignore
    with pytest.raises(TypeError):
        _ = Duration(hours=1) <= 1  # type:ignore


def test_duration_ge_num():
    with pytest.raises(TypeError):
        _ = Duration(hours=2) >= 1  # type:ignore
    with pytest.raises(TypeError):
        _ = Duration(hours=2) >= 2  # type:ignore
