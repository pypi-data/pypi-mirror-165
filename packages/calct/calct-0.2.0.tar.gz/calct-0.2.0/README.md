# Calct
Easily do calculations on hours and minutes using the command line

## TODO
1. Improve README and documentation
2. Add more tests
3. Custom parsing of durations without using `strptime` to support more formats
 - `25h` (bigger than 23h)
 - `h61`, `61m` (bigger than 60m)
 - `0.1h`(float format for hours)
