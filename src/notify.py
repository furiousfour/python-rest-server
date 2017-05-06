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
                                "longitude": str(signal_detail['Lo_x'])}).sort("_id",-1)
        try:
            if data.count() > 0 and (datetime.datetime.utcnow() - data[0]['timestamp']).total_seconds() < 300:
                return
        except Exception as inst:
            print inst
        point_for_data_first = (str(signal_detail['La_x']), str(signal_detail['Lo_x']))
        geolocator = Nominatim()
        collection_second = db['assigned_ambulance']
        data_second = collection_second.find_one({"vehicle_id": str(vehicle_id)})
        current_location = geolocator.reverse(point_for_data_first).address
        # print point_for_data_first
        collection.insert({"vehicleID": str(vehicle_id), "latitude": str(signal_detail['La_x']),
                           "longitude": str(signal_detail['Lo_x']), "current_location": str(current_location),
                           "destination": str(data_second['des_name']), "timestamp": datetime.datetime.utcnow()})

        # make call with phonenumber, id_of_vehicle
        phn = str(signal_detail['phone_no'])

        # localhost:3000 / api / makeCall?phonenumber = +919108665075 & ambulanceid = 100
        out=urllib2.urlopen("http://13.228.23.221/api/makeCall?phonenumber="+phn+"&ambulanceid="+vehicle_id)

# def mod():
#     urllib2.urlopen("http://52.77.53.23:9000/test/100/test.xml")
# mod()
