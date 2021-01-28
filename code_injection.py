import os
import sqlite3
import subprocess
import traceback
from uuid import uuid4

from flask import Flask, request, jsonify

DB_PATH = 'user.db'

app = Flask(__name__)


def create_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conexao = sqlite3.connect(DB_PATH)
    cursor = conexao.cursor()
    cursor.execute('''CREATE TABLE usuarios (cpf TEXT NOT NULL PRIMARY KEY, 
                                             nome TEXT NOT NULL,
                                             senha TEXT NOT NULL)''')

    for cpf, nome, senha in (('12345678910', 'joao', 'asdhjasg736427638'),
                             ('01987654321', 'maria', 'hdsfsd3824329847932'),
                             ('11122233345', 'pedro', '734ydshgfdsf7ds342')):
        cursor.execute("INSERT INTO usuarios values ('{}', '{}', '{}')".format(cpf, nome, senha))

    conexao.commit()
    conexao.close()


@app.route('/login', methods=('POST',))
def login():
    usuario, senha = request.form['usuario'], request.form['senha']

    conexao = sqlite3.connect(DB_PATH)
    cursor = conexao.cursor()

    try:
        cursor.execute("SELECT nome FROM usuarios WHERE nome = '{}' AND senha = '{}'".format(usuario, senha))
        sucesso = bool(cursor.fetchall())
    except:
        sucesso = False
    finally:
        conexao.close()

    if sucesso:
        return jsonify({'sid': str(uuid4())})
    else:
        return jsonify(''), 401


@app.route('/usuarios/cpf', methods=('GET',))
def consultar_por_cpf():
    cpf = request.args.get('cpf', '')

    conexao = sqlite3.connect(DB_PATH)
    cursor = conexao.cursor()

    try:
        cursor.execute("SELECT cpf, nome FROM usuarios WHERE cpf = '{}'".format(cpf))
        usuarios = cursor.fetchall()
    except:
        traceback.print_exc()
        usuarios = None
    finally:
        conexao.close()

    if usuarios:
        return jsonify([{'cpf': cpf, 'nome': nome} for cpf, nome in usuarios])
    else:
        return jsonify(''), 404


@app.route('/arquivos', methods=('GET',))
def consulta_arquivos():
    arquivo = request.args.get('arquivo', '')

    try:
        saida = subprocess.check_output('find . -name {}'.format(arquivo), stderr=subprocess.STDOUT, shell=True).decode()
    except:
        saida = None

    if saida:
        return jsonify([linha for linha in saida.split('\n') if linha])
    else:
        return jsonify(''), 404


if __name__ == '__main__':
    create_db()
    app.run()






# correções
# login: xpto' or 1=1 --
# cursor.execute("SELECT nome FROM usuarios WHERE nome = ? AND senha = ?", (usuario, senha))
# cursor.fetchone()

# consulta (simples): 1234' or 1=1 --
# cursor.execute("SELECT cpf, nome FROM usuarios WHERE cpf = ?", cpf)
# cursor.fetchmany()

# consulta (union): 1234' or 1=1 UNION SELECT type, sql FROM SQLITE_MASTER --

# command injection: caso 1:   caso 2: nada | ls /home/**/* caso3
# 1. ler todos os arquivos do diretório: '*'
# 2. ler todos os arquivos de um diretório qualquer: nada | ls /home/**/*
# 3. ler o conteúdo de um arquivo: nada | cat /home/vinicius_moreira/dafiti-dorks.txt
# possível correção:  arquivo = arquivo.strip().replace('*', '').split(' ')[0]

