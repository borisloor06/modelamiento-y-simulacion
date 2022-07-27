import matplotlib.pyplot as plt
import pandas as pd
import io
import base64
import seaborn as sbn

class Estadistica:
    """
    Clase estadistica que se encarga de realizar diferentes
    calculos estadisticos sobre el proyecto de ventas
    """
    def __init__(self):
        self.df = pd.read_csv('info/supermarket.csv')
        # self.recombrarDistritos()
        # self.recombrarPaises()
        #Transformación del tipo de dato de Fecha
        self.df['Date'] = pd.to_datetime(self.df['Date'])
        #Extración unicamente del mes
        self.df['mes'] = self.df['Date'].dt.month
        #Mejora en la presentación de la información
        self.df['mes'] = self.df['mes'].map({1: 'enero',
                                        2: 'febrero',
                                        3: 'marzo'})

    def datos(self):
        """
        funcion que retorna el dataframe con los datos
        """
        return self.df

    def graficoComprasPorGenero(self):
        """
        Funcion que retorna la grafica referente la distribucion de hombres y mujeres que realizan compras
        """
        img = io.BytesIO()

        plt.figure(figsize=(5,5))
        self.df["Gender"].value_counts().plot(kind="pie", colors=['pink', 'lightblue'], autopct="%1.1f%%")
        plt.legend()
        plt.title('Distribución de compras por género', fontsize=18)
        plt.savefig(img, format='png')
        img.seek(0)

        img_url = base64.b64encode(img.getvalue()).decode()
        return img_url

    def graficoFrecuenciaVentas(self):
        """
        Funcion que retorna la grafica de la frecuencia de las ventas
        """
        self.df["gross_group"] = pd.cut(self.df["Total"], bins=20)
        lis = (self.df
        .groupby("gross_group")
        .agg(fi=("gross income", "count")))
        dfclases=pd.DataFrame(lis)
        total = dfclases.sum(axis=0) 
        datahi = dfclases["fi"]/total["fi"]           # aqui calculamos la frecuencia 
        datahi.values
        # agregamos nueva columna de frecuencia relativa 
        dfclases["hi"] = datahi
        FA = dfclases["fi"].values
        # obtenemos FA
        a=[]
        b=0
        for c in FA:
            b = c + b
            a.append(b)
        dfclases["FA"] = a 
        HI = dfclases["hi"].values
        # obtenemos HI
        a=[]
        b=0
        for c in HI:
            b = c + b
            a.append(b)
        dfclases["HI"] = a
        lt = dfclases.index.values.tolist()

        intervalos = []
        i = 0
        for n in lt:
            intervalos.append(str(n))

        #Gráfica frecuencia observada  
        img = io.BytesIO()

        plt.figure(figsize=(36,16))
        plt.title('Gráfica de Frecuencia Observada', fontsize=28)
        plt.bar(intervalos, dfclases['fi'],  color="brown", ec="black")
        plt.axis()
        plt.xlabel('Ventas', fontsize=28)
        plt.ylabel('Frecuencia Observada', fontsize=28)
        plt.savefig(img, format='png')
        img.seek(0)

        img_url = base64.b64encode(img.getvalue()).decode()
        return img_url

    def graficaPreciosPorMesySucursal(self):
        #definicion de variables para realizar gráficas por sucursal y mes
        porcion = self.df.groupby(['City', 'mes'])

        t1 = porcion["gross income"].sum()
        arr1 = t1.index.get_level_values(level=0).values
        arr2 = t1.index.get_level_values(level=1).values
        x = arr1 + '-' + arr2

        img = io.BytesIO()
        plt.figure(figsize=(16,8))
        plt.title('Ingreso bruto por mes y sucursal', fontsize=28)
        plt.plot(x, t1, marker='o', color='blue')
        plt.xlabel('Ciudad de la Sucursal y Mes')
        plt.ylabel('Precios') 
        plt.legend(('Ingresos', ), prop = {'size':12
        },loc='upper right')
        plt.savefig(img, format='png')
        img.seek(0)

        img_url = base64.b64encode(img.getvalue()).decode()
        return img_url

    def graficaMetodoPago(self):
        # Métodos de pago
        paym_branch = self.df.groupby(['Branch', 'Payment']).size().reset_index(name='Counts')
        img = io.BytesIO()
        plt.figure(figsize=(16, 8))
        plt.title('Método de Pago preferido por Sucursal')
        sbn.barplot(x="Branch", y="Counts", hue="Payment", data=paym_branch, ci=None, palette="GnBu")
        plt.xlabel('Sucursal')
        plt.ylabel('Frecuencia')
        plt.savefig(img, format='png')
        img.seek(0)
        img_url = base64.b64encode(img.getvalue()).decode()
        return img_url
