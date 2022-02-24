#!/usr/bin/env python
from os import stat
import pymongo 
import flask
from flask import request
import jsonify


# Create the application.
APP = flask.Flask(__name__)
#Connect to the mongodb database
myclient = pymongo.MongoClient("mongodb://user:pass@server:port/dbname?retryWrites=false")
#get hold of database handle to perform db operations
mydb = myclient["mydb"]



@APP.route('/note', methods=['GET'])
def list():
    """ Display all the notes 
    """
    notes  = mydb["notes"].find()
    return jsonify({"notes":notes})

@APP.route('/note/<string:noteid>', methods=['GET'])
def read(noteid):
    """ Read one particular note
    """
    note = mydb["notes"].find_one({"id":noteid})
    return jsonify({"note":note})

@APP.route('/note', methods=['POST'])
def create():
    """ Create one note
    """
    notecontents = request.json["notecontents"]
    noteid = mydb["notes"].insert_one({"notecontents":notecontents})
    return jsonify({"noteid":noteid})

@APP.route('/note/<string:noteid>',methods=['PUT'])
def edit(noteid):
    """Save a modified note
    """
    notecontents = request.args.get('notecontents')
    status =  mydb["notes"].replace_one({'id': noteid}, {'notecontents':notecontents}, upsert=True)
    return jsonify({"successful":status})

@APP.route('/note/<string:noteid>', methods=['DELETE'])
def delete(noteid):
    """Delete a note
    """
    status = mydb["notes"].delete_one({'id': noteid})
    return jsonify({"success":status})

if __name__ == '__main__':
    APP.debug=True
    APP.run()