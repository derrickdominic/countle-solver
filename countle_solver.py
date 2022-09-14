import argparse
from enum import Enum, auto
from typing import List


class Operation(Enum):
  ADD = auto()
  SUBTRACT = auto()
  MULTIPLY = auto()
  DIVIDE = auto()

  def __str__(self) -> str:
    if (self.name == 'ADD'):
      return '+'
    if (self.name == 'SUBTRACT'):
      return '-'
    if (self.name == 'MULTIPLY'):
      return '*'
    if (self.name == 'DIVIDE'):
      return '/'


def perform(left: int, op: Operation, right: int) -> bool:
  if (op == Operation.ADD):
    return left + right
  if (op == Operation.SUBTRACT):
    return left - right
  if (op == Operation.MULTIPLY):
    return left * right
  if (op == Operation.DIVIDE):
    return left // right


class Equation:
  def __init__(self, left: int, op: Operation, right: int):
    self._left = left
    self._op = op
    self._right = right
    self._result = perform(left=left, op=op, right=right)

  @property
  def result(self) -> int:
    return self._result

  def __eq__(self, other) -> bool:
    if (self._op != other._op):
      return False
    if (self._op == Operation.SUBTRACT or self._op == Operation.DIVIDE):
      return self._left == other._left and self._right == other._right
    return (self._left == other._left and self._right == other._right) or \
        (self._left == other._right and self._right == other._left)
    
  def __str__(self) -> str:
    return f'{self._left} {self._op} {self._right} = {self._result}'


class Solution:
  def __init__(self, equations: List[Equation]):
    self._equations = equations

  def __eq__(self, other) -> bool:
    for equation in self._equations:
      if (other._equations.count(equation) == 0):
        return False
    return True

  def __str__(self) -> str:
    solution_str = ''
    for equation in self._equations:
      solution_str += f'{equation}\n'
    return solution_str


def possible(left: int, op: Operation, right: int) -> bool:
  return (op == Operation.ADD) or \
      (op == Operation.MULTIPLY) or \
      (op == Operation.SUBTRACT and left >= right) or \
      (op == Operation.DIVIDE and right != 0 and left % right == 0)


def remove_indices(values: List[int], indices: List[int]) -> List[int]:
  new_values = []
  for i in range(len(values)):
    if (indices.count(i) == 0):
      new_values.append(values[i])
  return new_values


def solve(target: int, inputs: List[int]) -> List[Solution]:
  assert len(inputs) > 1

  solutions = []

  def solve(target: int, inputs: List[int], equations: List[Equation]):
    if (inputs.count(target) > 0):
      solutions.append(Solution(equations))
      return

    inputs.sort(reverse=True)
    for i in range(len(inputs)):
      for j in range(i + 1, len(inputs)):
        for op in Operation:
          left = inputs[i]
          right = inputs[j]
          if (possible(left=left, op=op, right=right)):
            equation = Equation(left=left, op=op, right=right)
            new_inputs = remove_indices(inputs, [i, j])
            new_inputs.append(equation.result)
            new_equations = equations.copy()
            new_equations.append(equation)
            solve(target, new_inputs, new_equations)

    return

  solve(target, inputs, [])

  if (len(solutions) == 0):
    return solutions

  deduped_solutions = []
  for solution in solutions:
    if (deduped_solutions.count(solution) == 0):
      deduped_solutions.append(solution)
      
  return deduped_solutions


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Solve a countle.org problem.')
  parser.add_argument('target', type=int, help='Target value.')
  parser.add_argument('inputs', type=int, nargs='+', help='Input values.')
  args = parser.parse_args()
  
  solutions = solve(target=args.target, inputs=args.inputs)
  print(f'{len(solutions)} solution(s) found.\n')
  for solution in solutions:
    print(solution)