import config

from data import build_report
from flask import Flask, Response
from flask_restful import Api, Resource
from helpers import convert_to_json, convert_to_xml, convert_racer_to_json

app = Flask(__name__)
api = Api(app)


def create_data():
    build_report('asc')


class RacerList(Resource):
    def get(self):
        return Response(convert_to_json(config.RACER_LIST), mimetype='application/json')


class RacerListXML(Resource):
    def get(self):
        return Response(convert_to_xml(config.RACER_LIST), mimetype='text/xml')


class Racer(Resource):
    def get(self, racer_abr):
        return Response(convert_racer_to_json(config.RACER_DICT[racer_abr]), mimetype='application/json')


api.add_resource(RacerList, '/report')
api.add_resource(RacerListXML, '/report-xml')
api.add_resource(Racer, '/report/<racer_abr>')


if __name__ == '__main__':
    create_data()
    app.run(debug=True)
