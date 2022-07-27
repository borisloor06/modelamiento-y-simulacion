from flask import Flask, request
from flask.templating import render_template
from calc.Aleatorio import Aleatorio
from calc.Estadistica import Estadistica
from calc.Pronostico import Pronostico
from calc.Simulacion import Simulacion

est = Estadistica()
aleatorio = Aleatorio()
pronostico = Pronostico()
simulacion = Simulacion()

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/proyectoDatos')
def proyectoDatos():
    return render_template('proyectoDatos.html',
        data=est.datos())

@app.route('/proyectoAnalisis')
def proyectoAnalisis():
    return render_template('proyectoAnalisis.html',
        imagen1 = est.graficoComprasPorGenero(),
        imagen2 = est.graficoFrecuenciaVentas(),
        imagen3 = est.graficaPreciosPorMesySucursal(),
        imagen4 = est.graficaMetodoPago()
        )

@app.route('/cuadradosMedios', methods=['POST', 'GET'])
def cuadradosMedio():
    if request.method == 'POST':
        try:
            data = aleatorio.cuadradosMedios(
                int(request.form['n']),
                int(request.form['r']))

            return render_template('cuadradosMedios.html',
                datos = data[0],
                imagen1 = data[1])
        except Exception as error:
            return render_template('cuadradosMedios.html',
                error=error
            )
    elif request.method == 'GET':
        return render_template('cuadradosMedios.html')

@app.route('/congruenciaLineal', methods=['POST', 'GET'])
def congruenciaLineal():
    if request.method == 'POST':
        try:
            data = aleatorio.congruencialLineal(
                int(request.form['n']),
                int(request.form['x']),
                int(request.form['a']),
                int(request.form['c']),
                int(request.form['m']))

            return render_template('congruenciaLineal.html',
                datos = data[0],
                imagen = data[1])
        except Exception as error:
            return render_template('congruenciaLineal.html',
                error = error)

    elif request.method == 'GET':
        return render_template('congruenciaLineal.html')

@app.route('/congruencialMultiplicativo', methods=['POST', 'GET'])
def congruencialMultiplicativo():
    if request.method == 'POST':
        try:
            data = aleatorio.congruencialMultiplicativo(
                int(request.form['n']),
                int(request.form['x']),
                int(request.form['a']),
                int(request.form['m']))

            return render_template('congruencialMultiplicativo.html',
                datos = data[0],
                imagen = data[1])
        except Exception as error:
            return render_template('congruencialMultiplicativo.html',
                error = error)

    elif request.method == 'GET':
        return render_template('congruencialMultiplicativo.html')


@app.route('/distribucionPoisson', methods=['POST', 'GET'])
def distribucionPoisson():
    if request.method == 'POST':
        try:
            data = aleatorio.distribucionPoisson(
                int(request.form['landa']))

            return render_template('distribucionPoisson.html',
                imagen = data)
        except Exception as error:
            return render_template('distribucionPoisson.html',
                error = error)

    elif request.method == 'GET':
        return render_template('distribucionPoisson.html')

@app.route('/promedioMovil', methods=['POST', 'GET'])
def promedioMovil():
    if request.method == 'POST':
        try:
            data = pronostico.promedioMovil(
                request.form['x'],
                request.form['y'],
                request.form['xlbl'],
                request.form['ylbl'])

            return render_template('promedioMovil.html',
                datos = data[0],
                imagen = data[1],
                mediaMovil3 = data[5],
                mediaMovil4 = data[6])
        except Exception as error:
            return render_template('promedioMovil.html',
                error = error)

    elif request.method == 'GET':
        return render_template('promedioMovil.html')


@app.route('/suavizacionExponencial', methods=['POST', 'GET'])
def suavizacionExponencial():
    if request.method == 'POST':
        try:
            data = pronostico.suavizacionExponencial(
                request.form['x'],
                request.form['y'],
                request.form['xlbl'],
                request.form['ylbl'])

            return render_template('suavizacionExponencial.html',
                datos = data[0],
                imagen= data[1],
                cargar = True)
        except Exception as error:
            return render_template('suavizacionExponencial.html',
                error = error)

    elif request.method == 'GET':
        return render_template('suavizacionExponencial.html')

@app.route('/regresionLineal', methods=['POST', 'GET'])
def regresionLineal():
    if request.method == 'POST':
        try:
            data = pronostico.regresionLineal(
                request.form['x'],
                request.form['y'],
                request.form['xlbl'],
                request.form['ylbl'])

            return render_template('regresionLineal.html',
                imagen = data)
        except Exception as error:
            return render_template('regresionLineal.html',
                error = error)

    elif request.method == 'GET':
        return render_template('regresionLineal.html')

@app.route('/regresionCuadratica', methods=['POST', 'GET'])
def regresionCuadratica():
    if request.method == 'POST':
        try:
            data = pronostico.regresionLinealCuadratica(
                request.form['x'],
                request.form['y'],
                request.form['xlbl'],
                request.form['ylbl'])

            return render_template('regresionCuadratica.html',
                imagen = data)
        except Exception as error:
            return render_template('regresionCuadratica.html',
                error = error)

    elif request.method == 'GET':
        return render_template('regresionCuadratica.html')

@app.route('/inventario', methods=['GET'])
def inventario():
    data = simulacion.modeloInventario()
    return render_template('inventario.html',
        datos=data['datos'],
        df = data['df'],
        imagen = data['img_url'])

@app.route('/banco', methods=['GET'])
def banco():
    data = simulacion.banco()
    return render_template('banco.html',
        df = data['df'],
        imagen = data['img_url'])

@app.route('/sistemaMontecarlo')
def sistemaMontecarlo():
    return render_template('sistemaMontecarlo.html')

@app.route('/printSistemaMontecarlo')
def printSistemaMontecarlo():
    return render_template('printSistemaMontecarlo.html')

@app.route('/calcularMontecarlo', methods=['GET', 'POST'])
def calcularMontecarlo():
    tipoArch= request.form.get("tipoarchivo")
    n1 = request.form.get("numeroIteraciones", type=int)

    pago = request.form.get("x")
    probabilidad = request.form.get("y")

    file = request.files['file'].read()

    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    from pandas import ExcelWriter
    from matplotlib import pyplot as plt
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    from matplotlib.figure import Figure
    import io
    from io import BytesIO
    import base64
    import itertools
    import pandas as pd


    if tipoArch=='1':
        file = pd.read_excel(file)
    elif tipoArch=='2':
        file = pd.read_csv(io.StringIO(file.decode('utf-8')))
    elif tipoArch=='3':
        file = pd.read_json(file)


    df = pd.DataFrame(file)
    # Suma de probabilidad
    sumProbabilidad = np.cumsum(df[probabilidad])
    df['FDP'] = sumProbabilidad
    # Obtenemos los datos mínimos
    datosMin = df['FDP']+0.001
    # Obtenemos los datos máximos
    datosMax = df['FDP']
    # Asignamos al DataFrame
    df['Min'] = datosMin
    df['Max'] = datosMax
    # Se establecen correctamente los datos mínimos
    df['Min'] = df['Min'].shift(periods=1, fill_value=0)
    #Generamos números aleatorios
    n = n1
    r=[0.1]*n
    for i in range(1, n):
        r[i]=np.random.rand()
    d = {'ri': r }
    dfMCL = pd.DataFrame(data=d)
    # Valores máximos
    max = df['Max'].values
    # Valores mínimos
    min = df['Min'].values
    # Definimos el número de pagos
    # Función de búsqueda
    def busqueda(arrmin, arrmax, valor):
        for i in range (len(arrmin)):
            if valor >= arrmin[i] and valor <= arrmax[i]:
                return i
        return -1
    xpos = dfMCL['ri']
    posi = [0] * n
    for j in range(n):
        val = xpos[j]
        pos = busqueda(min,max,val)
        posi[j] = pos
    # Definiendo un índice para simular datos
    num = [0]*len(df.index.values)
    for i in range(len(num)):
        num[i] = i+1
    df['index']=num
    df.set_index('index')
    # Array para guardar los datos
    simula = []
    for j in range(n):
        for i in range(n):
            sim = df.loc[df["index"]== posi[i]+1 ]
            simu = sim.filter([pago]).values
            iterator = itertools.chain(*simu)
            for item in iterator:
                a=item
                simula.append(round(a,2))
    dfMCL["Simulación"] = pd.DataFrame(simula)
    dfMCL["Ganancia"] = dfMCL["Simulación"]*0.3
    data = dfMCL['Ganancia'].sum()

    buf = io.BytesIO()
    plt.plot(dfMCL['Simulación'], label='Simulación', color='purple')
    plt.plot(dfMCL['Ganancia'], label='Ganancia', color='green')
    plt.legend()

    fig = plt.gcf()
    canvas = FigureCanvasAgg(fig)
    canvas.print_png(buf)
    fig.clear()
    plot_url = base64.b64encode(buf.getvalue()).decode('UTF-8')

    data1 = df.to_html(
        classes="dataTable table table-bordered table-hover", justify="justify-all", border=0)

    data2 = dfMCL.to_html(
        classes="dataTable table table-bordered table-hover", justify="justify-all", border=0)

    return render_template('printSistemaMontecarlo.html', data=data1, data2=data2,data3=data, image=plot_url)


if __name__ == '__main__':
    app.run( host="0.0.0.0", port=3000,debug=True)
