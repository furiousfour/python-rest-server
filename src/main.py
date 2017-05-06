import time
from notify import notify_signals_for_ambulance
from ambulance_status import get_list_of_occupied_ambulance

while 1:
    occupied_ambulance_list = get_list_of_occupied_ambulance('true') # 'true' for occupied and 'false for free'
    for ambulance in occupied_ambulance_list:
        notify_signals_for_ambulance(str(ambulance['latitude']),str(ambulance['longitude']),str(ambulance['vehicleID']))
    time.sleep(5)