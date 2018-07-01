from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flaskext.mysql import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

app = Flask(__name__)

# Config MySQL

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'abcprode_admin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'lockboxes11'
app.config['MYSQL_DATABASE_DB'] = 'abcprode_principal'
app.config['MYSQL_DATABASE_CURSORCLASS'] = 'DictCursor'

# init MYSQL
mysql = MySQL(app)
#mysql.init_app(app)


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


@app.route('/quienes_somos')
def quiene_somos():
    return render_template('quienes_somos.html')


@app.route('/articles')
def articles():
    cur = mysql.get_db().cursor()
    result = cur.execute("SELECT * FROM ARTICLES")
    articles = cur.fetchall()
    if result > 0:
        return render_template("articles.html", articles=articles)
    msg = 'No articles found'
    return render_template('articles.html', articles=articles, msg=msg)
    cur.close()


@app.route('/articles/<string:id>')
def article(id):
    cur = mysql.get_db().cursor()
    cur.execute("SELECT * FROM ARTICLES WHERE id = %s", [id])
    art = cur.fetchone()
    cur.close()
    return render_template('article.html', article=art)

class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
        cur = mysql.get_db().cursor()
        cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)",
                    (name, email, username, password))

        mysql.connection.commit()
        cur.close()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('articles'))

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']

        cur = mysql.get_db().cursor()
        result = cur.execute("SELECT * FROM users where username = %s", [username])
        if result > 0:
            data = cur.fetchone()
            password = data['password']
            if sha256_crypt.verify(password_candidate, password):
                app.logger.info('PASSWORD MATCH')
                session['logged_in'] = True
                session['username'] = username

                flash('You are now loggeado', 'success')
                return redirect(url_for('dashboard'))


            else:
                error = 'Invalid login'
                app.logger.info(error)
                return render_template('login.html', error=error)
            cur.close()
        else:
            error = 'User not found'
            app.logger.info(error)
            return render_template('login.html', error=error)
    return render_template('login.html')


@app.route("/logout")
def logout():
    session.clear()
    flash("Sesion terminada")
    return redirect(url_for('login'))

@app.route("/dashboard")
@is_logged_in
def dashboard():
    cur = mysql.get_db().cursor()
    result = cur.execute("SELECT * FROM ARTICLES")
    articles = cur.fetchall()
    if result > 0:
        return render_template("dashboard.html", articles=articles)
    else:
        msg = 'No articles found'

        return render_template("dashboard.html", msg=msg)
    cur.close()

class ArticleForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=200)])
    body = TextAreaField('Body', [validators.Length(min=30)])


@app.route('/edit_article/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_article(id):
    cur = mysql.get_db().cursor()
    cur.execute("Select * from articles where id = %s", [id])
    article = cur.fetchone()
    form = ArticleForm(request.form)

    form.title.data = article['title']
    form.body.data = article['body']

    if request.method == 'POST':
        form.title.data = request.form['title']
        form.body.data = request.form['body']
        if form.validate():
            cur.execute("update articles set title=%s, body=%s where id = %s", (form.title.data,form.body.data,[id]))
            mysql.connection.commit()
            cur.close()
            flash('Article updated', 'success')
            return redirect(url_for('dashboard'))
    cur.close()
    return render_template('edit_article.html', form=form)

@app.route("/delete_article/<string:id>", methods=['post'])
@is_logged_in
def delete_article(id):
    cur = mysql.get_db().cursor()
    cur.execute("delete from articles where id = %s", [id])
    mysql.connection.commit()
    cur.close()
    flash('Article deleted', 'success')
    return redirect(url_for('dashboard'))

@app.route('/add_article', methods=['GET', 'POST'])
@is_logged_in
def add_article():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data

        cur = mysql.get_db().cursor()
        author = session['username']
        cur.execute("INSERT INTO articles(title, body, author) VALUES(%s, %s, %s)",
                    (title, body, author))
        mysql.connection.commit()
        cur.close()
        flash('Article created', 'success')
        return redirect(url_for('dashboard'))

    return render_template('add_article.html', form=form)


if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)
