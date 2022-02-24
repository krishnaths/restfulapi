#!/usr/bin/env python
from os import stat
import pymongo 
import flask
from flask import request, jsonify
from bson.json_util import dumps
import random


# Create the application.
APP = flask.Flask(__name__)
#Connect to the mongodb database
myclient = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.majex.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
#get hold of database handle to perform db operations
mydb = myclient["mydb"]



@APP.route('/note', methods=['GET'])
def list():
    """ Display all the notes 
    """
    notes  = mydb["notes"].find()
    return jsonify({"notes":dumps(notes)})

@APP.route('/note/<string:noteid>', methods=['GET'])
def read(noteid):
    """ Read one particular note
    """
    print(noteid)
    note = mydb["notes"].find_one({"noteid":int(noteid)})
    return jsonify({"note":dumps(note)})

@APP.route('/note', methods=['POST'])
def create():
    """ Create one note
    """
    noteid = random.randint(0,1000000000000000)
    notecontents = request.args["notecontents"]
    noteid = mydb["notes"].insert({"notecontents":notecontents, "noteid":noteid})
    return jsonify({"noteid":dumps(noteid)})

@APP.route('/note/<string:noteid>',methods=['PUT'])
def edit(noteid):
    """Save a modified note
    """
    notecontents = request.args.get('notecontents')
    print(notecontents)
    status =  mydb["notes"].update_one({'noteid': int(noteid)}, { "$set": {'notecontents':notecontents}})
    print((status.modified_count))
    return jsonify({"successful":dumps(status.modified_count)})

@APP.route('/note/<string:noteid>', methods=['DELETE'])
def delete(noteid):
    """Delete a note
    """
    status = mydb["notes"].delete_one({'noteid': int(noteid)})
    print(dir(status))
    return jsonify({"success":dumps(status.deleted_count)})

if __name__ == '__main__':
    APP.debug=True
    APP.run()