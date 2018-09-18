#!/usr/bin/python

from flask import Flask, render_template, flash, redirect, url_for, session, request
import datetime
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from wtforms_alchemy import ModelForm
from passlib.hash import sha256_crypt
from functools import wraps
from constants import (
    formas_pago,
    identificaciones,
    titulos,
    periodicidades
)
import os
from collections import OrderedDict
import logging
logging.basicConfig(filename='applog.log',level=logging.DEBUG)


# Config MySQL

app = Flask(__name__)

dbtouse = None
localdb = "mysql+pymysql://abcprode_admin:lockboxes11@localhost/abcprode_principal"
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="prodeinvzla",
    password="lockboxes11",
    hostname="prodeinvzla.mysql.pythonanywhere-services.com",
    databasename="prodeinvzla$abcprode_principal",
)

if os.getenv('HOME') == '/home/prodeinvzla':
    dbtouse = SQLALCHEMY_DATABASE_URI
else:
    dbtouse = localdb

app.config["SECRET_KEY"] = "FLASK_SCRT"
app.config["SQLALCHEMY_DATABASE_URI"] = dbtouse # SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

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
    municipio = db.Column(db.String(100))

    # bools
    voluntario = db.Column(db.Boolean, default=False)
    adorador = db.Column(db.Boolean, default=False)
    sociocolaborador = db.Column(db.Boolean, default=False)
    dama_prodein = db.Column(db.Boolean, default=False)
    activo = db.Column(db.Boolean, default=False)
    ejercitante = db.Column(db.Boolean, default=False)

class PrincipalForm(ModelForm):
    class Meta:
        model = Principal

def run_sql(statement, output=True):
    cur = db.session.execute(statement)
    db.session.commit()

    if output:
        result = cur.fetchall()
        try:
            cols = OrderedDict(result[0].items()).keys()
        except IndexError:
            cur.close()
    else:
        return None, None
    cur.close()
    return result, cols


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("No autorizado, debe conectarse", 'danger')
            return redirect(url_for('login'))
    return wrap


@app.route('/')
def index():
    return render_template('inicio.html')


# @app.route('/quienes_somos')
# def quiene_somos():
#     return render_template('quienes_somos.html')


@app.route('/registros', methods=['GET', 'POST'])
def registros():
    emptyform = PrincipalForm(request.form)

    if request.method == 'POST':
        form = request.form

        whereclause = "WHERE "
        for field in form:
            if form[field] == '':
                continue
            if field not in ['nombre', 'apellido_1','apellido_2']:
                continue
                #write a function to format the data in each field to appropriate value for the update clause.
            whereclause += field +"='"+str(form[field])+"' and "

        query = "SELECT * FROM principal "
        if whereclause[:-5] != '':
            query += whereclause[:-5]
        result, cols = run_sql(query)
        output = result if result else []

        return render_template("registros.html", registros=output, form=emptyform)

    elif request.method == 'GET':

        registros, cols = run_sql("SELECT * FROM principal")

       #if len(registros) > 0:
        return render_template("registros.html", registros=registros, form=emptyform)
        # else:
        #     msg = 'No se encontraron registros'
        #     return render_template('panel_de_control.html', usuarios=len(registros), msg=msg)
    # except Exception as e:
    #     logging.info(e)


@app.route('/registros/<string:id>')
def registro(id):
    try:
        result, cols = run_sql("SELECT * FROM principal WHERE cod_prodein = '{}'".format(id))
        return render_template('registro.html', cols=cols, registro=result[0])
    except Exception as e:
        logging.info(e)


@app.route('/registros/<string:id>/modificar', methods=['GET','POST'])
def modificar_registro(id):
    form = PrincipalForm(request.form)

    if request.method == 'GET':
        result, cols = run_sql("SELECT * FROM principal WHERE cod_prodein = '{}'".format(id))
        ids = [x.keys()[0] for x in identificaciones]
        for field in form:
            field.data = result[0][field.name]
        #result, cols = run_sql("SELECT * FROM principal WHERE cod_prodein = '{}'".format(id))

        try:
            return render_template('agregar_registro.html', form=form, titulos=titulos, periodicidades=periodicidades,
                                   identificaciones=ids, formas_pago=formas_pago)
        except Exception as e:
            logging.info(e)
    elif request.method == 'POST':
        titulo = request.form['t_titulo']
        tipo_id = request.form['t_id']
        strset = ""
        if titulo != '':
            strset += "titulo='" + titulo + "', "
        if tipo_id != '':
            strset += "tipo_id='" + tipo_id + "', "
        for field in form:
            print field.data
            if field.data == '':
                continue
            if field.name == 'direccion':
                continue
                #write a function to format the data in each field to appropriate value for the update clause.
            field_data = field.data if field.type != 'BooleanField' else int(field.data)

            strset += field.name+"='"+str(field_data)+"', "


        query = "UPDATE principal SET " + strset[:-2] + " WHERE cod_prodein=" + id
        print query
        run_sql(query, output=False)
        flash("Registro actualizado", 'success')
        return redirect(url_for('registros'))
    else:
        pass




class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


@app.route('/agregar_registro', methods=['GET', 'POST'])
@is_logged_in
def agregar_registro():
    ids = [x.keys()[0] for x in identificaciones]
    try:
        form = PrincipalForm(request.form)

        if request.method == 'POST' and form.validate():

            #cod_prodein = form.cod_prodein.data
            titulo = form.titulo.data
            nombre = form.nombre.data
            apellido_1 = form.apellido_1.data
            apellido_2 = form.apellido_2.data
            identificacion = form.identificacion.data
            tipo_id = request.values.get("t_id","")
            telf_1 = form.telf_1.data
            telf_2 = form.telf_2.data
            telf_cel = form.telf_cel.data
            vinculo = form.vinculo.data
            email = form.email.data
            # fecha_alta = form.fecha_alta.data
            # fecha_modificacion = form.fecha_modificacion.data
            # fecha_baja = form.fecha_baja.data
            direccion = form.direccion.data
            estado = form.estado.data
            municipio = form.municipio.data

            #bools
            voluntario = form.voluntario.data
            adorador = form.adorador.data
            sociocolaborador = form.sociocolaborador.data
            dama_prodein = form.dama_prodein.data
            activo = form.activo.data
            ejercitante = form.ejercitante.data

            principal = Principal(titulo=titulo, nombre=nombre, apellido_1=apellido_1,
                                  apellido_2=apellido_2, identificacion=identificacion, tipo_id=tipo_id, telf_1=telf_1,
                                  telf_2=telf_2, telf_cel=telf_cel, vinculo=vinculo, email=email, direccion=direccion,
                                  estado=estado, municipio=municipio, voluntario=voluntario, adorador=adorador,
                                  sociocolaborador=sociocolaborador, dama_prodein=dama_prodein, activo=activo, ejercitante=ejercitante)


            db.session.add(principal)
            db.session.commit()
            flash('Registro creado', 'success')

            return redirect(url_for('panel_de_control'))
        return render_template('agregar_registro.html', form=form, titulos=titulos, periodicidades=periodicidades,
                               identificaciones=ids, formas_pago=formas_pago)

    except Exception as e:
        logging.info(e)


@app.route('/registro_usuarios', methods=['GET', 'POST'])
def register_user():
    try:
        form = RegisterForm(request.form)
        if request.method == 'POST' and form.validate():
            name = form.name.data
            email = form.email.data
            username = form.username.data
            test, cols = run_sql("select * from users where username = '{}'".format(username))
            if len(test) > 1:
                return render_template('register.html', form=form, error="Username taken")
            password = sha256_crypt.encrypt(str(form.password.data))

            user = User(name=name, email=email, username=username, password=password)
            db.session.add(user)
            db.session.commit()
            flash('You are now registered and can log in', 'success')

            return redirect(url_for('panel_de_control'))

        return render_template('register.html', form=form)

    except Exception as e:
        logging.info(e)

@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'POST':
            username = request.form['username']
            password_candidate = request.form['password']

            result, cols = run_sql("SELECT * FROM users where username = '{}'".format(username))
            if len(result) == 1:
                data = result[0]
                password = data['password']
                if sha256_crypt.verify(password_candidate, password):
                    app.logger.info('PASSWORD MATCH')
                    session['logged_in'] = True
                    session['username'] = username

                    flash('Ingreso exitoso', 'success')
                    return redirect(url_for('panel_de_control'))


                else:
                    error = 'Invalid login'
                    app.logger.info(error)
                    return render_template('login.html', error=error)

            elif len(result) > 1:
                app.logger.info("Found more than 1 user: {}".format([ x['username'] + " with name " + x['name'] for x in result ] ))
            else:
                error = 'User not found'
                app.logger.info(error)
                return render_template('login.html', error=error)
        return render_template('login.html')
    except Exception as e:
        logging.info(e)


@app.route("/salir")
def salir():
    try:
        session.clear()
        flash("Sesion terminada", 'success')
        return redirect(url_for('login'))
    except Exception as e:
        logging.info(e)

@app.route("/panel_de_control")
@is_logged_in
def panel_de_control():
    try:
        result, cols = run_sql("SELECT * FROM principal")
        #if len(result) > 0:
        return render_template("panel_de_control.html", usuarios=len(result), registros=result)
        # else:
        #     msg = 'No hay registros'
        #     return render_template("panel_de_control.html", msg=msg)
    except Exception as e:
        logging.info(e)



if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',
            port=5050)
