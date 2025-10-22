import clase
import pickle
import os


def calcular_comision(monto, algoritmo):
    m = monto
    alg = algoritmo
    c = 0

    if alg == 1:
        c = 0.09 * m
    elif alg == 2:
        if m < 50000:
            c = 0
        elif 50000 <= m < 80000:
            c = 0.05 * m
        elif m > 80000:
            c = 0.078 * m
    elif alg == 3:
        c = 100
        if m > 25000:
            c += 0.06 * m
    elif alg == 4:
        if m <= 100000:
            c = 500
        elif m > 100000:
            c = 1000
    elif alg == 5:
        if m < 500000:
            c = 0
        elif m >= 500000:
            c = 0.07 * m
        if c > 50000:
            c = 50000
    return c


def calcular_impuesto(v, base):
    alg_imp = v.algoritmo_impositivo
    imp = 0

    if alg_imp == 1:
        if base <= 300000:
            imp = 0
        if base > 300000:
            imp = 0.25 * (base - 300000)
    elif alg_imp == 2:
        if base < 50000:
            imp = 50
        if base >= 50000:
            imp = 100
    elif alg_imp == 3:
        imp = 0.03 * base
    return imp


def monto_final(v):
    monto = int(v.monto_nominal)
    alg_com = int(v.algoritmo_comision)
    com = calcular_comision(monto, alg_com)
    base = monto - com
    imp = calcular_impuesto(v, base)
    final_origen = base - imp
    final_pago = final_origen * float(v.tasa)
    return final_pago

 
def menu():
    print('1. Cargar envíos')
    print('2. Mostrar listado')
    print('3. Buscar')
    print('4. Mayores')
    print('0. Salir')
    return int(input('Ingrese opción: '))


def add_in_order(v, envio):
    n = len(v)
    izq, der = 0, n - 1
    while izq  <= der:
        c = (izq + der) // 2
        if v[c].identificacion_destinatario == envio.identificacion_destinatario:
            pos = c
            break
        elif  v[c].identificacion_destinatario < envio.identificacion_destinatario:
            der = c - 1
        else:
            izq = c + 1

    if izq > der:
        pos = izq
    v[pos:pos] = [envio]
    return v


def cargar_envios(v):
    # procesar archivo .csv...
    with open('envios.csv', 'r') as f:
        lineas = f.readlines()  # guardar contenido...
    v = []  # vaciar arreglo de envios...
    for linea in lineas:  # recorrer cada envio por separado...
        linea = linea.rstrip("\n")  # elimina el salto de linea al final de cada envio...
        datos = linea.split(",")  # separa los datos por las comas (formato .csv)...

        # porcesar datos del envio...
        cod = datos[0]
        des = datos[1]
        nom = datos[2]
        tas = datos[3]
        mon = datos[4]
        com = datos[5]
        imp = datos[6]

        # generar un objeto/registro envío a partir de los datos obtenidos...
        envio = clase.Envio(cod, des, nom, tas, mon, com, imp)
        # agregar en su lugar correspondiente al nuevo objeto...
        v = add_in_order(v, envio)
    return v


def mostrar(v):
    # solicitar indice del arreglo cargado...
    n = int(input("Ingresar índice: "))

    # obtener identificador de pago del envio con el indice "n"...
    id_pago = v[n].obtener_identificador_pago()
    print("r1.1:", id_pago)
    # verificar impar...
    if n % 2 == 1:
        n = 3 * n + 1  # nuevo indice...
    # verificar par...
    elif n % 2 == 0:
        n = n // 2  # nuevo indice...
    # verificar indice fuera de rango...
    rango = len(v)
    if n <= rango:
        id_pago = v[n].obtener_identificador_pago()
        print("r1.2:", id_pago)
    # mostrar ultimo elemento (fuera de rango)...
    else:
        id_pago = v[-1].obtener_identificador_pago()
        print("r1.2:", id_pago)
        # print("r1.2:", v[-1])


def promedio_comisiones(v):
    c = [0] * 5  # contador de envios por moneda de origen...
    a = [0] * 5  # acumulador de comisiones por moneda de origen...
    for envio in v:
        tipo_moneda = envio.obtener_codigo_moneda_origen()  # tipo de moneda del envio...
        c[tipo_moneda - 1] += 1  # incrementar 1 el contador de este tipo de moneda...
        monto = int(envio.monto_nominal)
        algoritmo = int(envio.algoritmo_comision)
        comision = calcular_comision(monto, algoritmo)
        a[tipo_moneda - 1] += comision  # acumular comision segun tipo moneda...
        # calcular promedio...
    prom = [0] * 5  # arreglo de promedios...
    for i in range(5):
        prom[i] = a[i] / c[i]  # calculo de promedios por cada tipo de moneda...
    return prom


def filtrar_envios(v):
    # promedio de comisiones cobradas...
    prom = promedio_comisiones(v)
    filtrados = []
    for envio in v:
        monto = int(envio.monto_nominal)
        algoritmo = int(envio.algoritmo_comision)
        comision = calcular_comision(monto, algoritmo)
        tipo_moneda = envio.obtener_codigo_moneda_origen()
        if prom[tipo_moneda - 1] < comision:
            filtrados.append(envio)
    return filtrados


def crear_archivo_binario(fd, v):
    """  ==> PARTE 1 <==
        Crear un archivo binario que contenga todos aquellos envíos del vector cuya comisión supere 
        al promedio de comisiones cobradas para su moneda de origen. """
    envios_filtrados = filtrar_envios(v)
    m = open(fd, "wb")  # crear archivo...
    if envios_filtrados:
        pickle.dump(envios_filtrados, m)  # alamcenar dentro del archivo binario...


def mostrar_archivo_binario(fd):
    flag = os.path.exists(fd)
    # verificar si existe el archivo...
    if not flag:
        print("El archivo no fue cargado.")
        return
    
    m = open(fd, "rb")
    tam = os.path.getsize(fd)
        # verificar que termino de comparar... 
    while m.tell() < tam:
        envios = pickle.load(m)  # mostrar archivo...

    for envio in envios:
            print(envio.__str__())
    m.close()


def buscar(v):
    id = input("Ingrese identificación del destinatario a buscar: ")
    n = len(v)
    izq, der = 0, n - 1
    encontrado = False

    while izq <= der:
        c = (izq + der) // 2
        if v[c].identificacion_destinatario == id:
            encontrado = True
            pos = c
            break
        elif v[c].identificacion_destinatario < id:
            der = c - 1   # porque está ordenado en forma descendente
        else:
            izq = c + 1

    if encontrado:
        # Convertimos a float por si viene como string
        monto_original = int(v[pos].monto_nominal)
        print("Monto nominal antes de la modificacion:", monto_original)

        # Aumentamos un 17%
        nuevo_monto = monto_original * 1.17

        # Redondeamos a la centena más próxima
        nuevo_monto = round(nuevo_monto / 100) * 100

        v[pos].monto_nominal = int(nuevo_monto)
        print("Monto nominal actualizado:", v[pos].monto_nominal)
    else:
        print("No se encontro el envio buscado: 0")
        print("No se encontro el envio buscado: 0")


def mayores(v):
    """Almacenar en una matriz el Envío con mayor monto final, para cada combinación posible de 
    moneda origen / moneda de pago.
    r.4.1: Mostrar para cada combinación posible el código (y solo el código) del envío 
    almacenado en cada casillero. """
    # matriz combinaciones posibles moneda origen-pago...
    m = [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
    ]
    # 1 - determinar mayor monto final para cada combinacion...
    final_mayor = 25 * [0]  # venctor de acumulacion de montos finales...
    for envio in v:  # recorres los envios...
        identificador_pago = envio.obtener_identificador_pago()
        final_envio = monto_final(envio)
        moneda_origen = envio.obtener_codigo_moneda_origen()
        moneda_destino = envio.obtener_codigo_moneda_destino()

        for i in range(5):  # filas...
            for j in range(5):  # columnas...
                if moneda_origen == i + 1:  # moneda origen n == fila moneda de origen n... 
                    if moneda_destino == j + 1:  # moneda destino n == columna moneda destino n...
                        if final_mayor[i + j] < final_envio:  # si monto final de esa fila y columna < monto final del envio...
                            final_mayor[i + j] = final_envio
                if final_mayor[i + j] == final_envio:
                    m[i][j] = identificador_pago
    for i in range(5):
        for j in range(5):
            if final_mayor[i + j] > 0:
                print(final_mayor[i + j], m[i][j])









    # 2 - alamacenar CODIGO de envio con mayor monto fianl...
    # 3 - mostrar codigo para cada combinacion posible...


def principal():
    v = []  # inicializar arreglo...
    fd = "archivos.dat"
    op = -1  # forzar primera vuelta...
    while op != 0:
        op = menu()  # menu de control del programa...
        if op == 1:  # opcion 1 (Cargar Envios)...
            """  ==> PARTE 1 <==
            Debe importar los envíos del archivo “envíos.csv” (que es exactamente el mismo que el usado 
            en el TP3) y agregarlos a un vector, de tal manera que el vector se mantenga siempre 
            ordenado por identificación del destinatario, de forma descendente. """
            v = cargar_envios(v)

            """  ==> PARTE 2 <==
            Cuando haya terminado de cargar el arreglo, y antes de salir de la opción 1 del menú, debe 
            solicitar al usuario que ingrese por teclado un valor i que hace referencia a un índice del 
            arreglo que se ha cargado. Y con estos elementos, mostrar las siguientes salidas: """
            mostrar(v)

        elif op == 2:  # opcion 2 (Generar Archivo)...
            """  ==> PARTE 1 <==
            Crear un archivo binario que contenga todos aquellos envíos del vector cuya comisión supere 
            al promedio de comisiones cobradas para su moneda de origen. """
            crear_archivo_binario(fd, v)
            mostrar_archivo_binario(fd)
        
        elif op == 3:  # opcion 3 (Buscar Envio)...
            buscar(v)

        elif op == 4:  # opcion 4 (Mayores por Combinacion de Moneda)...
            mayores(v)


if __name__ == "__main__":
    principal()
