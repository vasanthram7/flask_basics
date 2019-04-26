from flask import Flask, request,render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config.update(
    SECRET_KEY='topsecret',
    #SQLALCHEMY_DATABASE_URI='<database>://<user_id>:<password>@<server>/<database_name>',
    SQLALCHEMY_DATABASE_URI='postgresql://postgres:topsecret@localhost/catalog_db',
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

db = SQLAlchemy(app)

#BASIC ROUTE
@app.route('/index')
@app.route('/')
def hello_flask():
    return  'Hello flask'

@app.route('/new/')
def query_strings(greeting='hello'):
    query_val=request.args.get('greeting', greeting)
    return '<h1> The greeting is: {0} </h1>'.format(query_val)

@app.route('/user')
@app.route('/user/<name>')
def no_query_string(name='mina'):
    return '<h1> The user name is: {} </h1>'.format(name)

@app.route('/text/<string:name>')
def working_with_stings(name):
    return '<h1> Here is the string:'+ name + '</h1>'

@app.route('/number/<int:num>')
def working_with_number(num):
    return '<h1> Here is the number:' + str(num) + '</h1>'

@app.route('/add/<int:num1>/<int:num2>')
def adding_int(num1,num2):
    return '<h1> The sum of passed value: {}'.format(num1 + num2)+'</h1>'

@app.route('/float/<float:num>')
def working_with_float(num):
    return '<h1> Here is floating point: ' + str(num) + '<h1>'

@app.route('/temp1')
def using_templates():
    return render_template('hello.html')

@app.route('/watch')
def top_movies():
    movie_list=['autopsy of jane doe',
                'neon demon',
                'ghost in a shell',
                'kong: skull island',
                'john wick 2',
                'spiderman - homecoming']
    return render_template('movies.html', movies=movie_list, name='Harry')

@app.route('/tables')
def movies_plus():
    movies_dict={'autospy of  jane doe': 02.14,
                 'neon demon': 3.20,
                 'ghost: skull island': 3.50,
                 'john wick 2': 02.52,
                 'spiderman - homecoming': 1.48}
    return render_template('table_data.html', movies=movies_dict, name='sally')

@app.route('/filters')
def filter_data():
        movies_dict={'autospy of  jane doe': 02.14,
                 'neon demon': 3.20,
                 'ghost: skull island': 3.50,
                 'john wick 2': 02.52,
                 'spiderman - homecoming': 1.48}
        return render_template('filter_data.html',movies = movies_dict,name=None,film = 'a christmas carol')

@app.route('/macros')
def jinja_macros():
    movies_dict = {'autospy of  jane doe': 02.14,
                 'neon demon': 3.20,
                 'ghost: skull island': 3.50,
                 'john wick 2': 02.52,
                 'spiderman - homecoming': 1.48}
    return render_template('using_macros.html', movies=movies_dict)

class Publication(db.Model):
    __tablename__ = 'publication'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return  'The Publisher Name is {}'.format(self.name)

class Book(db.Model):
    __tablename__ = 'book'

    id =  db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False, index=True)
    author = db.Column(db.String(350))
    avg_rating = db.Column(db.Float)
    format = db.Column(db.String(50))
    image = db.Column(db.String(100), unique=True)
    num_pages = db.Column(db.Integer)
    pub_date = db.Column(db.DateTime, default= datetime.utcnow())
    #Relationship
    pub_id  = db.Column(db.Integer, db.ForeignKey('publication.id'))

    def __init__(self, title, author, avg_rating, book_format, image, num_pages, pub_id):

     self.title = title
     self.author = author
     self.avg_rating = avg_rating
     self.format = book_format
     self.image = image
     self.num_pages = num_pages
     self.pub_id = pub_id

     def __repr__(self):
      return 'hi {} by {}'.format(self.title, self.author)



if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
