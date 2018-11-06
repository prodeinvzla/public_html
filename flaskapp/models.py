# from app import db
import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class Principal(db.Model):
    __tablename__ = "principal"

    cod_prodein = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100))
    nombre = db.Column(db.String(100))
    apellido_1 = db.Column(db.String(100))
    apellido_2 = db.Column(db.String(100))
    identificacion = db.Column(db.String(100))
    tipo_id = db.Column(db.String(100))
    telf_1 = db.Column(db.String(20))
    telf_2 = db.Column(db.String(20))
    telf_cel = db.Column(db.String(20))
    vinculo = db.Column(db.String(100))
    email = db.Column(db.String(100))
    fecha_alta = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    fecha_modificacion = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    fecha_baja = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    direccion = db.Column(db.Text)
    estado = db.Column(db.String(100))
    ciudad = db.Column(db.String(100))
    municipio = db.Column(db.String(100))

    # bools
    voluntario = db.Column(db.Boolean, default=False)
    adorador = db.Column(db.Boolean, default=False)
    sociocolaborador = db.Column(db.Boolean, default=False)
    dama_prodein = db.Column(db.Boolean, default=False)
    activo = db.Column(db.Boolean, default=False)
    ejercitante = db.Column(db.Boolean, default=False)

    def __init__(self, titulo, nombre, apellido_1, apellido_2, identificacion, tipo_id, telf_1, telf_2,
                 telf_cel, vinculo, email, direccion, estado, ciudad,
                 municipio, voluntario, adorador, sociocolaborador, dama_prodein, activo, ejercitante):

        self.titulo = titulo
        self.nombre = nombre
        self.apellido_1 = apellido_1
        self.apellido_2 = apellido_2
        self.identificacion = identificacion
        self.tipo_id = tipo_id
        self.telf_1 = telf_1
        self.telf_2 = telf_2
        self.telf_cel = telf_cel
        self.vinculo = vinculo
        self.email = email

        self.direccion = direccion
        self.estado = estado
        self.ciudad = ciudad
        self.municipio = municipio
        self.voluntario = voluntario
        self.adorador = adorador
        self.sociocolaborador = sociocolaborador
        self.dama_prodein = dama_prodein
        self.activo = activo
        self.ejercitante = ejercitante



class DonacionPeriodica(db.Model):
    __tablename__ = "donacion_periodica"
    id = db.Column(db.Integer, primary_key=True)
    cod_prodein = db.Column(db.Integer, db.ForeignKey('principal.cod_prodein'))
    periodicidad = db.Column(db.String(100))
    concepto = db.Column(db.String(100))
    importe = db.Column(db.String(100))
    forma_pago = db.Column(db.String(100))
    banco = db.Column(db.String(100))
    numero_cuenta = db.Column(db.String(100))
    vencimiento = db.Column(db.String(100))
    tipo_moneda = db.Column(db.String(100))
    activo = db.Column(db.Boolean, default=True)
    fecha_alta = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    fecha_modificacion = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    fecha_baja = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class Donacion(db.Model):
    __tablename__ = "donacion"
    id = db.Column(db.Integer, primary_key=True)
    cod_prodein = db.Column(db.Integer, db.ForeignKey('principal.cod_prodein'))
    concepto = db.Column(db.String(100))
    importe = db.Column(db.String(100))
    forma_pago = db.Column(db.String(100))
    fecha_alta = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    fecha_modificacion = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    fecha_baja = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    cod_donador = db.relationship("Principal", backref=db.backref(
        "donacion", order_by=id))
