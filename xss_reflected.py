from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    query = request.args.get('query', '')
    return render_template('xss_reflected/home.html', query=query)


if __name__ == '__main__':
    app.run()








# correção
# 0. Remover a expressão "| safe" da linha 7 da home.html
