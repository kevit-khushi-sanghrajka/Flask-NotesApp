from flask import Flask, request, render_template, redirect
from flask_pymongo import PyMongo
import datetime
from bson import ObjectId


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mydatabase"
mongo = PyMongo(app)

@app.route("/")
def home():
    notes = list(mongo.db.notes.find({}).sort("createdAt", -1))
    return render_template("/pages/home.html", homeIsActive=True, addNoteIsActive=False, notes=notes)

@app.route("/add-note", methods=['GET', 'POST'])
def addNote():
    if(request.method=="GET"):
        return render_template("pages/add-note.html",homeIsActive=False,addNoteIsActive=True)
    elif(request.method=="POST"):
        title = request.form['title']
        description = request.form['description']
        createdAt = datetime.datetime.now()

        mongo.db.notes.insert_one({"title": title, "description": description, "createdAt": createdAt})
        return redirect("/")
@app.route("/edit-note", methods=['GET', 'POST'])
def editNote():
    if(request.method == "GET"):
        noteId = request.args.get('form')
        note = dict(mongo.db.notes.find_one({"_id": ObjectId(noteId)}))

        # direct to edit note page
        return render_template('pages/edit-note.html',note=note)

    elif request.method == "POST":

        #get the data of the note
        noteId = request.form['_id']
        title = request.form['title']
        description = request.form['description']

        # update the data in the db
        mongo.db.notes.update_one({"_id":ObjectId(noteId)},{"$set":{"title":title,"description":description}})

        # redirect to home page
        return redirect("/")
        
@app.route('/delete-note', methods=['POST'])
def deleteNote():
     noteId = request.form['_id']

    # delete from the database
     mongo.db.notes.delete_one({ "_id": ObjectId(noteId)})

    # redirect to home page
     return redirect("/")


if __name__=="__main__":
    app.run(debug=True)