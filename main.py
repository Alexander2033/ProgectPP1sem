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
    telephone = Column(Integer)
    password = Column(String)
    email = Column(String)

#class Order(Base):
#    __tablename__ = 'order_lines'


#    id = Column(Integer, primary_key=True)
 #   order_id = Column(ForeignKey('orders.id'))
  #  item_id = Column(ForeignKey('items.id'))
   # quantity = Column(Integer)


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

                # Print the users
                for item in items:
                    print(item.name)
                    print(item.price)
                    print(item.quantity)
                    print(item.image)
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
                    print("True")
                return redirect('/')
        print("False")
        return render_template('door.html')

    else:
        return render_template('door.html')

@app.route('/katalog')
def katalog():
    session1 = Session()
    items = session1.query(Items).all()
    return render_template('Katalog.html', article=items)

@app.route('/support')
def support():
    if 'name' in session:
        print(session['name'])
    return render_template('Support.html')


@app.route('/backet')
def backet():
    return render_template('backet.html')

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
            user = User(name=namef, telephone=telephonef, email=emailf, password=passwordf)

            # Add the user to the database
            session1 = Session()
            session1.add(user)
            session1.commit()
            session['name'] = namef
            # Query the database for all users
            users = session1.query(User).all()

            # Print the users
            for user in users:
                print(user.name)
                print(user.telephone)
                print(user.email)
                print(user.password)
            return redirect('/')
        return render_template('creat-article.html')
    else:
        return render_template('creat-article.html')


if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True)

