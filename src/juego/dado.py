import random

class dado:
   def __init__(self):
      self.numero = None
   
   def tirar(self):
      self.numero = random.randint(1,6)
      return self.numero
   
   def ver(self):
      return self.numero