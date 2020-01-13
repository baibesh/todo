from flask import Flask 
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

ma = Marshmallow()
db = SQLAlchemy()

class Item(db.Model):
	__tablename__ = 'items'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(250), unique=True, nullable=False)

	def __init__(self, name):
		self.name = name

class Task(db.Model):
	__tablename__ = 'tasks'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(250), nullable=False)
	creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
	item_id = db.Column(db.Integer, db.ForeignKey('items.id', ondelete='CASCADE'), nullable=False)

	def __init__(self, name, item_id):
		self.name = name
		self.item_id = item_id

class Tag(db.Model):
	__tablename__ = 'tags'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(250), nullable=False)

	def __init__(self, name):
		self.name = name

class Attachment(db.Model):
	__tablename__ = 'attachments'
	id = db.Column(db.Integer, primary_key=True)
	url = db.Column(db.String(255), nullable=False)
	task_id = db.Column(db.Integer, nullable=False)

	def __init__(self, url, task_id):
		self.url = url
		self.task_id = task_id

class TaskTag(db.Model):
	__tablename__ = 'task_tag'
	id = db.Column(db.Integer, primary_key=True)
	task_id = db.Column(db.Integer, db.ForeignKey('tasks.id', ondelete='CASCADE'), nullable=False)
	tag_id = db.Column(db.Integer, db.ForeignKey('tags.id', ondelete='CASCADE'), nullable=False)

	def __init__(self, task_id, tag_id):
		self.task_id = task_id
		self.tag_id = tag_id

class ItemSchema(ma.Schema):
	id = fields.Integer()
	name = fields.String(required=True)

class TaskSchema(ma.Schema):
	id = fields.Integer()
	name = fields.String(required=True)
	creation_date = fields.DateTime()
	item_id = fields.Integer(required=True)

class TagSchema(ma.Schema):
	id = fields.Integer()
	name = fields.String(required=True)

class AttachmentSchema(ma.Schema):
	id = fields.Integer()
	url = fields.String(required=True)
	task_id = fields.Integer()

class TaskTagSchema(ma.Schema):
	id = fields.Integer()
	task_id = fields.Integer(required=True)
	tag_id = fields.Integer(required=True)

