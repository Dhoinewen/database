from dataclasses import dataclass, field
from datetime import datetime, timedelta
import os
from flask import Flask, render_template, redirect
import wikipedia


app = Flask(__name__)

DIVISION = 15


""" def args():
    Settings for terminal

    :return: terminal params
    
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--asc", help="Show all list in asc", default=False, action="store_false", dest="order")
    group.add_argument("--desc", help="Show all list in asc", default=False, action="store_true", dest="order")
    parser.add_argument("-r", "--racer", help="Search racer", default=None, type=str, dest="racer")
    args = parser.parse_args()
    return args
    """


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


def read_from_files():
    """Read data from files

    :return: racer_dict with all data
    """
    racer_dict = {}
    datetime_format = '%Y-%m-%d_%H:%M:%S.%f'
    file_path = os.path.join(os.path.dirname(__file__), "data")
    with open(os.path.join(file_path, "start.log"), "r") as file:
        for line in file:
            abbr = line[:3].rstrip()
            start_time = datetime.strptime(line[3:].rstrip(), datetime_format)
            racer_dict[abbr] = Racer(abbreviation=abbr, start_time=start_time)

    with open(os.path.join(file_path, "end.log"), "r") as file:
        for line in file:
            abbr = line[:3].rstrip()
            end_time = datetime.strptime(line[3:].rstrip(), datetime_format)
            racer_dict[abbr].end_time = end_time

    with open(os.path.join(file_path, "end_name.txt"), "r") as file:
        for line in file:
            abbr, full_name, team = line.strip().split("_")
            racer_dict[abbr].full_name = full_name
            racer_dict[abbr].racer_team = team
    return racer_dict


def build_report(sorting_type):
    """Built Racer_list and sort it.

    Return sorted racer_list
    """
    racer_dict = read_from_files()
    racer_list = [clases for clases in racer_dict.values()]
    racer_list.sort(key=get_key_value(sorting_type), reverse=sorting_type)
    return racer_list


def find_racer(racer):
    """looking for the right rider

    :param racer:
    :return: data right racer
    """
    racer_dict = read_from_files()
    return racer_dict[racer]


def print_report(racer_list):
    """print sorted list of racers

    :param racer_list:
    """
    """
    for position, clases in enumerate(racer_list, 1):
        print('{0:<3}| {1:<20}| {2:<30}|'.format(position, clases.full_name, clases.racer_team), clases.lap_time)
        if position == DIVISION:
            print('-' * 15)
    """


def print_racer(racer):
    """Print data for solo racer   """
    print(racer.full_name, " | ", racer.racer_team, " | ", racer.lap_time)


@app.route('/report')
def start_report():
    """Start program"""
    """if args().racer is None:
        racer_list = build_report(args().order)
        print_report(racer_list)
    else:
        racer_list = find_racer(args().racer)
        print_racer(racer_list)"""
    racer_list = build_report(True)
    print_report(racer_list)
    return render_template('report.html', racer_list=racer_list)


@app.route('/report/<string:abbreviation>')
def racer_info(abbreviation):
    racer_data = find_racer(abbreviation)
    return redirect(wikipedia.page(racer_data.full_name).url, code=404)


if __name__ == '__main__':
    app.run(debug=True)
    "start_report()"
