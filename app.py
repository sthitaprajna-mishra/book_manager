import os

from flask import Flask, redirect, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

engine = create_engine("postgres://postgres:davidmalan@localhost:5432/lecture3")
db = scoped_session(sessionmaker(bind=engine))

@app.route("/", methods = ["POST", "GET"])
def index():
	if request.form:
		db.execute("INSERT INTO books(title) VALUES (:title)", {"title": request.form.get("title")})
		db.commit()
	books = db.execute("SELECT * FROM books").fetchall()
	return render_template("home.html", books = books)

@app.route("/update", methods = ["POST", "GET"])
def update():
	oldtitle = request.form.get("oldtitle")
	newtitle = request.form.get("newtitle")
	db.execute("UPDATE books SET title = :newtitle WHERE title = :oldtitle", {"oldtitle": oldtitle, "newtitle": newtitle})
	db.commit()
	return redirect("/")

@app.route("/delete", methods = ["POST", "GET"])
def delete():
	db.execute("DELETE FROM books WHERE title = :title", {"title": request.form.get("title")})
	db.commit()
	return redirect("/")

if __name__ == '__main__':
	app.run(debug = True)
