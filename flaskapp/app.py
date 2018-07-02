from flask import Flask, render_template, flash, redirect, url_for, session, request
import datetime
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from wtforms_alchemy import ModelForm
from passlib.hash import sha256_crypt
from functools import wraps
import os

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
app.config["SECRET_KEY"] = "secret123"
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


class Article(db.Model):
    __tablename__ = "articles"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    author = db.Column(db.String(100))
    body = db.Column(db.Text)
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
    result = None
    if output:
        result = cur.fetchall()
    cur.close()
    return result


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


@app.route('/ver_modificar_registro')
def ver_modificar_registro():
    try:
        registros = run_sql("SELECT * FROM principal")

        if len(registros) > 0:
            return render_template("registros.html", registros=registros)
        msg = 'No se encontraron registros'
        return render_template('registros.html', registros=registros, msg=msg)
    except Exception as e:
        logging.info(e)


# @app.route('/articles/<string:id>')
# def article(id):
#     try:
#         result = run_sql("SELECT * FROM articles WHERE id = '{}'".format(id))
#         return render_template('article.html', article=result[0])
#     except Exception as e:
#         logging.info(e)
#
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
    try:
        form = PrincipalForm(request.form)

        if request.method == 'POST' and form.validate():

            #cod_prodein = form.cod_prodein.data
            titulo = form.titulo.data
            nombre = form.nombre.data
            apellido_1 = form.apellido_1.data
            apellido_2 = form.apellido_2.data
            identificacion = form.identificacion.data
            tipo_id = form.tipo_id.data
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
        return render_template('agregar_registro.html', form=form)

    except Exception as e:
        logging.info(e)




@app.route('/register', methods=['GET', 'POST'])
def register():
    try:
        form = RegisterForm(request.form)
        if request.method == 'POST' and form.validate():
            name = form.name.data
            email = form.email.data
            username = form.username.data
            test = run_sql("select * from users where username = '{}'".format(username))
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

            result = run_sql("SELECT * FROM users where username = '{}'".format(username))
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
        result = run_sql("SELECT * FROM principal")
        #if len(result) > 0:
        return render_template("panel_de_control.html", usuarios=len(result), registros=result)
        # else:
        #     msg = 'No hay registros'
        #     return render_template("panel_de_control.html", msg=msg)
    except Exception as e:
        logging.info(e)

# class ArticleForm(Form):
#     title = StringField('Title', [validators.Length(min=1, max=200)])
#     body = TextAreaField('Body', [validators.Length(min=30)])


@app.route('/edit_article/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_article(id):
    try:
        result = run_sql("Select * from articles where id = '{}'".format(id))
        form = ArticleForm(request.form)

        form.title.data = result[0]['title']
        form.body.data = result[0]['body']

        if request.method == 'POST':
            form.title.data = request.form['title']
            form.body.data = request.form['body']
            if form.validate():
                run_sql("update articles set title='{}', body='{}' where id = '{}'".format(form.title.data,form.body.data,id), output=False)

                flash('Article updated', 'success')
                return redirect(url_for('dashboard'))

        return render_template('edit_article.html', form=form)
    except Exception as e:
        logging.info(e)

@app.route("/delete_article/<string:id>", methods=['post'])
@is_logged_in
def delete_article(id):
    try:
        run_sql("delete from articles where id = '{}'".format(id), output=False)
        flash('Article deleted', 'success')
        return redirect(url_for('dashboard'))
    except Exception as e:
        logging.info(e)

@app.route('/add_article', methods=['GET', 'POST'])
@is_logged_in
def add_article():
    try:
        form = ArticleForm(request.form)
        if request.method == 'POST' and form.validate():
            title = form.title.data
            body = form.body.data
            author = session['username']
            article = Article(title=title, author=author, body=body)
            db.session.add(article)
            db.session.commit()
            flash('Article created', 'success')
            return redirect(url_for('dashboard'))

        return render_template('add_article.html', form=form)
    except Exception as e:
        logging.info(e)

if __name__ == '__main__':
    #app.secret_key='secret123'
    app.run(debug=True,host=os.getenv('IP', '0.0.0.0'),
            port=int(os.getenv('PORT', 4444)))
