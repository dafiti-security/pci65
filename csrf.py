from flask import Flask, session, redirect, url_for, request, render_template
from markupsafe import escape

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

posts = {}


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = escape(request.form['username'])
        return redirect(url_for('index'))
    return render_template('csrf/login.html')


@app.route('/')
def index():
    if 'username' in session:
        user = session['username']
        return render_template('csrf/home.html',
                               user=user,
                               posts=posts.get(user, []))

    return 'Você não está autenticado'


@app.route('/', methods=('POST',))
def new_post():
    if 'username' not in session:
        return redirect(url_for('index'))

    users_posts = posts.get(session['username'], [])
    users_posts.insert(0, request.form['post'])
    posts[session['username']] = users_posts
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/phishing')
def phishing():
    return render_template('csrf/phishing.html')


if __name__ == '__main__':
    app.run()











# correção:
# 0. Adicionar abaixo da linha 7: csrf = CSRFProtect(app) (fazer o import)
# 1. Adicionar na função login: @csrf.exempt
# 2. Adicionar no form da home.html: <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
# 3. Para testar na pagina de phising: adicionar <input type="hidden" name="csrf_token" value="3432423423423"/>
# CSRF com Flask: https://flask-wtf.readthedocs.io/en/stable/csrf.html
