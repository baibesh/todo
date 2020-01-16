from flask import request
from flask_restful import Resource
from models import db, Tag, TagSchema, TaskTag, TaskTagSchema, Task, TaskSchema

tag_schema = TagSchema()
tags_schema = TagSchema(many=True)

task_tag_schema = TaskTagSchema()
tasks_tag_schema = TaskTagSchema(many=True)

task_schema = TaskSchema()

class TagsResource(Resource):
	def get(self):
		tags = Tag.query.all()

		tags = tags_schema.dump(tags)

		return { 'status':'success', 'data':tags }

	def post(self):
		json_data = request.get_json()

		if not json_data:
			return {'message':'No input data provided'}, 400

		tag = Tag.query.filter_by(name=json_data['name']).first()

		if tag:
			return { 'message': 'Tag already exists' }, 400

		new_tag = Tag(name=json_data['name'])

		db.session.add(new_tag)
		db.session.commit()

		tag_info = tag_schema.dump(new_tag)

		tag_id = tag_info['id']
		task_id = json_data['task_id']

		task = Task.query.filter_by(id=task_id).first()

		if not task:
			return {'message':'No task found!'}, 400

		new_taskTag = TaskTag(tag_id=tag_id, task_id=task_id)
		db.session.add(new_taskTag)
		db.session.commit()

		return { 'status':'success', 'data': tag_info }, 201

class TagResource(Resource):
	def get(self, id):
		tag = Tag.query.filter_by(id=id).first()
		tag = tag_schema.dump(tag)

		tasks_tag = TaskTag.query.filter_by(tag_id=tag['id']).all()
		tasks_tag = tasks_tag_schema.dump(tasks_tag)

		tasks = []

		for task_tag in tasks_tag:
			task = Task.query.filter_by(id=task_tag['task_id']).first()
			task = task_schema.dump(task)
			tasks.append(task)

		return { 'status':'success', 'tag':tag, 'tasks':tasks }