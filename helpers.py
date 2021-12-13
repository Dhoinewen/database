import json

from dict2xml import dict2xml
from dataclasses import asdict
from datetime import datetime


def myconverter(o):
    if isinstance(o, datetime):
        return o.__str__()


def convert_racer_to_json(racer):
    return json.dumps(asdict(racer), default=myconverter, indent=4)


def convert_to_json(racer_list):
    dict_list = list()
    for racers in racer_list:
        dict_list.append(asdict(racers))
    return json.dumps(dict_list, default=myconverter, indent=4)


def convert_to_xml(racer_list):
    racers_dict = dict()
    dict_for_xml = dict()
    for racers in racer_list:
        racers_dict[racers.abbreviation] = asdict(racers)
    dict_for_xml['racers'] = racers_dict
    xml = '<?xml version = "1.0" encoding = "UTF-8" standalone = "no"?>' + dict2xml(dict_for_xml, wrap="racerList",
                                                                                    indent="  ")
    return xml
