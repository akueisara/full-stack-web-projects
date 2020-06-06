from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# postgresql://username:password@host:port/database_name
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://kuei@localhost:5432/example'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# db.Model lets us create and manipulate data models
class Person(db.Model):
  __tablename__ = 'persons'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(), nullable=False)

  # ability to customize a printable string (useful for debugging)
  def __repr__(self):
    return f'<Person ID: {self.id}, name: {self.name}>'

class User(db.Model):
  __tablename__ = 'users'
  name = db.Column(db.String(), nullable=False, unique=True)

class Product(db.Model):
  __tablename__ = 'products'
  price = db.Column(db.Float, db.CheckConstraint('price>0'))

# db.create_all() detects models and creates tables for them (if they don't exist)
db.create_all()

# db.session lets us create and manipulate database transactions
person = Person(name='Sara')
db.session.add(person)
db.session.commit()

@app.route('/')
def index():
  person = Person.query.first()
  return 'Hello ' + person.name

if __name__ == '__main__':
  app.run()