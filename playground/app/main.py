from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse

from db import *

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True

api = Api(app)
db = TinyDB('db.json')


class Cats(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("keywords", type=str, default='', required=True, help="Hey!")

    def get(self):
        return {"cats": get_cats(db)}, 200

    def post(self):
        keywords = Cats.parser.parse_args()["keywords"].replace(" ", "").split(',')
        cats = get_cats_by_description(db, *keywords)
        if len(cats) == 0:
            return {"msg": f"Failed! Cats with keywords {keywords} not found"}, 404
        else:
            return {"cats": cats}, 200


class Cat(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int, help='Specify cat id', location='args', required=True)


    def get(self):
        args = Cat.parser.parse_args()
        id = args["id"]
        result = get_cat_by_id(db, id)
        if result:
            return result, 200
        else:
            return {"msg": f"Failed! Cat with id {id} does not exist"}, 404

    def post(self):
        cat_data = request.get_json(force=True)
        cat_id = create_cat(db, cat_data)
        return {"msg": "Success!", "id": cat_id}, 201

    def delete(self):
        args = Cat.parser.parse_args()
        id = args["id"]
        cat_id = delete_cat(db, id)
        return {"msg": f"Success! Cat {cat_id} is removed"}, 200

    def put(self):
        args = Cat.parser.parse_args()
        id = args["id"]
        cat_data = request.get_json(force=True)
        if update_cat(db, id, cat_data):
            return {"msg": f"Success! Cat {id} is updated"}, 200
        else:
            return {"msg": f"Failed! Cats with i {id} does not exist"}, 404

class PetCat(Resource):
    def get(self, id, action):
        if action == 'hug':
            hug_cat(db,id)
        elif action == 'pet':
            pet_cat(db, id)
        else:
            yield {"msg": f"Failed! You are doing something wrong with the cat! You can only 'hug' or 'pet' the cat!"}


api.add_resource(Cats, '/cats')
api.add_resource(Cat, '/cat', endpoint='cat')
api.add_resource(PetCat,'/cat/{id}/{action}')

if __name__ == '__main__':
    app.run(port=8090, debug=True)
