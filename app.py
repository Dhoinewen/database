import json

from xml.etree import cElementTree
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from pathlib import Path
from flask import Flask, Response
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

DIVISION = 15


@dataclass
class Racer:
    start_time: datetime = field(default=None)
    end_time: datetime = field(default=None)
    full_name: str = field(default="")
    racer_team: str = field(default="")
    abbreviation: str = field(default="")

    @property
    def lap_time(self):
        lap_time = self.end_time - self.start_time
        if lap_time.days < 0:
            lap_time = timedelta.max
        return lap_time


def get_key_value(reverse):
    """sort racers with errors in data

    :param reverse:
    :return: params for right sort
    """
    def get_value(obj):
        value = obj.lap_time
        if reverse and value == timedelta.max:
              value = timedelta.min
        return value
    return get_value


def read_from_files(path):
    d = Path(__file__).resolve().parent
    filepath = d / 'data' / path
    with open(filepath, 'r') as f:
        return f.readlines()


def create_racers_data():
    racer_dict = {}
    datetime_format = '%Y-%m-%d_%H:%M:%S.%f'
    file = read_from_files('start.log')
    for line in file:
        abbr = line[:3].rstrip()
        start_time = datetime.strptime(line[3:].rstrip(), datetime_format)
        racer_dict[abbr] = Racer(abbreviation=abbr, start_time=start_time)

    file = read_from_files("end.log")
    for line in file:
        abbr = line[:3].rstrip()
        end_time = datetime.strptime(line[3:].rstrip(), datetime_format)
        racer_dict[abbr].end_time = end_time

    file = read_from_files("end_name.txt")
    for line in file:
        abbr, full_name, team = line.strip().split("_")
        racer_dict[abbr].full_name = full_name
        racer_dict[abbr].racer_team = team
    return racer_dict


def build_report(sorting_type):
    """Built Racer_list and sort it.

    Return sorted racer_list
    """
    racer_dict = create_racers_data()
    racer_list = [clases for clases in racer_dict.values()]
    racer_list.sort(key=get_key_value(sorting_type), reverse=sorting_type)
    return racer_list


def find_racer(racer):
    """looking for the right rider

    :param racer:
    :return: data right racer
    """
    racer_dict = create_racers_data()
    return racer_dict[racer]


def print_racer(racer):
    """Print data for solo racer   """
    print(racer.full_name, " | ", racer.racer_team, " | ", racer.lap_time)


def myconverter(o):
    if isinstance(o, datetime):
        return o.__str__()


def conver_to_json():
    dict_list = list()
    for racers in build_report(True):
        dict_list.append(asdict(racers))
    return json.dumps(dict_list, default=myconverter, indent=4)


def convert_to_xml():
    dict_list = list()
    for racers in build_report(True):
        dict_list.append(asdict(racers))
    xml = cElementTree.Element('racerList')
    for racers in dict_list:
        xml_racer = cElementTree.SubElement(xml, 'racer')
        xml_racer.attrib = {'abbreviation': racers['abbreviation']}
        for elem in racers:
            xml_data_racer = cElementTree.SubElement(xml_racer, elem)
            xml_data_racer.text = myconverter(racers[elem])
    return cElementTree.dump(xml)


def start_report():
    """Start program"""
    return conver_to_json()


class RacerList(Resource):
    def get(self):
        return Response(conver_to_json(), mimetype='application/json')


class RacerListXML(Resource):
    def get(self):
        return Response(convert_to_xml(), mimetype='text/xml')


api.add_resource(RacerList, '/report')
api.add_resource(RacerListXML, '/report-xml')


if __name__ == '__main__':
    app.run(debug=True)
