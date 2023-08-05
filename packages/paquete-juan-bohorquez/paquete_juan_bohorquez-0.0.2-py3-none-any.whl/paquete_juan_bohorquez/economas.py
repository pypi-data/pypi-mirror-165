class Paquete:
  def __init__(self, x: list):
    self.__x= x 
    self.media = sum(self.__x)/len(self.__x)
    
  def mediana(self):
    m = sorted(self.__x)
    if len(self.__x) %2 != 0:
      print(self.__x[(len(m)//2)])
    else:
      print((self.__x[(len(m)//2)-1] + self.__x[(len(m)//2)])/2)
  def moda(self):
    diccionario= {}
    for numero in self.__x:
      clave = str(numero)
      if not clave in diccionario:
        diccionario[clave] = 1
      else:
        diccionario[clave] += 1
      frecuencia_mayor = 0
    numero_repetido = self.__x[0]
    #print(diccionario)
    r = max(diccionario.values())
    moda = [key for key, value in diccionario.items() if value == r] 
    if r == 1:
      print(self.__x)
    if r > 1:
      print(f'{moda} repetido {r} veces')
  def varianza(self):
    c=[]
    for i in self.__x:
      c.append((i-self.media)**2)
      d=sum(c)
      e= d/(len(self.__x)-1)
    print(e)
  def desviacion(self):
    c=[]
    for i in self.__x:
      c.append((i-self.media)**2)
      d=sum(c)
      e= d/(len(self.__x))
      e_2 = e**(1/2)
    print(e_2)
  def coeficiente_var(self):
    c=[]
    for i in self.__x:
      c.append((i-self.media)**2)
      d=sum(c)
      e= (d/(len(self.__x)))**(1/2)
    print(e/abs(self.media)) 
  def curtosis(self):
    ku = []
    for i in self.__x:
      ku.append((i-self.media)**4)
      sum_ku = sum(ku)
      c=[]
      for i in self.__x:
        c.append((i-self.media)**2)
        d=sum(c)
        e= d/(len(self.__x))
        e_2 = e**(1/2)
    print(sum_ku/(len(self.__x)*(e_2)**4)-3)
  def simetria(self):
    si = []
    for i in self.__x:
      si.append((i-self.media)**3)
      sum_si = sum(si)
      c=[]
      for i in self.__x:
        c.append((i-self.media)**2)
        d=sum(c)
        e= d/(len(self.__x))
        e_2 = e**(1/2)
    print(sum_si/(len(self.__x)*(e_2)**3))