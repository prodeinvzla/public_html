
local_db = "mysql+pymysql://abcprode_admin:lockboxes11@localhost/abcprode_principal"
external_db = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="prodeinvzla",
    password="lockboxes11",
    hostname="prodeinvzla.mysql.pythonanywhere-services.com",
    databasename="prodeinvzla$abcprode_principal",
)

formas_pago = ["CHEQUE", "EFECTIVO", "PAYPAL", "TDC", "TRANSFERENCIA"]

identificaciones = [
    {'C': 'CONSEJO COMUNAL, COMUNA, U OTRA ORGANIZACION SOCIOPRODUCTIVA'},
    {'E': 'PERSONA NATURAL EXTRANJERO'},
    {'G': 'ENTE GUBERNAMENTAL'},
    {'J': 'PERSONA JURIDICA'},
    {'P': 'PASAPORTE'},
    {'V': 'PERSONA NATURAL VENEZOLANO'}
]

periodicidades = [
    "ANUAL",
    "MENSUAL",
    "OCASIONAL",
    "SEMANAL",
    "SEMESTRAL",
    "TRIMESTRAL",
]

titulos = [
    "FLIA.",
    "HNA.",
    "HNAS.",
    "M.M.",
    "RVDO. P.",
    "SR.",
    "SRA.",
    "SRTA.",
]


estados = [
 'AMAZONAS',
 'ANZOATEGUI',
 'APURE',
 'ARAGUA',
 'BARINAS',
 'BOLIVAR',
 'CARABOBO',
 'COJEDES',
 'DELTA AMACURO',
 'FALCON',
 'GUARICO',
 'LARA',
 'MERIDA',
 'MIRANDA',
 'MONAGAS',
 'NUEVA ESPARTA',
 'PORTUGUESA',
 'SUCRE',
 'TACHIRA',
 'TRUJILLO',
 'VARGAS',
 'YARACUY',
 'ZULIA',
 'DISTRITO CAPITAL',
 'DEPENDENCIAS FEDERALES'
]