## Exemplos: PCI 6.5

### Dependências
- python3
- python3-venv

### Preparação
```
git clone git@github.com:dafiti-security/pci65.git
cd pci65
python3 -m venv venv
venv/bin/pip install pip --upgrade
venv/bin/pip install setuptools --upgrade
venv/bin/pip install -r requirements.txt
```

### Execução

Code Injection
```
./venv/bin/python code_injection.py
```

XSS Reflected
```
./venv/bin/python xss_reflected.py
```

XSS Stored

```
./venv/bin/python xss_stored.py
```

CSRF
```
./venv/bin/python csrf.py
```