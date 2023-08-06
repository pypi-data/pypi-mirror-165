#pip install build
#pip install setuptools
#pip install wheel
#pip install twine
#creer un dossier src ou mettre les codes : main et other
#creer un dosssier tests pr y mettre les tests unitaires
#creer un fichier pyprojet.toml : fichier de construction
#y mettre :
"""
[build-system]
requires = ["setuptools", "wheel"]
build_backend = "setuptools.build_meta"

"""
#setup.cfg : fichier de configuration statique pr dynamique : setup.py
#syntaxe d un fichier ini
#y mettre :
#version = <Majeur>.<Mineur>.<Maintenance> #passer par un fichier de version attr: src.VERSION

"""
[metadata]
name = MonProjetKali
version = 1.0.0
author = René LaTaupe
description = Un projet inutile
long_description = file: README.md 
long_description_content_type = text/markdown
licence = file: LICENCE
classifiers =  #repertorier le projet au bon endroit https://pypi.org/classifiers/
    One
    Two
    Etc.

[options]
package_dir =
    = src
python_requires = >= 3.7



#projet_urls = 
    #info https://
    #info2 https://
    #Bug Tracker https://
#download_url = 


"""
#python Package index : plateforme de depot
#pypi.org :
#partie principal recup et mettre en ligne des projets
#autre partie : test python Package index


#creer un token :
#aller sur le profile puis add API token
#nom : tutoriel_formationVideo
#permission : mettre en ligne des paquets : Upload packages
#scope : portée : Entire account (all projets)
#copier le :
#pypi-AgEIcHlwaS5vcmcCJDRjMjM0N2I3LTc3MmYtNDc1Yy05NmNlLWU4YTBjOWYyOGI1ZgACKlszLCJmNTEwYWJiMi0zMzgyLTQ1MDctYjE4OS1iZjZlYzQyOGVmMWMiXQAABiBk727CR8Fk4Oh1Sr07zy73HycJ7sQ7iMpeojPyja5Rmg


"""
[pypi]
  username = __token__
  password = pypi-AgEIcHlwaS5vcmcCJDRjMjM0N2I3LTc3MmYtNDc1Yy05NmNlLWU4YTBjOWYyOGI1ZgACKlszLCJmNTEwYWJiMi0zMzgyLTQ1MDctYjE4OS1iZjZlYzQyOGVmMWMiXQAABiBk727CR8Fk4Oh1Sr07zy73HycJ7sQ7iMpeojPyja5Rmg

"""
#depuis l outils mise en ligne sur la version test du compte
#pip list : voir ce qu on installer
#cmd :
#python -m build :pr construire le projet
#on obtient un dossier dist : 2 fichier tar.gz et whl : outils de configuration des paquets : utilise le fichier whl
#dans le cas il ne marcherait pas il se rabattrait sur l archive
#mettre en ligne les deux versions : compatibilité
#cmd :
#python -m twine upload --repository testpypi dist/*
#Enter your username: __token__
#Enter your password: api token

def hello_world():
    print("Hello World !")