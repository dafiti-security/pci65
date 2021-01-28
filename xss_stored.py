from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

news = ["Teste 1", "Teste 2", "Teste 3"]


@app.route('/', methods=('GET',))
def home():
    return render_template('xss_stored/news.html', news=news)


@app.route('/', methods=('POST',))
def save_new():
    new_post = request.form['post']

    if new_post:
        news.insert(0, new_post)
        return jsonify(), 201
    else:
        return jsonify(), 400


if __name__ == '__main__':
    app.run()












# ataque: <script>alert('oi')</script>

# correção
# 0. Substituir a linha 16 por: new_post = escape(request.form['post'])
# 1. adicionar o import no topo do arquivo: from markupsafe import escape
