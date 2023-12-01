import sys

calibration_sum = 0
with open(sys.argv[1]) as f:
    for line in f:
        digits = ""
        for c in line:
            if c.isdigit():
                digits += c
                break

        for c in reversed(line):
            if c.isdigit():
                digits += c
                break
        calibration_sum += int(digits)
            

print(f"{calibration_sum}")
        
