import re
from z3 import *

class Computer:
  def __init__(self, fp):
    lA = fp.readline()
    lB = fp.readline()
    lC = fp.readline()

    self.A = int(lA.split()[-1])
    self.B = int(lB.split()[-1])
    self.C = int(lC.split()[-1])
    self.ip = 0

    fp.readline()

    program = re.findall(r"\d+", fp.readline())
    program = [int(n) for n in program]
    self.expanded_program = program
    
    self.program = []
    for i in range(len(program) // 2):
      self.program.append((program[i * 2], program[i * 2 + 1]))

    self.opcode_map = [self._adv, self._bxl, self._bst, self._jnz, self._bxc, self._out, self._bdv, self._cdv]
    self.has_outputted = False

  def run(self):
    while self.ip < len(self.program):
      opcode, operand = self.program[self.ip]
      self.opcode_map[opcode](operand)
      self.ip += 1
    print()

  # ONLY WORKS ON MY PERSONAL INPUT
  def solve(self):
    s = Solver()

    A_0 = BitVec('A_0', 64)
    B_0 = BitVec('B_0', 64)
    C_0 = BitVec("C_0", 64)
    As = [A_0]
    Bs = [B_0]
    Cs = [C_0]

    s.add(B_0 == 0)
    s.add(C_0 == 0)
    s.add(A_0 > 0)

    for i in range(1, 17):
      # A
      A_prev = As[-1]
      A_i = BitVec(f'A_{i}', 64)
      s.add(A_i == A_prev >> 3)
      if i <= 15:
        s.add(A_i != 0)
      else:
        s.add(A_i == 0)

      As.append(A_i)

      # C
      C_i = BitVec(f"C_{i}", 64)
      s.add(C_i == A_prev >> (1 << ((A_prev % 8) ^ 7)))
      Cs.append(C_i)

      # B
      B_i = BitVec(f"B_{i}", 64)
      s.add(B_i == (((A_prev % 8) ^ 7) ^ C_i) ^ 7)
      s.add(B_i % 8 == self.expanded_program[i-1])
      Bs.append(B_i)

    for c in s.assertions():
      print(c)
    
    if s.check() == sat:
      m = s.model()
      return m[A_0]
    else:
      raise Exception("Unsatisfiable")

  def solve_test(self):
    s = Solver()

    A_0 = BitVec('A_0', 64)
    B_0 = BitVec('B_0', 64)
    C_0 = BitVec("C_0", 64)
    As = [A_0]
    s.add(B_0 == 0)
    s.add(C_0 == 0)
    for i in range(1, 7):
      A_i = BitVec(f'A_{i}', 64)
      s.add(A_i == As[-1] >> 3)
      s.add(A_i % 8 == self.expanded_program[i-1])
      As.append(A_i)
      if i <= 5:
        s.add(A_i != 0)
      else:
        s.add(A_i == 0)

    # for c in s.assertions():
    #   print(c)
    
    if s.check() == sat:
      m = s.model()
      return m[A_0]
    else:
      raise Exception("Unsatisfiable")


  def _combo_operand(self, operand):
    if operand <= 3:
      return operand
    elif operand == 4:
      return self.A
    elif operand == 5:
      return self.B
    elif operand == 6:
      return self.C
    else:
      raise Exception("Invalid combo operand")
    
  # OPERATIONS
  def _adv(self, operand):
    combo_operand = self._combo_operand(operand)
    denom = 2 ** combo_operand
    self.A //= denom
  
  def _bxl(self, operand):
    self.B = self.B ^ operand

  def _bst(self, operand):
    self.B = self._combo_operand(operand) % 8

  def _jnz(self, operand):
    if self.A == 0:
      return
    
    self.ip = operand - 1  # since we don't advance after this

  def _bxc(self, _):
    self.B = self.B ^ self.C

  def _out(self, operand):
    if self.has_outputted:
      print(",", end="")
    operand = self._combo_operand(operand)
    print(operand % 8, end="")
    self.has_outputted = True

  def _bdv(self, operand):
    combo_operand = self._combo_operand(operand)
    denom = 2 ** combo_operand
    self.B = self.A // denom

  def _cdv(self, operand):
    combo_operand = self._combo_operand(operand)
    denom = 2 ** combo_operand
    self.C = self.A // denom