#! /usr/bin/env python

from collections import Counter
from math import lcm
import sys

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))


class Broadcaster:
    connected: list
    name: str
    pulse: bool

    def __init__(self, l) -> None:
        self.name, modules = l.split(' -> ')
        self.connected = modules.split(', ')
        self.pulse = False

    def send_pulse(self):
        return ((self.name, m, self.pulse) for m in self.connected)

    def receive_pulse(self, pulse, src):
        self.pulse = pulse


class FlipFlop(Broadcaster):
    state: bool = False

    def send_pulse(self):
        if self.pulse:
            return ()

        self.state = not self.state
        return ((self.name, m, self.state) for m in self.connected)


class Conjunction(Broadcaster):
    last_pulses: dict

    def __init__(self, l) -> None:
        super().__init__(l)
        self.last_pulses = dict()

    def send_pulse(self):
        if not self.last_pulses:
            return ((self.name, m, True) for m in self.connected)

        p = not all(self.last_pulses.values())
        return ((self.name, m, p) for m in self.connected)

    def receive_pulse(self, pulse, src):
        self.last_pulses[src] = pulse
        self.pulse = pulse


circuit = dict()
for line in lines:
    if line.startswith('%'):
        module = FlipFlop(line[1:])
    elif line.startswith('&'):
        module = Conjunction(line[1:])
    else:
        module = Broadcaster(line)
    circuit[module.name] = module

# Init modules, especially Conjunctions
for k,m in circuit.items():
    for n in m.connected:
        try:
            circuit[n].receive_pulse(False, k)
        except KeyError:
            pass

cpt = Counter()
for _ in range(1000):
    status = [ ('button', 'broadcaster', False)]
    while status:
        # print(status)
        new_status = []
        cpt.update(p for _,_,p in status)
        for source, module, pulse in status:
            try:
                circuit[module].receive_pulse(pulse, source)
                new_status.extend(circuit[module].send_pulse())
            except KeyError:
                pass
        status = new_status

print("Part 1:", cpt[False]*cpt[True])


# ReInit modules
for k,m in circuit.items():
    if isinstance(m, FlipFlop):
        m.state = False
    for n in m.connected:
        try:
            circuit[n].receive_pulse(False, k)
        except KeyError:
            pass

# see r/adventofcode for explanations...
feed_modules = {'cl': 0, 'rp': 0, 'lb': 0, 'nj': 0}
button_presses = 0
while True:
    status = [ ('button', 'broadcaster', False)]
    button_presses += 1
    while status:
        new_status = []
        cpt.update(p for _,_,p in status)
        for source, module, pulse in status:
            try:
                if module in feed_modules and not pulse:
                    feed_modules[module] = button_presses

                circuit[module].receive_pulse(pulse, source)
                new_status.extend(circuit[module].send_pulse())
            except KeyError:
                pass
        status = new_status

    if all(feed_modules.values()):
        break

print("Part 2:", lcm(*feed_modules.values()))
