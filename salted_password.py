import time

import bcrypt

senha = 'minhasenha123'
salt = bcrypt.gensalt()  # rounds=16 para aumentar a complexidade

ti = time.time()
hash_senha = bcrypt.hashpw(senha.encode(), salt)
tf = time.time()
print('hash: {}'.format(hash_senha))
print(tf - ti)
