from geopy.distance import great_circle
from pymongo import MongoClient
from bson.son import SON

THRESHOLD = 1
client = MongoClient("ec2-13-228-23-221.ap-southeast-1.compute.amazonaws.com:27017")
db = client['greenway']


def get_list_of_occupied_ambulance(value):
    collection = db['gpslog']
    pipeline=[
        {
    "$match": {'isOccupied': value}
    }
    , {
    "$sort": SON([("timestamp", -1)])
    }
    , {
    "$group": {
        'originalId': {"$first": "$_id"},
    '_id': '$vehicleID',
         "latitude": {'$first': '$latitude'},
    "longitude":  {'$first': '$longitude'},
    "speed":  {'$first': '$speed'},
    "heading":  {'$first': '$heading'},
    "accuracy":  {'$first': '$accuracy'},
    "timestamp": {'$first': '$timestamp'}
    }

    }, {
   "$sort": SON([("timestamp", -1)])
    }
    , {
    "$project":{
        '_id': '$originalId',
        'vehicleID': '$_id',
        'latitude': '$latitude',
        'longitude': '$longitude',
        'speed': '$speed',
        'heading': '$heading',
        'accuracy': '$accuracy',
        'timestamp': '$timestamp'
         }
    }
    ]
    cursor= db.command('aggregate', 'gpslog', pipeline=pipeline, explain=False)
    return cursor['result']

# print get_list_of_occupied_ambulance('true')