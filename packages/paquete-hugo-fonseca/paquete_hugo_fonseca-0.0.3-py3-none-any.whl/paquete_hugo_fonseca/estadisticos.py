class Estadisticos_descriptivos:
    def __init__(self,vec):
        self.__vec = vec

    def media(self):
        '''Calcula la media de un Vector'''
        return sum(self.__vec)/len(self.__vec)

    def mediana(self):
        '''Calcula la mediana de un vector'''
        if len(self.__vec)%2 !=0:
            return (sorted(self.__vec)[len(self.__vec)//2])
        else:
            return (sorted(self.__vec)[len(self.__vec)//2-1]+sorted(self.__vec)[len(self.__vec)//2]) / 2

    def moda(self):
        '''Calcula la moda de un vector'''
        s = list(set(self.__vec)) # un set con los valores unicos del vector
        llaves = []
        for x in s:
            llaves.append((x,self.__vec.count(x)))
        frecuencias = [j for i,j in llaves] 
        return llaves[frecuencias.index(max(frecuencias))][0]

    def varianza(self): 
        '''Caclula la varianza de un vector'''   
        return (sum([(x - self.media())**2 for x in self.__vec])/(len(self.__vec)-1))
    
    def desviacion(self):
        '''Calcula la desviacion estandar de un vector'''
        return self.varianza()**0.5

    def coeficiente_variacion(self):
        '''Calcula el coeficiente de variacion de un vector'''
        return self.desviacion()/abs(self.media())

    def simetria(self):
        '''Calcula la simetria de un vector'''
        return sum([(x-self.media())**3 for x in self.__vec])/(len(self.__vec)*self.coeficiente_variacion()**3)

    def curtosis(self):
        '''Calcula la curtosis de un vector'''
        return sum([(x-self.media())**4 for x in self.__vec])/(len(self.__vec)*self.coeficiente_variacion()**4)







