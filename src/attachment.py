from flask import request
from flask_restful import Resource, reqparse
from models import db, Attachment, AttachmentSchema, Task, TaskSchema

attachment_schema = AttachmentSchema()
attachments_schema = AttachmentSchema(many=True)

class AttachmentResource(Resource):
	def get(self):
		attachments = Attachment.query.all()
		attachments = attachments_schema.dump(attachments)

		return {'status':'success', 'attachments':attachments }

	def post(self):
		if 'file' in request.files:
			file = request.files['file'] 	# get file
			data = request.form 			# get data


			filename = secure_filename(file.filename)	# get filename
			url = os.path.join(os.path.abspath(os.path.dirname(__file__))+'/uploads', filename) 

			task_id = data['task_id']	

			task = Task.query.filter_by(id=task_id).first()

			if not task:
				return { 'message':'No task found!' }, 400

			if not file.save(url):
				return { 'message':'Error when saving a file' }, 400

			new_attachment = Attachment(url=url, task_id=task_id)

			db.session.add(new_attachment)
			db.session.commit()

			return { 'status':'success' }

		return { 'status':'No success!' }
