from flask import request
from flask_restful import Resource
from models import db, Item, ItemSchema
import simplejson as json

item_schema = ItemSchema()
items_schema = ItemSchema(many=True)

class ItemResource(Resource):
	def get(self):
		items = Item.query.all()
		items = items_schema.dump(items)

		return { 'status':'success', 'data': items }, 200

	def post(self):
		json_data = request.get_json()

		if not json_data:
			return {'message':'No input data provided'}, 400

		data, errors = item_schema.load(json_data)

		if errors:
			return {'message':'Category already exists'}, 400

		item = Item.query.filter_by(name=data['name']).first()
		if item:
			return { 'message': 'Item already exists' }, 400

		item = Item(name=json_data['name'])
		
		db.session.add(item)
		db.session.commit()

		result = item_schema.dump(item)

		return { 'status':'success', 'data': result }, 201

	def put(self):
		json_data = request.get_json()

		if not json_data:
			return { 'message': 'No input data provided!' }

		data, errors = item_schema.load(json_data)

		if errors:
			return errors, 422

		item = Item.query.filter_by(id=data['id']).first()
		
		if not item:
			return {'message':'Item doesnot exits!'}
		
		item.name = data['name']
		db.session.commit()

		result = item_schema.dump(item)

		return { 'status':'success', 'data':result }