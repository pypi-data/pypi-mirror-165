class Estadisticos:
  def __init__(self,x:list):
        self.x=x
        self.n=len(self.x)
        self.c=self.x.count
  def media(self)-> list:
    """Muestra la media aritmetica de un conjunto de datos numericos
    """
    return sum(self.x)/len(self.x)
  def mediana(self)-> list:

    """Muestra la mediana (valor medio) de un conjunto de datos numericos
      Cuando el numero de datos es impar, muestra el valor medio
      Cuando el numero de datos es par, se muestra la media entre los dos datos que se encuantran en la mitad del conjunto numerico
    """

    mitad= len(self.x)//2
    self.x.sort()
    if not len(self.x) % 2:
      return (self.x[mitad -1]+ self.x[mitad])/2.0
    return self.x[mitad]
  def moda(self)-> list:
    """Muestra el/los datos que mas se repiten dentro del conjunto de datos
    """
    y=[]
    con = 0
    for num in self.x:
      if self.x.count(num) > con:
          y=[]
          y.append(num)
          con = self.x.count(num)
      elif self.x.count(num)==con:
          if not num in y:
                y.append(num)
                con = self.x.count(num)
    return y
  def varianza(self)-> list:
    """Muestra la varianza muestral del conjunto de datos numericos
    """

    y=[]
    for i in self.x:
      y.append((i-(sum(self.x)/len(self.x)))**2)
    return (sum(y))/(len(self.x)-1)
  def desviacion(self)-> list:
    """Muestra la desviacion estandar del conjunto de datos numericos
    """
    return (self.varianza()** 0.5)
  def coeficiente_var(self)-> list:
    """Muestra el coeficiente de variacion del conjunto de datos numericos
    """
    return self.desviacion()/ abs(self.media())
  def curtosis(self)-> list:
    """Muestra la curtosis del conjunto de datos numericos
    """
    y=[]
    for i in self.x:
      y.append(((i)-(sum(self.x)/len(self.x)))**4)
    return (sum(y)/((self.n)*(self.desviacion()**4)))
  def simetria(self)-> list:
    """Muestra el grado de simetria que presenta el conjunto de datos numericos
    """
    y=[]
    for i in self.x:
      y.append(((i)-(sum(self.x)/len(self.x)))**3)
    return (sum(y)/((self.n)*(self.desviacion()**3)))