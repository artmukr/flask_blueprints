from flask import Response, jsonify, request, Blueprint
from reader_writer import json_reader, json_writer

post = Blueprint('post', __name__)


@post.route('/posts')
def posts():
    data = json_reader()['posts']
    return jsonify(data)


@post.route('/posts/<int:id>')
def get_posts(id):
    try:
        return json_reader()['posts'][id]
    except IndexError:
        return Response('Not found', status=404)


@post.route('/posts', methods=['POST'])
def post_posts():
    person = request.get_json()
    person_id = len(json_reader()['posts'])
    data = json_reader()
    data["posts"].append({'id': person_id, **person})
    json_writer(data)
    print(json_reader())
    return jsonify({"id": person_id}), 201


@post.route('/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    try:
        data = json_reader()
        data['posts'][id] = None
        json_writer(data)
        return Response(status=204)
    except IndexError:
        return Response('Not found', status=404)


@post.route('/posts/<int:id>', methods=['PATCH'])
def update_post(id):
    try:
        data = json_reader()
        data['posts'][id].update(request.get_json())
        json_writer(data)
        return Response(status=204)
    except IndexError:
        return Response('Not found', status=404)


@post.route('/people/<int:id>/posts')
def peoples_post(id):
    data = json_reader()['posts'][id]
    return data['title']
