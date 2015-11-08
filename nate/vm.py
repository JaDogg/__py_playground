from __future__ import absolute_import
from collections import deque


class Instruction(object):
    def __call__(self, vm, match):
        pass


class Fetch(Instruction):
    def __init__(self, pos):
        self._pos = pos

    def __call__(self, vm, match):
        vm.push(match.group(self._pos))

    def __repr__(self):
        return "<fetch:{d}>".format(d=repr(self._pos))


class Push(Instruction):
    def __init__(self, value):
        self._value = value

    def __call__(self, vm, match):
        vm.push(self._value)

    def __repr__(self):
        return "<push:{d}>".format(d=repr(self._value))


class CallFunc(Instruction):
    def __init__(self, func):
        self._func = func

    def __call__(self, vm, match):
        self._func(vm, match)

    def __repr__(self):
        return "<call:{d}>".format(d=repr(self._func))


class NateVm(deque, object):
    def __init__(self):
        deque.__init__(self)

    def run(self, match, code):
        self.clear()
        for instruction in code:
            instruction(self, match)

    def push(self, *atoms):
        for atom in atoms:
            self.stack.appendleft(atom)
