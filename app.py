from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from flask import Flask, render_template, redirect
from flask_restful import reqparse, abort, Api, Resource
import wikipedia


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


@app.route('/report')
def start_report():
    """Start program"""
    racer_list = build_report(False)
    return render_template('report.html', racer_list=racer_list)


@app.route('/report/<string:abbreviation>')
def racer_info(abbreviation):
    racer_data = find_racer(abbreviation)
    return redirect(wikipedia.page(racer_data.full_name).url, code=404)


if __name__ == '__main__':
    app.run(debug=True)
