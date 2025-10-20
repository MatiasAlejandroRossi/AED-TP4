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
    print('1) Cargar Envíos')
    print('2) Mostrar Resultados')
    print('0) Salir')
    print()
    return int(input('Ingrese opción: '))

def principal():
    envios = []
    op = -1
    while op != 0:
        op = menu()
        if op == 1:
            with open('envios.csv', 'r') as f:
                lineas = f.readlines()
            envios = []
            c1 = 0
            c2 = 0
            for linea in lineas:
                linea = linea.rstrip("\n")
                datos = linea.split(",")
                cod = datos[0]
                des = datos[1]
                nom = datos[2]
                tas = datos[3]
                mon = datos[4]
                com = datos[5]
                imp = datos[6]
                envio = clase.Envio(cod, des, nom, tas, mon, com, imp)
                envios.append(envio)
                c1 += 1
                if envio.moneda_origen != envio.moneda_pago:
                    c2 += 1
            print("r1.1:", c1)
            print("r1.2:", c2)

        elif op == 2:
            total_comision = 0
            mayor_descuento = -1
            envio_mayor = None

            for e in envios:
                com, imp, final = monto_final(e)
                porc_com = (com / e.monto) * 100
                total_comision += porc_com
                descuento = ((com + imp) / e.monto) * 100
                if descuento > mayor_descuento:
                    mayor_descuento = descuento
                    envio_mayor = e
                    monto_final_mayor = final

            prom_com = total_comision / len(envios)

            print("r2.1:", prom_com)
            print("r2.2:", envio_mayor.id_pago)
            print("r2.3:", monto_final_mayor)

            combinaciones = []
            for e in envios:
                combo = (e.moneda_origen, e.moneda_pago)
                if combo not in combinaciones:
                    combinaciones.append(combo)

            for origen, destino in combinaciones:
                mayor_final = -1
                id_envio = ""
                for e in envios:
                    if e.moneda_origen == origen and e.moneda_pago == destino:
                        com, imp, final = monto_final(e)
                        if final > mayor_final:
                            mayor_final = final
                            id_envio = e.id_pago

                print(f"Origen {origen} -> Destino {destino}: {mayor_final}")


if __name__ == "__main__":
    principal()