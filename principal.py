import clase


def calcular_comision(envio):
    m = envio.monto
    alg = envio.comision
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


def calcular_impuesto(envio, base):
    alg = envio.impositivo
    imp = 0

    if alg == 1:
        if base <= 300000:
            imp = 0
        if base > 300000:
            imp = 0.25 * (base - 300000)
    elif alg == 2:
        if base < 50000:
            imp = 50
        if base >= 50000:
            imp = 100
    elif alg == 3:
        imp = 0.03 * base
    return imp


def monto_final(envio):
    com = calcular_comision(envio)
    base = envio.monto - com
    imp = calcular_impuesto(envio, base)
    final_origen = base - imp
    final_pago = final_origen * envio.tasa
    return com, imp, final_pago

 
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


def principal():
    v = []  # inicializar arreglo...
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
            pass
        
        elif op == 3:  # opcion 3 (Buscar Envio)...
            pass

        elif op == 4:  # opcion 4 (Mayores por Combinacion de Moneda)...
            pass


if __name__ == "__main__":
    principal()
