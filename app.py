from flask import Flask
from flask import render_template
from flask import request
from pony.orm import *
import json
import logging
import sqlite3

app = Flask(__name__)

db = Database()
db.bind('sqlite', 'bookmanager.db',create_db=True )

class Books(db.Entity):
    id = PrimaryKey(int, auto=True)
    title = Required(str)
    author = Required(str)

db.generate_mapping(create_tables=True)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/all')
@db_session
def all():
    all_books = select (e for e in Books)[:]
    return render_template('all.html', all_books=all_books)

@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/register', methods=['POST'])
@db_session
def register():
    new_book = Books(
        title = request.form['Title'],
        author = request.form['Author'],
    )
    commit()
    return render_template('submit.html')

@app.route('/update', methods=['POST'])
@db_session
def update():
    book = Books[request.form['id']]
    book.title = request.form['Title']
    book.author = request.form['Author']
    commit()

    return render_template('submit.html')

@app.route('/postmethod', methods = ['POST'])
@db_session
def get_post_json_data():
    js_data = request.json
    logging.info('js_data: ')
    logging.info(js_data)
    logging.info(type(js_data))
    for key in js_data:
        logging.info('ID: ' + js_data[key])
        Books[js_data[key]].delete()
    return 'get_post_json_data was successful'

@app.route('/book/<int:id>')
@db_session
def book(id):
    list = select (e for e in Books if e.id == id)[:]
    record = Books[id]
    return render_template('book.html', list=list)

if __name__ == "__main__":
    app.run(debug=True)


