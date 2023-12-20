import operator
import re
import sys

workflows = {}
parts = []

with open(sys.argv[1]) as f:
    rule_re = re.compile(r"^(.*)\{(.*)\}")
    condition_re = re.compile(r"^(.*)([<>])(.*)")
    for line in f:
        data = line.strip()
        if not data:
            break
        m = rule_re.match(data)
        name = m.group(1)
        rules = m.group(2).split(',')
        workflows[name] = []
        workflow = workflows[name]
        for rule in rules:
            l = rule.split(':')
            if len(l) == 1:
                workflow.append({'action': l[0]})
            else:
                c_m = condition_re.match(l[0])
                workflow.append({'action': l[1],
                                 'condition': {'variable': c_m.group(1),
                                               'op': operator.lt if c_m.group(2) == '<' else operator.gt,
                                               'value': int(c_m.group(3))}})
    part_re = re.compile(r"^\{x=(.*),m=(.*),a=(.*),s=(.*)\}")
    for line in f:
        m = part_re.match(line)
        parts.append({'x': int(m.group(1)),
                      'm': int(m.group(2)),
                      'a': int(m.group(3)),
                      's': int(m.group(4))})

def run_workflow(part, workflow):
    for item in workflow:
        if 'condition' not in item:
            return item['action']
        if item['condition']['op'](part[item['condition']['variable']], item['condition']['value']):
            return item['action']


def get_rating(part):
    return sum(part.values())

total_rating = 0
max_depth = 0
for part in parts:
    workflow = 'in'
    while workflow:
        action = run_workflow(part, workflows[workflow])
        if action == 'A':
            rating = get_rating(part)
            total_rating += rating
            workflow = None
        elif action == 'R':
            workflow = None
        else:
            workflow = action

print(f"part1: {total_rating}")

def count_items(ranges):
    total_count = 0
    for variable_range in ranges.values():
        count = variable_range['max'] - variable_range['min'] + 1
        if not total_count:
            total_count = count
        else:
            total_count *= count
    return total_count

def split_ranges(ranges, condition):
    if condition['variable'] not in ranges:
        return {},{}

    matching_ranges = {}
    non_matching_ranges = {}

    if condition['op'] == operator.lt:
        min_matching = ranges[condition['variable']]['min']
        max_matching = min(ranges[condition['variable']]['max'], condition['value'] - 1)

        min_non_matching = max(ranges[condition['variable']]['min'], condition['value'])
        max_non_matching = ranges[condition['variable']]['max']

        if min_matching <= max_matching:
            matching_ranges = {condition['variable']: {'min': min_matching, 'max': max_matching}}

        if min_non_matching <= max_non_matching:
            non_matching_ranges = {condition['variable']: {'min': min_non_matching, 'max': max_non_matching}}
    else:
        min_non_matching = ranges[condition['variable']]['min']
        max_non_matching = min(ranges[condition['variable']]['max'], condition['value'])

        min_matching = max(ranges[condition['variable']]['min'], condition['value'] + 1)
        max_matching = ranges[condition['variable']]['max']

        if min_non_matching <= max_non_matching:
            non_matching_ranges = {condition['variable']: {'min': min_non_matching, 'max': max_non_matching}}

        if min_matching <= max_matching:
            matching_ranges = {condition['variable']: {'min': min_matching, 'max': max_matching}}

    for variable in ranges:
        if matching_ranges and not variable in matching_ranges:
            matching_ranges[variable] = ranges[variable]
        if non_matching_ranges and not variable in non_matching_ranges:
            non_matching_ranges[variable] = ranges[variable]

    return matching_ranges, non_matching_ranges

def run_ranges_workflow(workflows, workflow, ranges):
    approved = 0
    for item in workflows[workflow]:
        if 'condition' in item:
            matching_ranges, non_matching_ranges = split_ranges(ranges, item['condition'])
        else:
            matching_ranges = ranges
            non_matching_ranges = []

        if matching_ranges:
            if item['action'] == 'A':
                approved += count_items(matching_ranges)
            elif item['action'] == 'R':
                pass
            else:
                approved += run_ranges_workflow(workflows, item['action'], matching_ranges)

        if not non_matching_ranges:
            break
        ranges = non_matching_ranges

    return approved


ranges = {'x': {'min':1, 'max': 4000},
          'm': {'min':1, 'max': 4000},
          'a': {'min':1, 'max': 4000},
          's': {'min':1, 'max': 4000}}

print(f"part2: {run_ranges_workflow(workflows, 'in', ranges)}")
