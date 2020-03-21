#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## flask + mongodb api for illness tracking
## Hüseyin Kilic
## a lot of help from https://github.com/fblupi/flask-and-mongodb-api-rest

from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

app.config['MONGO_URI'] = 'mongodb://root:gvOIqn8DJ8tvHz%!@localhost:27017/illness?authSource=admin'
# Disable redirecting on POST method from /illness to /illness/
app.url_map.strict_slashes = ''

mongo = PyMongo(app)

class Illness(Resource):
    def get(self, symptoms):
        illness = mongo.db.illness
        s = illness.find_one({'symptoms' : symptoms})
        if s:
            output = {'symptoms' : s['symptoms'], 'area' : s['area']}
        else:
            output = "No such symptoms"
        return jsonify({'result' : output})

class IllnessList(Resource):
    def get(self):
        illness = mongo.db.illness
        output = []
        for i in illness.find():
            output.append({'symptoms' : i['symptoms'], 'area' : i['area']})
        return jsonify({'result' : output})

    def post(self):
        illness = mongo.db.illness
        symptoms = request.json['symptoms']
        area = request.json['area']
        illness_id = illness.insert({'symptoms': symptoms, 'area': area})
        new_illness = illness.find_one({'_id': illness_id })
        output = {'symptoms' : new_illness['symptoms'], 'area' : new_illness['area']}
        return jsonify({'result' : output})

api.add_resource(IllnessList, '/illness')
api.add_resource(Illness, '/illness/<string:symptoms>')

if __name__ == '__main__':
    app.run(debug=True)
