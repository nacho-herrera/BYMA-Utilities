from enum import Enum

class Monedas(Enum):
    PESOS = "00"
    DOLAR_MEP = "01"
    DOLAR_CABLE = "02"


class Movimientos(Enum):
    TODOS = ""
    ALTA_OBLIGACION = "01"
    BAJA_OBLIGACION = "02"
    AFECTACION_TITULOS = "03"
    DESAFECTACION_TITULOS = "04"
    ADELANTO_COMPRAS = "06"
    ADELANTO_CHEQUES = "07"
    DIFERIMIENTO = "08"
    LIBERACION_COMPRAS = "09"


class TipoMovimiento(Enum):
    TODOS = None
    SALDO_ANTERIOR = "01"
    MOV_BANCOS = "02"
    MOV_GARANTIAS = "03"
    MOV_ACREENCIAS = "04"


class Segmentos(Enum):
    TOTAL = "T"
    GARANTIZADO = "G"
    NO_GARANTIZADO = "N"
    COLOCACIONES_PRIMARIAS = "P"

