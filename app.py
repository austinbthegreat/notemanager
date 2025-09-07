import pymongo
from flask import Flask, render_template, request, redirect
from datetime import datetime
from bson.objectid import ObjectId
from flask_moment import Moment
import os

app = Flask("notemanager")
moment = Moment(app)

client = pymongo.MongoClient(os.environ.get("MONGOSTRING"))
database = client.notemanager
collection = database["notes"]


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        allinfo = collection.find({})
        return render_template("index.html", allinfo=allinfo)
    else:
        data = request.form
        content = data["note"]
        timeadded = datetime.utcnow()
        collection.insert_one({"content": content, "timestamp": timeadded})
        return redirect("/")


# comments


@app.route("/delete")
def delete():
    noteid = request.args["noteid"]
    collection.delete_one({"_id": ObjectId(noteid)})
    return redirect("/")


app.run(debug=True)
