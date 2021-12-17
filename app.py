from get_data import get_data_from_db, get_racer_data_from_db
from flask import Flask, Response
from flask_restful import Api, Resource, abort
from helpers import convert_to_json, convert_to_xml, convert_racer_to_json
from flasgger import Swagger

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)


class RacerList(Resource):
    def get(self):
        return Response(convert_to_json(get_data_from_db()), mimetype='application/json')


class RacerListXML(Resource):
    def get(self):
        return Response(convert_to_xml(get_data_from_db()), mimetype='text/xml')


class Racer(Resource):
    def get(self, racer_abr):
        """
        file: app.yml
        """
        return Response(convert_racer_to_json(get_racer_data_from_db([racer_abr])), mimetype='application/json')


api.add_resource(RacerList, '/report')
api.add_resource(RacerListXML, '/report-xml')
api.add_resource(Racer, '/report/<racer_abr>')


if __name__ == '__main__':
    app.run(debug=True)
