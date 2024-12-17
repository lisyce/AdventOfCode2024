import re

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