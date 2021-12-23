from create_db import db, RacerDB


def get_racers_data_from_db():
    db.connect()
    racer_list = list()
    data_from_db = RacerDB.select()
    for racers in data_from_db:
        dict = {'start_time': racers.start_time,
                'end_time': racers.end_time,
                'full_name': racers.full_name,
                'racer_team': racers.racer_team,
                'abbreviation': racers.abbreviation}
        racer_list.append(dict)
    db.close()
    return racer_list


def get_racer_data_from_db(racer_abr):
    db.connect()
    data = RacerDB.get_or_none(RacerDB.abbreviation == racer_abr)
    if data == None:
        return data
    racer = {'start_time': data.start_time,
             'end_time': data.end_time,
             'full_name': data.full_name,
             'racer_team': data.racer_team,
             'abbreviation': data.abbreviation}
    db.close()
    return racer
