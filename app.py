from flask import Flask, Response, jsonify, request
from reader_writer import json_reader, json_writer
from posts.blueprint import post

app = Flask(__name__)
app.register_blueprint(post)


@app.route('/version')
def version():
    return '1.0'


@app.route('/people')
def people():
    country = request.args.get('country')
    if country is not None:
        return jsonify([p for p in json_reader()["people"]
                        if p['country'] == country])
    else:
        return jsonify(json_reader()["people"])


@app.route('/people/<int:id>', methods=['GET'])
def get_person(id):
    try:
        return json_reader()['people'][id]
    except IndexError:
        return Response('Not found', status=404)


@app.route('/people', methods=['POST'])
def post_people():
    person = request.get_json()
    person_id = len(json_reader()['people'])
    data = json_reader()
    data["people"].append({'id': person_id, **person})
    json_writer(data)
    print(json_reader())
    return jsonify({"id": person_id}), 201


@app.route('/people/<int:id>', methods=['DELETE'])
def delete_person(id):
    try:
        data = json_reader()
        data['people'][id] = None
        json_writer(data)
        return Response(status=204)
    except IndexError:
        return Response('Not found', status=404)


@app.route('/people/<int:id>', methods=['PATCH'])
def update_person(id):
    try:
        data = json_reader()
        data['people'][id].update(request.get_json())
        json_writer(data)
        return Response(status=204)
    except IndexError:
        return Response('Not found', status=404)


if __name__ == '__main__':
    app.run(debug=True)

