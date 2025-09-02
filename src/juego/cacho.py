from src.juego.dado import *

class cacho:   
   def __init__(self):
      self.dados = []
      self.dados_extra = 0
      self.nombre = ""
      self.primer_unico_dado = False
      self.llego_a_unico_dado = False

      for i in range(5):
         self.dados.append(dado())

   def tirar_dados(self):
      for i in range(len(self.dados)):
         self.dados[i].tirar()
      return self.dados

   def ver_dados(self):
      dados_num = []
      for i in range(len(self.dados)):
         dados_num.append(self.dados[i].ver())
      return dados_num
   
   def sacar_dado(self):
      self.dados.pop()

      if self.get_cantidad() == 1 and not self.llego_a_unico_dado:
        self.primer_unico_dado = True
        self.llego_a_unico_dado = True
      return self.dados

   def agregar_dado(self):
      if len(self.dados) < 5:         
         dadonuevo = dado()
         self.dados.append(dadonuevo)
         return self.dados
      self.dados_extra += 1
      return self.dados
   
   def get_nombre(self):
      return self.nombre

   def set_nombre(self, nombre):
      self.nombre = nombre

   def get_cantidad(self):
      return len(self.dados)

   def get_dados_extra(self):
      return self.dados_extra
    