from flask import Flask,  render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

#---------------------BASE DE DATOS------------------------

# ruta absoluta d'aquesta carpeta
basedir = os.path.abspath(os.path.dirname(__file__)) 

# paràmetre que farà servir SQLAlchemy per a connectar-se
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + basedir + "/base_datos.db"

# Inicio SQLAlchemy
db = SQLAlchemy()
db.init_app(app)

#######-----------------TABLA-PRODUCTOS---------------#######
class Product(db.Model):
    
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    photo = db.Column(db.String)
    price = db.Column(db.Integer)
    # category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    # seller_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created = db.Column(db.DateTime, nullable=False, server_default= db.func.now())
    updated = db.Column(db.DateTime, nullable=False, server_default= db.func.now(), onupdate= db.func.now())

    # category = db.relationship('Category', back_populates='products')
    # seller = db.relationship('User', back_populates='products')



#####----------------SELECT-------------------####
@app.route('/')
def init():
    return redirect(url_for('list'))

@app.route('/product')
def list():
    products = db.session.execute(
        db.select(Product).order_by(Product.id.asc())
    ).scalars()
    return render_template('/products/list.html', products = products)


#####----------------CREATE-------------------####

@app.route('/product/create', methods = ['POST', 'GET'])
def create():
    # recupero l'item per la pk
    product = Product()
    if request.method == 'GET':
        
        return render_template('/products/create.html', product = product)
    else:
        title = request.form['title']
        description = request.form['description']
        photo = request.form['photo']
        price = request.form['price']
        # actualitzo els valors de l'item
        product.title = title
        product.description = description
        product.photo = photo
        product.price =  price
        # notifico que item ha canviat i amb el commit és guarda a la BBDD
        db.session.add(product)
        db.session.commit()

        # https://en.wikipedia.org/wiki/Post/Redirect/Get
        return redirect(url_for('list'))
    



#####----------------UPDATE-------------------####


@app.route('/product/<int:product_id>',methods = ['POST', 'GET'])
def product(product_id):
    # recupero l'item per la pk
    product = db.session.get(Product, product_id)
    if request.method == 'GET':
        
        return render_template('/products/update.html', product = product)
    
    else: # POST
        title = request.form['title']
        description = request.form['description']

        # actualitzo els valors de l'item
        product.title = title
        product.description = description

        # notifico que item ha canviat i amb el commit és guarda a la BBDD
        db.session.add(product)
        db.session.commit()

        # https://en.wikipedia.org/wiki/Post/Redirect/Get
        return redirect(url_for('list'))
    




#####----------------DELETE-------------------####


@app.route('/hello/')
def hello():
    return render_template('hello.html')



