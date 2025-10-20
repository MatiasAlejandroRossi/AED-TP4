class Envio:
    def __init__(self, cod, des, nom, tas, mon, com, imp):
        self.codigo = cod
        self.destinatario = des
        self.nombre = nom
        self.tasa = float(tas)
        self.monto = float(mon)
        self.comision = int(com)
        self.impositivo = int(imp)

        partes = cod.split("|")
        self.moneda_origen = int(partes[0])
        self.moneda_pago = int(partes[1])
        self.id_pago = partes[2]


    def __str__(self):
        return f"Envio {self.id_pago} - {self.nombre} ({self.monto} nominal)"