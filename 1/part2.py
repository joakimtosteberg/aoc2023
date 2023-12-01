import sys
import re

calibration_sum = 0

search_re = re.compile(".*?(0|1|2|3|4|5|6|7|8|9|one|two|three|four|five|six|seven|eight|nine)(?:(?:.*(0|1|2|3|4|5|6|7|8|9|one|two|three|four|five|six|seven|eight|nine))|.*)")

def get_digit(data):
    if data == "one":
        return "1"
    if data == "two":
        return "2"
    if data == "three":
        return "3"
    if data == "four":
        return "4"
    if data == "five":
        return "5"
    if data == "six":
        return "6"
    if data == "seven":
        return "7"
    if data == "eight":
        return "8"
    if data == "nine":
        return "9"
    return data
    

with open(sys.argv[1]) as f:
    for line in f:
        m = search_re.match(line)
        calibration_sum += int(get_digit(m.group(1)) + get_digit(m.group(2) if m.group(2) else m.group(1)))

print(f"{calibration_sum}")
