from flask import Flask, render_template
#from flask_sqlachemy import SQLAlchemy
#from datetime import datetime


app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
#db = SQLAlchemy(app)


#class Article(db.Model):
 #   id = db.Column(db.Integer, primary_key=True)
  #  title = db.Column(db.String(100), primary_key=False)
   # intro = db.Column(db.String(300), primary_key=False)
   # text = db.Column(db.Text, nullable=False)
    #date = db.Column(db.DateTime, default=datetime.utcnow)

#    def __repr__(self):
 #       return '<Article %r>' % self.id

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


if __name__ == "__main__":
    app.run(debug=True)

