#from wtforms_alchemy import ModelForm
#from models import Principal, DonacionPeriodica, Donacion
from wtforms import (
    Form,
    StringField,
    SelectField,
    DecimalField,
    IntegerField,
    DateField,
    BooleanField,
    TextAreaField,
    PasswordField,
    validators
    )
from constants import periodicidades, formas_pago, titulos, identificaciones, estados
from municipios import MUNICIPIOS
from ciudades import CIUDADES

class PrincipalForm(Form):


    cod_prodein = IntegerField('cod_prodein')
    titulo = SelectField('Titulo', choices=[(t,t) for t in titulos])
    nombre = StringField('Nombre')
    apellido_1 = StringField('Apellido 1')
    apellido_2 = StringField('Apellido 2')
    identificacion = IntegerField('N. ID')
    tipo_id = SelectField('Tipo ID', choices=[(tid.keys()[0], tid.keys()[0]) for tid in identificaciones])
    telf_1 = IntegerField('Telefono 1')
    telf_2 = IntegerField('Telefono 2')
    telf_cel = IntegerField('Telefono Movil')
    vinculo = StringField('Vinculo')
    email = StringField('Email')

    direccion = TextAreaField('Direccion')
    estado = SelectField('Estado', choices=[(e,e) for e in estados])
    ciudad = SelectField('Ciudad', choices=[(c[-1], c[-1]) for c in CIUDADES])
    municipio = SelectField('Municipio', choices=[(m[-1], m[-1]) for m in MUNICIPIOS])

    # bools
    voluntario = BooleanField('Voluntario', default=False)
    adorador = BooleanField('Adorador', default=False)
    sociocolaborador = BooleanField('Socio-colaborador', default=False)
    dama_prodein = BooleanField('Dama Prodein', default=False)
    activo = BooleanField('Activo', default=False)
    ejercitante = BooleanField('Ejercitante', default=False)



    # class Meta:
    #     model = Principal


class DonacionPeriodicaForm(Form):

   # id = db.Column(db.Integer, primary_key=True)
    cod_prodein = IntegerField('cod_prodein')
    periodicidad = SelectField('Periodicidad', choices=[(p,p) for p in periodicidades])

    concepto = StringField('Concepto')
    importe = DecimalField('Importe')
    forma_pago = SelectField('Forma Pago', choices=[ (fp, fp) for fp in formas_pago ])
    banco = StringField('Banco')
    numero_cuenta = IntegerField('Numero Cuenta', [validators.optional()])
    vencimiento = DateField('Vencimiento', [validators.optional()])
    busqueda = StringField("Busqueda")
    tipo_moneda = StringField('Tipo Moneda')
    activo = BooleanField(default='activo')
    # fecha_alta = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    # fecha_modificacion = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    # fecha_baja = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    #
    # class Meta:
    #     model = DonacionPeriodica


class DonacionForm(Form):
    cod_prodein = IntegerField('cod_prodein')
    concepto = StringField('Concepto')
    importe = DecimalField('Importe')
    forma_pago = SelectField('Forma Pago', choices=[(fp, fp) for fp in formas_pago])
    busqueda = StringField("Busqueda")


class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')