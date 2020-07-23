from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://kuei@localhost:5432/example'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(), nullable=False)

  def __repr__(self):
      return f'<User {self.id}, {self.name}>'


db.create_all()

#Implement a query to filter all users by name 'Bob'.
User.query.filter_by(name='Bob').all()

#Implement a LIKE query to filter the users for records with a name that includes the letter "b".
User.query.filter(User.name.like('%b%')).all()

#Return only the first 5 records of the query above.
User.query.limit(5).all()

#Re-implement the LIKE query using case-insensitive search.
User.query.filter(User.name.ilike('%b%')).all()

#Return the number of records of users with name 'Bob'.
User.query.filter(User.name.like('Bob')).count()