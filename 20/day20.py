from abc import ABC, abstractmethod
import math
import queue
import re
import sys

modules = {}

class Module(ABC):
    def __init__(self, name, outputs):
        self.name = name
        self.outputs = outputs
        self.inputs = set()

    def add_input(self, input_module):
        self.inputs.add(input_module)

    @abstractmethod
    def activate_input(self, input_name, signal, press_number):
        pass

    def done(self):
        return True

class Broadcaster(Module):
    def __init__(self, name, outputs):
        super().__init__(name, outputs)

    def activate_input(self, input_name, signal, press_number):
        return signal

class FlipFlop(Module):
    def __init__(self, name, outputs):
        super().__init__(name, outputs)
        self.state = False

    def activate_input(self, input_name, signal, press_number):
        if not signal:
            self.state = not self.state
            return self.state
        return None

class Conjunction(Module):
    def __init__(self, name, outputs):
        super().__init__(name, outputs)
        self.states = {}
        self.time_to_high = {}

    def add_input(self, input_module):
        super().add_input(input_module)
        self.states[input_module] = False

    def activate_input(self, input_name, signal, press_number):
        self.states[input_name] = signal
        # Assumes that all inputs to conjunctions are strictly cyclic
        # with exactly one high value in the cycle, this is apparently
        # true for the given input data. Not sure if it really holds
        # in general...
        if signal and input_name not in self.time_to_high:
            self.time_to_high[input_name] = press_number + 1
        return not all(self.states.values())

    def done(self):
        return len(self.states) == len(self.time_to_high)

class Output(Module):
    def __init__(self, name):
        super().__init__(name, [])

    def activate_input(self, input_name, signal, press_number):
        return None

class Button(Module):
    def __init__(self):
        super().__init__("button", ['broadcaster'])

    def activate_input(self, input_name, signal, press_number):
        return signal

modules = {'button': Button(), 'rx': Output('rx')}
with open(sys.argv[1]) as f:
    r = re.compile(r"([%&])?(.*) -> (.*)")
    for line in f:
        m = r.match(line)
        module_type = m.group(1)
        module_name = m.group(2)
        module_outputs = [o.strip() for o in m.group(3).split(',')]


        if module_type == '%':
            module = FlipFlop(module_name, module_outputs)
        elif module_type == '&':
            module = Conjunction(module_name, module_outputs)
        else:
            module = Broadcaster(module_name, module_outputs)

        modules[module.name] = module

for module in modules.values():
    for output in module.outputs:
        if output in modules:
            modules[output].add_input(module.name)

statistics = {True: 0, False: 0}

i = 0
while True:
    output_queue = queue.Queue()
    output_queue.put({'name': 'button', 'signal': False})
    while not output_queue.empty():
        output_item = output_queue.get()
        statistics[output_item['signal']] += len(modules[output_item['name']].outputs)
        for input_name in modules[output_item['name']].outputs:
            if input_name == 'rx' and not output_item['signal']:
                print(f"part2: {i}")
            if input_name in modules:
                input_module = modules[input_name]
                signal = input_module.activate_input(output_item['name'], output_item['signal'], i)
                if signal is not None:
                    output_queue.put({'name': input_name, 'signal': signal})
    i = i + 1
    if i == 1000:
        print(f"part1: {statistics[True]*statistics[False]}")


    for module in modules.values():
        if not module.done():
            break
    else:
        print(f"All done after {i} iterations")
        break


print(math.lcm(*modules[list(modules['rx'].inputs)[0]].time_to_high.values()))
