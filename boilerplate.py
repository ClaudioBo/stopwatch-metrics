"""
Utilidad para el tema del cronometro
"""

import time, json


class Stopwatch:
    def __init__(self):
        self.inicio = None

    def iniciar(self):
        self.inicio = time.time()

    def terminar(self):
        total = time.time() - self.inicio
        return f"{total*1000:.2f}"


"""
Uso del cronometro
"""
cronometro_datos = {}
stopwatch = Stopwatch()

stopwatch.iniciar()
cronometro_datos["1_prueba"] = stopwatch.terminar()

with open("cronometro_datos.json", "a") as f:
    f.write(json.dumps(cronometro_datos))
