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
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(), nullable=False, unique=True)

class Product(db.Model):
  __tablename__ = 'products'
  id = db.Column(db.Integer, primary_key=True)
  price = db.Column(db.Float, db.CheckConstraint('price>0'))

# db.create_all() detects models and creates tables for them (if they don't exist)
db.create_all()

# db.session lets us create and manipulate database transactions
# person = Person(name='Sara')
# db.session.add(person)
# db.session.commit()

# add_all
# person1 = Person(name='New Person 1')
# person2 = Person(name='New Person 2')
# db.session.add_all([person1, person2])
# db.session.commit()

# all()
Person.query.all()

# first()
Person.query.first()

# filter_by
Person.query.filter_by(name='Amy')
person = Person.query.filter_by(name='Amy').first()
person.name

# filter
# MyModel.query.filter(MyOtherModel.some_attr=='some value')
User.query.filter(Product.id==3)

# order_by
# MyModel.order_by(MyModel.created_at)
# MyModel.order_by(db.desc(MyModel.created_at))

# limit
Person.query.limit(100).all()

# count
Person.query.count()

# delete
# Product.query.filter_by(category='Misc').delete()

# chaining
# Person.query.filter(Person.name == 'Amy').filter(Team.name == 'Udacity').first()
# Person.query is same as db.session.query(Person) 

# Driver.query.join('vehicles').filter_by(driver_id=3).all()

@app.route('/')
def index():
  person = Person.query.first()
  return 'Hello ' + person.name

if __name__ == '__main__':
  app.run()