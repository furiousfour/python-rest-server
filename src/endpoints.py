from flask import Flask
from pymongo import MongoClient
from flask import Response

from ambulance_status import get_list_of_occupied_ambulance
from get_closest import get_closet_ambulance_detail

app = Flask(__name__)


@app.route('/assign-ambulance/<lat>/<longi>')
def assign_ambulance(lat, longi):
    list_of_free_ambulance = get_list_of_occupied_ambulance('false')
    lat, longi = get_closet_ambulance_detail(lat, longi, list_of_free_ambulance)
    if list_of_free_ambulance is not None:
    # make a url get call to the
    return 'success'


@app.route('/test/<ambulance_id>/test.xml', methods=['POST'])
def give_greetingss(ambulance_id):
    client = MongoClient("ec2-13-228-23-221.ap-southeast-1.compute.amazonaws.com:27017")
    db = client['greenway']
    collection_first = db['traffic_signals_notification']
    data_first = collection_first.find_one({"vehicleID": id})
    source = data_first['current_location']
    destination = data_first['destination']
    response = '<?xml version="1.0" encoding="UTF-8" ?><Response><Say voice="alice">An ambulance is heading from ' + source + ' to place ' + destination + '. Please Clear the traffic. Thank you.</Say></Response>'
    return Response(response, mimetype='text/xml')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9000)
