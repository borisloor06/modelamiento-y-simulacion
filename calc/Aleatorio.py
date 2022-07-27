import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy.stats as stats
import io
import base64

class Aleatorio:
    """
    Clase que manejo diferentes metodos aletorios
    """

    def cuadradosMedios(self, n: int, r: int):
        """
        Metodo de los cuadrados medios
        parametros:
            n -> Cantidad de numeros a generar
            r -> Semilla
        retorna:
            tupla con la grafica y la tabla
        """
        l=len(str(r)) # determinamos el número de dígitos 
        lista = [] # almacenamos en una lista
        lista2 = []
        i=1
        
        while i < n:
            x=str(r*r) # Elevamos al cuadrado r
            if l % 2 == 0: 
                x = x.zfill(l*2)
            else:
                x = x.zfill(l)
            y=(len(x)-l)/2
            y=int(y)
            r=int(x[y:y+l])
            lista.append(r)
            lista2.append(x)
            i=i+1
            
        df = pd.DataFrame({'X2':lista2,'Xi':lista})
        dfrac = df["Xi"]/10**l
        df["ri"] = dfrac
        
        ## Graficando los numeros aleatorios generados
        # seleccionamos del dataframe los nùmeros generados
        img = io.BytesIO()
        x1=df['ri']
        plt.figure(figsize=(10,5))
        plt.plot(x1, marker='o')
        plt.title('Generador de Numeros Aleatorios Cuadrados Medios')
        plt.xlabel('Serie')
        plt.ylabel('Aleatorios')
        plt.savefig(img, format='png')
        plt.clf()
        img.seek(0)
        
        img_url = base64.b64encode(img.getvalue()).decode()        

        return (df, img_url)

    def congruencialLineal(self, n, x0, a, c, m):
        """
        Metodo que calcula la congruencia lineal

        """
        # Validar el ingreso de numero positivos
        if(n<=0 or x0<=0 or a<=0 or c <= 0 or m<=0):
            raise Exception('Solo puede ingresar valores positivos!')
        x = [1] * n
        r = [0.1] * n
        for i in range(0, n):
            x[i] = ((a*x0)+c) % m
            x0 = x[i]
            r[i] = x0 / m
        # llenamos nuestro DataFrame 
        d = {'Xn': x, 'ri': r }
        df = pd.DataFrame(data=d)

        # Grafica
        img = io.BytesIO()
        plt.figure(figsize=(10,5))
        plt.plot(r,marker='o')
        plt.title('Generador de Numeros Aleatorios ')
        plt.xlabel('Serie')
        plt.ylabel('Aleatorios')
        plt.savefig(img, format='png')
        plt.clf()
        img.seek(0)

        img_url = base64.b64encode(img.getvalue()).decode()
        
        return (df, img_url)

    def congruencialMultiplicativo(self, n, x0, a, m):
        """
        Metodo congruencial multiplicativo
        """
         # Validar el ingreso de numero positivos
        if(n<=0 or x0<=0 or a<=0 or m<=0):
            raise Exception('Solo puede ingresar valores positivos!')
        
        x = [1] * n
        r = [0.1] * n
        print (" Generador Congruencial multiplicativo")
        print ("--------------------------------------")
        for i in range(0, n):
            x[i] = (a*x0) % m
            x0 = x[i]
            r[i] = x0 / m
        d = {'Xn': x, 'ri': r }
        df = pd.DataFrame(data=d)
        
        # Grafica
        img = io.BytesIO()
        plt.plot(r,'g-', marker='o',)
        plt.title('Generador de Numeros Aleatorios ')
        plt.xlabel('Serie')
        plt.ylabel('Aleatorios')
        plt.savefig(img, format='png')
        plt.clf()
        img.seek(0)

        img_url = base64.b64encode(img.getvalue()).decode()
        
        return (df, img_url)

    def transformadaInversa(self):
        None

    def distribucionPoisson(self, landa):
        """
        Distribucion de Poisson
        """
        poisson = stats.poisson(landa) 
        x = np.arange(poisson.ppf(0.01), poisson.ppf(0.99))
        fmp = poisson.pmf(x)
        img = io.BytesIO()
        plt.plot(x,fmp,'--')
        plt.vlines(x,0,fmp,colors='b',lw=5,alpha=0.5)
        plt.title('Distribución de Poisson')
        plt.ylabel('Probabilidad')
        plt.xlabel('Valores')
        plt.savefig(img, format='png')
        plt.clf()
        img.seek(0)

        img_url = base64.b64encode(img.getvalue()).decode()

        return img_url
