from data import build_report
from flask import Flask, Response
from flask_restful import Api, Resource
from helpers import convert_to_json, convert_to_xml

app = Flask(__name__)
api = Api(app)


def find_racer(racer):
    """looking for the right rider

    :param racer:
    :return: data right racer
    """
    racer_dict = create_racers_data()
    return racer_dict[racer]


def build_xml():
    return convert_to_xml(build_report(True))


def build_json():
    return convert_to_json(build_report(True))


class RacerList(Resource):
    def get(self):
        return Response(build_json(), mimetype='application/json')


class RacerListXML(Resource):
    def get(self):
        return Response(build_xml(), mimetype='text/xml')


api.add_resource(RacerList, '/report')
api.add_resource(RacerListXML, '/report-xml')


if __name__ == '__main__':
    app.run(debug=True)
