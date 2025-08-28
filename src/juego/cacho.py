import dado

class cacho:
   def __init__(self):
      self.dados = []
      self.dados_extra = 0
      for i in range(5):
         self.dados.append(dado.dado())

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
      return self.dados

   def agregar_dado(self):
      if len(self.dados) < 5:         
         dadonuevo = dado.dado()
         self.dados.append(dadonuevo)
         return self.dados
      self.dados_extra += 1
      return self.dados