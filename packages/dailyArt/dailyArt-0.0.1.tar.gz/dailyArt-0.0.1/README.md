## !!! Do not install this package This is a demo to setuptool 

---

### How to pack projects? 
[click me](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
***

### setup project
1. conda create -n daily python=3.10
2. conda activate daily
3. python -m pip install --upgrade pip
4. python -m pip install --upgrade build

### build project
1. python -m build
2. python -m twine upload  dist/*
