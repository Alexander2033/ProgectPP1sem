from flask import Flask, render_template, request, redirect, session
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, ClauseList, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

# Create a connection to your database
engine = create_engine('sqlite:///Baseee.db')

# Create a session factory
Session = sessionmaker(bind=engine)

# Create a base class for your models
Base = declarative_base()

# Define a model


class Items(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)
    quantity = Column(Integer)
    image = Column(String)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    telephone = Column(String)
    password = Column(String)
    email = Column(String)
    order_cost = Column(Integer)

class Order(Base):
    __tablename__ = 'order_lines'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('users.id'))
    item_id = Column(Integer, ForeignKey('items.id'))
    quantity = Column(Integer)


# Create the table in the database
Base.metadata.create_all(engine)

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blr.db'
#db = SQLAlchemy(app)

@app.route('/delT', methods=['POST', 'GET'])
def delT():
    if 'name' not in session:
        return redirect('/')
    if session['name'] == "admin":
        if (request.method == "POST"):
            namef = request.form['name']
            session1 = Session()
            items = session1.query(Items).all()
            for item in items:
                if item.name == namef:
                    session1.delete(item)
                    session1.commit()
                    break
        return render_template('delT.html')
    else:
        return redirect('/')



@app.errorhandler(404)
def pageNotFind(error):
    return render_template('index.html')

@app.route('/addT', methods=['POST', 'GET'])
def addT():
    if 'name' not in session:
        return redirect('/')
    if session['name'] == "admin":
        if (request.method == "POST"):
            namef = request.form['name']
            pricef = request.form['price']
            quantityf = request.form['quantity']
            imagef = request.form['image']
            if (namef and pricef and quantityf and imagef):
                item = Items(name=namef, price=pricef, quantity=quantityf, image=imagef)

                # Add the user to the database
                session1 = Session()
                session1.add(item)
                session1.commit()
                items = session1.query(Items).all()

        return render_template('addT.html')
    else:
        return redirect('/')



@app.route('/')
def index():
    return render_template('index.html')
@app.route('/door', methods=['POST', 'GET'])
def door():
    if (request.method == "POST"):
        passwordf = request.form['password']
        emailf = request.form['email']
        if (passwordf and emailf):
            session1 = Session()
            user = session1.query(User).filter_by(email=emailf).first()
            if user:
                if ((user.password == passwordf) and (user.email == emailf)):
                    session['name'] = user.name
                return redirect('/')
        return render_template('door.html')

    else:
        return render_template('door.html')



@app.route('/katalog', methods=['POST', 'GET'])
def katalog():
    session1 = Session()
    items = session1.query(Items).all()
    return render_template('Katalog.html', article=items)


@app.route('/backet', methods=['POST', 'GET'])
def backet():
    if 'name' in session:
        session1 = Session()
        orders = session1.query(Order).all()
        items = session1.query(Items).all()
        users = session1.query(User).all()
        for user in users:
            if (user.name == session['name']):
                for order in orders:
                    if (order.order_id == user.id):
                        for item in items:
                            if (order.item_id == item.id):
                                print(item.price)
                                user.order_cost += (item.price * order.quantity)
        return render_template('backet.html', orders=orders, items=items, all_users=users, user=session['name'], allcost=user.order_cost)
    return render_template('Error2.html')


@app.route('/cart3/<int:order_id>', methods=['POST'])
def order_delete(order_id):
    if 'name' in session:
        session1 = Session()
        order = session1.query(Order).filter_by(id=order_id).first()
        session1.delete(order)
        session1.commit()
    return redirect('/backet')

@app.route('/cart1/<int:order_id>', methods=['POST'])
def order_plas(order_id):
    if 'name' in session:
        session1 = Session()
        order = session1.query(Order).filter_by(id=order_id).first()
        product = session1.query(Items).filter_by(id=order.item_id).first()
        if (order.quantity < product.quantity):
            order.quantity += 1
        session1.commit()
    return redirect('/backet')

@app.route('/cart2/<int:order_id>', methods=['POST'])
def order_minus(order_id):
    if 'name' in session:
        session1 = Session()
        order = session1.query(Order).filter_by(id = order_id).first()
        if order.quantity > 0:
            order.quantity -= 1
        session1.commit()
    return redirect('/backet')


@app.route('/cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if 'name' in session:
        session1 = Session()
        product = session1.query(Items).filter_by(id = product_id).first()
        user = session1.query(User).filter_by(name = session['name']).first()
        orders = session1.query(Order).all()
        for order in orders:
            if ((order.order_id == user.id) and (order.item_id == product.id) and (order.quantity < product.quantity)):
                order.quantity += 1
                session1.commit()
                return redirect('/katalog')
            if (order.quantity == product.quantity):
                return redirect('/katalog')
        cart_item = Order(item_id=product.id, order_id=user.id, quantity=1)
        session1.add(cart_item)
        session1.commit()
        users = session1.query(Order).all()
    return redirect('/katalog')


@app.route('/support')
def support():
    if 'name' in session:
        print(session['name'])
    return render_template('Support.html')




@app.route('/unsetsession', methods=['POST', 'GET'])
def unsetsession():
    if 'name' in session:
        if (request.method == "POST"):
            session.pop('name', None)
            return redirect('/')
        return render_template('unsetsession.html')
    return render_template('Error2.html')



@app.route('/creat-article', methods=['POST', 'GET'])
def creat_article():
    if 'name' in session:
        return render_template('Error1.html')
    if (request.method == "POST"):
        namef = request.form['name']
        telephonef = request.form['telephone']
        passwordf = request.form['password']
        emailf = request.form['email']
        if (passwordf and emailf and telephonef and namef):
            session1 = Session()
            users = session1.query(User).all()
            for user1 in users:
                if ((user1.name == namef) and (user1.password == passwordf)):
                    return render_template('Error1.html')
            user = User(name=namef, telephone=telephonef, email=emailf, password=passwordf, order_cost=0)
            # Add the user to the database
            session1.add(user)
            session1.commit()
            session['name'] = namef
            # Query the database for all users
            users = session1.query(User).all()
            return redirect('/')
        return render_template('creat-article.html')
    else:
        return render_template('creat-article.html')


if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True)

