import json

from dict2xml import dict2xml
from datetime import datetime


def myconverter(o):
    if isinstance(o, datetime):
        return o.__str__()


def convert_racer_to_json(racer):
    return json.dumps(racer, default=myconverter, indent=4)


def convert_to_json(racer_list):
    return json.dumps(racer_list, default=myconverter, indent=4)


def convert_to_xml(racer_list):
    dict_for_xml = dict()
    dict_for_xml['racers'] = racer_list
    xml = '<?xml version = "1.0" encoding = "UTF-8" standalone = "no"?>' + dict2xml(dict_for_xml, wrap="racerList",
                                                                                    indent="  ")
    return xml
