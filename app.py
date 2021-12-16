from data import build_report, create_racers_data, create_db
from flask import Flask, Response
from flask_restful import Api, Resource, abort
from helpers import convert_to_json, convert_to_xml, convert_racer_to_json
from flasgger import Swagger

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)


class RacerList(Resource):
    def get(self):
        return Response(convert_to_json(build_report('asc')), mimetype='application/json')


class RacerListXML(Resource):
    def get(self):
        return Response(convert_to_xml(build_report('asc')), mimetype='text/xml')


class Racer(Resource):
    def get(self, racer_abr):
        """
        file: app.yml
        """
        if racer_abr not in create_racers_data():
            abort(404, message="racer doesn't exist")
        return Response(convert_racer_to_json(create_racers_data()[racer_abr]), mimetype='application/json')


api.add_resource(RacerList, '/report')
api.add_resource(RacerListXML, '/report-xml')
api.add_resource(Racer, '/report/<racer_abr>')


if __name__ == '__main__':
    create_db()
    app.run(debug=True)
