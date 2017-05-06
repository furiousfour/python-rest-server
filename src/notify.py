import datetime
import time
from pymongo import MongoClient
from geopy.geocoders import Nominatim

from get_closest import get_closet_signal_detail
import urllib2

client = MongoClient("ec2-13-228-23-221.ap-southeast-1.compute.amazonaws.com:27017")
db = client['greenway']


def notify_signals_for_ambulance(lat, long, vehicle_id):
    signal_detail = get_closet_signal_detail(lat, long)
    collection = db['traffic_signals_notification']
    if signal_detail != None:
        data = collection.find({"vehicleID": str(vehicle_id), "latitude": str(signal_detail['La_x']),
                                "longitude": str(signal_detail['Lo_x'])})
        if data.count() > 0 and (datetime.datetime.utcnow() - data['timestamp']).total_seconds() < 300:
            return
        point_for_data_first = (str(signal_detail['La_x']), str(signal_detail['Lo_x']))
        geolocator = Nominatim()
        collection_second = db['assigned_ambulance']
        data_second = collection_second.find_one({"vehicleID": id})
        current_location = geolocator.reverse(point_for_data_first).address
        collection.insert({"vehicleID": str(vehicle_id), "latitude": str(signal_detail['La_x']),
                           "longitude": str(signal_detail['Lo_x']), "current_location": current_location,
                           "destination": str(data_second['des_name']), "timestamp": datetime.datetime.utcnow()})

        # make call with phonenumber, id_of_vehicle
        # urllib2.urlopen("/api/makecall/signal_detail['Lo_x']/{id_of_ambulance}").read()
