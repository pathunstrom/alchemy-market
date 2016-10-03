from flask import Flask, jsonify, request
import logging

from alchmark.errors import APIError
import alchmark.models as models


ALL_METHODS = ["GET", "POST", "PUTS", "DELETE"]


app = Flask(__name__)


@app.route('/')
def hello_world():
    return jsonify()


@app.route('/api/<obj>/', methods=ALL_METHODS, defaults={'identifier': None})
@app.route('/api/<obj>/<identifier>/', methods=ALL_METHODS)
def api(obj, identifier):
    cls = models.map.get(obj)
    payload = dict()
    if cls is None:
        raise APIError("Resource requested does not exist.")
    if request.method == "POST":
        resource = cls(id=identifier, **request.json)
        resource.create()
        payload[obj] = resource.as_dict()
    elif request.method == "GET":
        resource = cls.get(id=identifier)
        payload[obj] = resource.as_dict()
    elif request.method == "PUT":
        pass
    elif request.method == "DELETE":
        pass
    return jsonify(**payload)


@app.errorhandler(APIError)
def unknown_resource(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True)