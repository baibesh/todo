from flask import Blueprint
from flask_restful import Api
from src.item import ItemResource
from src.task import TasksResource, TaskResource
from src.attachment import AttachmentResource
from src.tag import TagResource, TagsResource

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(ItemResource, '/item')
api.add_resource(TasksResource, '/task') 
api.add_resource(TaskResource, '/task/<id>')

api.add_resource(AttachmentResource, '/attachment')

api.add_resource(TagsResource, '/tag')
api.add_resource(TagResource, '/tag/<id>')