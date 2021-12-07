import json

from dict2xml import dict2xml
from dataclasses import asdict
from datetime import datetime


def myconverter(o):
    if isinstance(o, datetime):
        return o.__str__()


def convert_to_json(racer_list):
    dict_list = list()
    for racers in racer_list:
        dict_list.append(asdict(racers))
    return json.dumps(dict_list, default=myconverter, indent=4)


def convert_to_xml(racer_list):
    dict_list = list()
    dict_for_xml = dict()
    for racers in racer_list:
        dict_list.append(asdict(racers))
    dict_for_xml['racer'] = dict_list
    return '<?xml version = "1.0" encoding = "UTF-8" standalone = "no"?>', dict2xml(dict_for_xml, wrap="racerList", indent="  ")