from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from ispyb.model_list import model_list
from ispyb import db

class ISPyBModelView(ModelView):
    column_exclude_list = ('externalId')

def init_app(app):
    admin = Admin(app, name='ISPyB Models', template_mode='bootstrap3')

    for model in model_list:
        admin.add_view(ISPyBModelView(model, db.session))
