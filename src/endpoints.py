import urllib2

from flask import Flask
from pymongo import MongoClient
from flask import Response
from geopy.geocoders import Nominatim

from ambulance_status import get_list_of_occupied_ambulance
from get_closest import get_closet_ambulance_detail

app = Flask(__name__)


@app.route('/assign-ambulance/<lat>/<longi>')
def assign_ambulance(lat, longi):
    client = MongoClient("ec2-13-228-23-221.ap-southeast-1.compute.amazonaws.com:27017")
    db = client['greenway']
    collection_first = db['assigned_ambulance']
    geolocator = Nominatim()
    list_of_free_ambulance = get_list_of_occupied_ambulance('false')
    ambulance_detail = get_closet_ambulance_detail(lat, longi, list_of_free_ambulance)
    des = geolocator.reverse((lat, longi)).address
    print "I am here"
    print ambulance_detail
    if ambulance_detail is not None:
        print (
            "http://54.169.6.96/api/vehicle/alert?vehicleID=" + str(ambulance_detail['vehicleID']) + "&latitude=" +
            ambulance_detail['latitude'] + "&longitude=" + ambulance_detail['longitude'] + "&locationName=" + des)
        # urllib2.urlopen("http://54.169.6.96/api/vehicle/alert?vehicleID=" + str(ambulance_detail['vehicleID']) + "&latitude=" +str(ambulance_detail['latitude']) + "&longitude=" + str(ambulance_detail['longitude']) + "&locationName=SP InfoCity")
        urllib2.urlopen("http://54.169.6.96/api/vehicle/alert?vehicleID=124&latitude=" + str(
            ambulance_detail['latitude']) + "&longitude=" + str(ambulance_detail['longitude']) + "&locationName=SP Infocity")

    return 'success'


@app.route('/test/<ambulance_id>/test.xml', methods=['POST'])
def give_greetingss(ambulance_id):
    client = MongoClient("ec2-13-228-23-221.ap-southeast-1.compute.amazonaws.com:27017")
    db = client['greenway']
    collection_first = db['traffic_signals_notification']
    data_first = collection_first.find_one({"vehicleID": ambulance_id})
    source = data_first['current_location']
    destination = data_first['destination']
    response = '<?xml version="1.0" encoding="UTF-8" ?><Response><Say voice="alice">An ambulance is heading from ' + source + ' to place ' + destination + '. Please Clear the traffic. Thank you.</Say></Response>'
    return Response(response, mimetype='text/xml')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9000)
