
def media(vec):
    '''Calcula la media de un Vector'''
    return sum(vec)/len(vec)

def mediana(vec):
    if len(vec)%2 !=0:
        return (sorted(vec)[len(vec)//2])
    else:
        return (sorted(vec)[len(vec)//2-1]+sorted(vec)[len(vec)//2]) / 2

def moda(vec):
  s = list(set(vec)) # un set con los valores unicos del vector
  llaves = []
  for x in s:
    llaves.append((x,vec.count(x)))
  frecuencias = [j for i,j in llaves] 
  return llaves[frecuencias.index(max(frecuencias))][0]

def varianza(vec): 
    '''Caclula la varianza de un vector'''   
    return (sum([(x - media(vec))**2 for x in vec])/(len(vec)-1))

def desviacion(vec):
    '''Calcula la desviacion estandar de un vector'''
    return varianza(vec)**0.5

def coeficiente_variacion(vec):
    '''Calcula el coeficiente de variacion de un vector'''
    return desviacion(vec)/abs(media(vec))

def simetria(vec):
    '''Calcula la simetria de un vector'''
    return sum([(x-media(vec))**3 for x in vec])/(len(vec)*coeficiente_variacion(vec)**3)

def curtosis(vec):
    '''Calcula la curtosis de un vector'''
    return sum([(x-media(vec))**4 for x in vec])/(len(vec)*coeficiente_variacion(vec)**4)






