from flask import Blueprint
from flask_restful import Api
from .domain import *
from .record_name import *
from .ttl import *
from .zone import *
from .record_data import *

api_blueprint = Blueprint("api", __name__, url_prefix='/api')
api = Api(api_blueprint)

api.add_resource(DomainCommand, '/domain')
api.add_resource(RecordName, '/namerecord')
api.add_resource(TtlName, '/ttl')
api.add_resource(ZoneName, '/zone')
api.add_resource(RecordData, '/datarecord')