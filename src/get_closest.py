from geopy.distance import great_circle
from pymongo import MongoClient

client = MongoClient("ec2-13-228-23-221.ap-southeast-1.compute.amazonaws.com:27017")
db = client['greenway']


def get_closet_signal(lat, long, collection):
    THRESHOLD = 1
    source = (lat, long)
    cursor = collection.find({})
    list_of_signals_coordinates = list(map(lambda x: (x['La_x'], x['Lo_x']), cursor))
    data = get_closet(list_of_signals_coordinates, source, THRESHOLD)
    # print data
    if len(data) > 0:
        return min(data, key=data.get)
    return 0, 0


def get_closet(list_of_signals_coordinates, source, threshold):
    data = {}
    for point in list_of_signals_coordinates:
        kilometers = great_circle(source, point).kilometers
        if kilometers < threshold:
            data[point] = kilometers
    return data


def get_closet_ambulance_detail(lat, long, list_of_free_ambulance):
    collection = db['traffic_signals']
    source = (lat, long)
    list_of_ambulance_coordinates = list(map(lambda x: [(x['latitude'], x['longitude'])], list_of_free_ambulance))
    lat, long = get_closet_ambulance(list_of_ambulance_coordinates, source)
    if lat == 0 and long == 0:
        return None
    cursor = collection.find_one({'La_x': lat, 'Lo_x': long})
    return cursor


def get_closet_ambulance(list_of_ambulance_coordinates, source):
    data = get_closet(list_of_ambulance_coordinates, source, 100)
    if len(data) > 0:
        return min(data, key=data.get)
    return 0, 0


def get_closet_signal_detail(lat, long):
    collection = db['traffic_signals']
    lat, long = get_closet_signal(lat, long, collection)
    if lat == 0 and long == 0:
        return None
    cursor = collection.find_one({'La_x': lat, 'Lo_x': long})
    return cursor


# get_signal_detail(13.085634, 80.262869)
def get_closet_hospital(lat, long):
    source = (lat, long)
    collection = db['amenities_position']
    cursor = collection.find({"properties.type": "hospital"})
    list_of_hospital_coordinates = list(map(lambda x: (x['la'], x['lo']), cursor))
    data = get_closet(list_of_hospital_coordinates, source, 0)
    return min(data, key=data.get)

# get_closet_hospital(2,3)
