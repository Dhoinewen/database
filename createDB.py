from peewee import *
from dataclasses import asdict
from get_data import *


db = SqliteDatabase('Racers.db')


class RacerDB(Model):
    id = PrimaryKeyField(unique=True)
    start_time = DateTimeField()
    end_time = DateTimeField()
    full_name = CharField()
    racer_team = CharField()
    abbreviation = CharField()

    class Meta:
        database = db


def create_db():
    dict_list = list()
    for racers in build_report('asc'):
        dict_list.append(asdict(racers))
    db.connect()
    db.create_tables([RacerDB])
    RacerDB.insert_many(dict_list).execute()
    db.close()
