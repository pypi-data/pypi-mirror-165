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

import string
from typing import Union

Number = Union[int, float]


SIGN_STR = "+-"
OPS_STR = SIGN_STR + "*/@"
OPS_PAREN_STR = OPS_STR + "()"

WHITESPACE_STR = string.whitespace

DIGITS_STR = string.digits
FLOAT_EXPONENT_STR = "eE"
FLOAT_SEPARATOR_EXPONENT_STR = "." + FLOAT_EXPONENT_STR
FLOAT_CHARS_STR = DIGITS_STR + FLOAT_SEPARATOR_EXPONENT_STR

DEFAULT_HOUR_SEPARATOR = "h:"
DEFAULT_MINUTE_SEPARATOR = "m"

CANT_BE_CUSTOM_SEPARATOR = OPS_PAREN_STR + FLOAT_CHARS_STR + WHITESPACE_STR
