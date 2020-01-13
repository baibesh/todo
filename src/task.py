from flask import request
from flask_restful import Resource
from models import db, Task, TaskSchema, Item, ItemSchema, Attachment, AttachmentSchema, Tag, TagSchema, TaskTag, TaskTagSchema


task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

item_schema = ItemSchema()
items_schema = ItemSchema(many=True)

attachments_schema = AttachmentSchema(many=True)
tag_schema = TagSchema()
tasks_tag_schema = TaskTagSchema(many=True)


class TasksResource(Resource):
	def get(self):
		tasks = Task.query.all()
		tasks = tasks_schema.dump(tasks)

		result = []
		for task in tasks:

			task_data = {}
			item = Item.query.filter_by(id=task['item_id']).first()
			item = item_schema.dump(item)

			task_data['id'] = task['id']
			task_data['name'] = task['name']
			task_data['creation_date'] = task['creation_date']
			task_data['status'] = item
			result.append(task_data)

		return { 'status':'success', 'tasks': result }, 200

	def post(self):
		data = request.get_json()

		if not data:
			return {'message':'No input data provided'}, 400

		new_task = Task(name=data['name'], item_id=1)

		db.session.add(new_task)
		db.session.commit()

		return { 'status':'success' }, 201

class TaskResource(Resource):
	def get(self, id):
		task = Task.query.filter_by(id=id).first()
		
		if not task:
			return {'message':'No task found!'}

		task = task_schema.dump(task)

		item = Item.query.filter_by(id=task['item_id']).first()
		item = item_schema.dump(item)
		task['status'] = item

		attachments = Attachment.query.filter_by(task_id=task['id']).all()
		attachments = attachments_schema.dump(attachments)


		task_tags = TaskTag.query.filter_by(task_id=task['id']).all()
		task_tags = tasks_tag_schema.dump(task_tags)

		tags = []

		for tag in task_tags:
			tag_info = Tag.query.filter_by(id=tag['tag_id']).first()
			tag_info = tag_schema.dump(tag_info)
			tags.append(tag_info)


		return {'status':'success', 'task':task, 'attachments':attachments, 'tags':tags }

	def put(self, id):
		status = request.get_json()
		task = Task.query.filter_by(id=id).first()
		
		if not task:
			return {'message':'No task found!'}

		task.item_id = status['item_id']
		db.session.commit()

		task = Task.query.filter_by(id=id).first()
		task = task_schema.dump(task)

		return {'status':'success', 'task':task}



