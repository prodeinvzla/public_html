#!/usr/bin/python


from flask import Flask, render_template, flash, redirect, url_for, session, request
from flask_sqlalchemy import SQLAlchemy
from models import db
import models
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from forms import DonacionPeriodicaForm, PrincipalForm
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
#from db import init_db
from constants import external_db, local_db

#init_db()


# Config MySQL

app = Flask(__name__)

if os.getenv('HOME') == '/home/prodeinvzla':
    dbtouse = external_db
else:
    dbtouse = local_db

app.config["SECRET_KEY"] = "FLASK_SCRT"
app.config["SQLALCHEMY_DATABASE_URI"] = dbtouse # SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#app.config['TRAP_HTTP_EXCEPTIONS'] = True

db.init_app(app)


def run_sql(statement, output=True):
    cur = db.session.execute(statement)
    db.session.commit()
    result = 'empty_result'
    cols = ['empty_cols']
    if output:
        result = cur.fetchall()
        try:
            cols = OrderedDict(result[0].items()).keys()
        except IndexError:
            pass
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
        return render_template("registros.html", registros=registros, form=emptyform)


@app.route('/registros/<string:id>')
def registro(id):
    try:
        result, cols = run_sql("SELECT * FROM principal WHERE cod_prodein = '{}'".format(id))
        return render_template('registro.html', cols=cols, registro=result[0])
    except Exception as e:
        logging.info(e)

@app.route('/registros_donacion_periodica', methods=['GET', 'POST'])
def registros_don_rec():
    emptyform = DonacionPeriodicaForm(request.form)

    if request.method == 'POST':
        form = request.form

        whereclause = "WHERE "
        for field in form:
            if form[field] == '' or field not in ['cod_prodein', 'periodicidad', 'concepto']:
                continue
                #write a function to format the data in each field to appropriate value for the update clause.
            whereclause += field +"='"+str(form[field])+"' and "

        query = "SELECT * FROM donacion_periodica "
        if whereclause[:-5] != '':
            query += whereclause[:-5]
        result, cols = run_sql(query)
        output = result if result else []
        return render_template("registros_donacion_periodica.html", registros=output, form=emptyform)

    elif request.method == 'GET':
        registros, cols = run_sql("SELECT * FROM donacion_periodica")
        return render_template("registros_donacion_periodica.html", registros=registros, form=emptyform)


@app.route('/registros_donacion_periodica/<string:id>')
def registro_don_rec(id):
    try:
        result, cols = run_sql("SELECT * FROM donacion_periodica WHERE cod_prodein = '{}'".format(id))
        return render_template('registro_donacion_periodica.html', cols=cols, registro=result[0])
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
        print request.form
        entry = db.session.query(models.Principal).filter_by(cod_prodein=id).first()

        entry.titulo = request.form['titulo']
        entry.nombre = request.form['nombre']
        entry.apellido_1 = request.form['apellido_1']
        entry.apellido_2 = request.form['apellido_2']
        entry.identificaion = request.form['identificacion']
        entry.tipo_id = request.form['tipo_id']
        entry.telf_1 = request.form['telf_1']
        entry.telf_2 = request.form['telf_2']
        entry.telf_cel = request.form['telf_cel']
        #entry.vinculo = request.form['vinculo']
        entry.email = request.form['email']

        entry.direccion = request.form['direccion']
        entry.estado = request.form['estado']
        entry.ciudad = request.form['ciudad']
        entry.municipio = request.form['municipio']
        # entry.voluntario = request.form['voluntario']
        # entry.adorador = request.form['adorador']
        # entry.sociocolaborador = request.form['sociocolaborador']
        # entry.dama_prodein = request.form['dama_prodein']
        # entry.activo = request.form['activo']
        # entry.ejercitante = request.form['ejercitante']

        db.session.commit()

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
            direccion = form.direccion.data
            estado = form.estado.data
            ciudad = form.ciudad.data
            municipio = form.municipio.data

            #bools
            voluntario = form.voluntario.data
            adorador = form.adorador.data
            sociocolaborador = form.sociocolaborador.data
            dama_prodein = form.dama_prodein.data
            activo = form.activo.data
            ejercitante = form.ejercitante.data

            principal = models.Principal(titulo=titulo, nombre=nombre, apellido_1=apellido_1,
                                  apellido_2=apellido_2, identificacion=identificacion, tipo_id=tipo_id, telf_1=telf_1,
                                  telf_2=telf_2, telf_cel=telf_cel, vinculo=vinculo, email=email, direccion=direccion,
                                  estado=estado, ciudad=ciudad, municipio=municipio, voluntario=voluntario, adorador=adorador,
                                  sociocolaborador=sociocolaborador, dama_prodein=dama_prodein, activo=activo, ejercitante=ejercitante)


            db.session.add(principal)
            db.session.commit()
            flash('Registro creado', 'success')

            return redirect(url_for('panel_de_control'))
        return render_template('agregar_registro.html', form=form, titulos=titulos, periodicidades=periodicidades,
                               identificaciones=ids, formas_pago=formas_pago)

    except Exception as e:
        logging.info(e)


@app.route('/agregar_donacion_periodica', methods=['GET', 'POST'])
@is_logged_in
def agregar_donacion_periodica():
    #ids = [x.keys()[0] for x in identificaciones]
    try:
        form = DonacionPeriodicaForm(request.form)

        if request.method == 'POST' and form.validate():

            cod_prodein = form.cod_prodein.data
            periodicidad = form.periodicidad.data
            concepto = form.concepto.data
            importe = form.importe.data
            forma_pago = form.forma_pago.data
            banco = form.banco.data
            numero_cuenta = form.numero_cuenta.data
            vencimiento = form.vencimiento.data
            tipo_moneda = form.tipo_moneda.data
            activo = form.activo.data

            donacion_periodica = models.DonacionPeriodica(cod_prodein=cod_prodein,
                                                    periodicidad=periodicidad,
                                                    concepto=concepto,
                                                    importe=importe,
                                                    forma_pago=forma_pago,
                                                    banco=banco,
                                                    numero_cuenta=numero_cuenta,
                                                    vencimiento=vencimiento,
                                                    tipo_moneda=tipo_moneda,
                                                    activo=activo,

                                                    )
            db.session.add(donacion_periodica)
            db.session.commit()
            flash('Registro creado', 'success')

            return redirect(url_for('panel_de_control'))

        #return render_template("hello.html")
        logging.info("got here")
        return render_template('agregar_donacion_periodica.html',
                               form=form,
                               periodicidades=periodicidades,
                               formas_pago=formas_pago)

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
        personas, cols = run_sql("SELECT * FROM principal")
        don_rec, cols = run_sql("SELECT * FROM donacion_periodica")
        donaciones, cols = run_sql("SELECT * FROM donacion")


        #if len(result) > 0:
        return render_template("panel_de_control.html",
                               personas=len(personas),
                               don_rec=len(don_rec),
                               donaciones=len(donaciones)
                               )
    except Exception as e:
        logging.info(e)



if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',
            port=5050)
