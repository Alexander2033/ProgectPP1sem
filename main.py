from flask import Flask, render_template, request
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Create a connection to your database
engine = create_engine('sqlite:///Based.db')

# Create a session factory
Session = sessionmaker(bind=engine)

# Create a base class for your models
Base = declarative_base()

# Define a model
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)
    size = Column(Integer)

# Create the table in the database
Base.metadata.create_all(engine)

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blr.db'
#db = SQLAlchemy(app)




@app.route('/')
def index():
    return render_template('index.html')

@app.route('/katalog')
def katalog():
    return render_template('Katalog.html')

@app.route('/support')
def support():
    return render_template('Support.html')


@app.route('/backet')
def backet():
    return render_template('backet.html')


@app.route('/creat-article', methods=['POST', 'GET'])
def creat_article():
    if (request.method == "POST"):
        namef = request.form['name']
        pricef = request.form['price']
        sizef = request.form['size']
        user = User(name=namef, price=pricef, size=sizef)

        # Add the user to the database
        session = Session()
        session.add(user)
        session.commit()

        # Query the database for all users
        users = session.query(User).all()

        # Print the users
        for user in users:
            print(user.name)
            print(user.price)
            print(user.size)
    return render_template('creat-article.html')


if __name__ == "__main__":
    app.run(debug=True)

