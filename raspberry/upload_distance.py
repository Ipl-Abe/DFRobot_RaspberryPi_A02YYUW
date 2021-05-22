#!/usr/bin/python
# -*- coding:utf-8 -*-

'''
  # demo_get_distance.py
  #
  # Connect board with raspberryPi.
  # Run this demo.
  #
  # Connect A02 to UART
  # get the distance value
  #
  # Copyright   [DFRobot](http://www.dfrobot.com), 2016
  # Copyright   GNU Lesser General Public License
  #
  # version  V1.0
  # date  2019-8-31
'''

import json
import requests
import os
import time
import math
import csv

from DFRobot_RaspberryPi_A02YYUW import DFRobot_A02_Distance as Board


def print_distance(dis):
  if board.last_operate_status == board.STA_OK:
    print("Distance %d mm" %dis)
  elif board.last_operate_status == board.STA_ERR_CHECKSUM:
    print("ERROR")
  elif board.last_operate_status == board.STA_ERR_SERIAL:
    print("Serial open failed!")
  elif board.last_operate_status == board.STA_ERR_CHECK_OUT_LIMIT:
    print("Above the upper limit: %d" %dis)
  elif board.last_operate_status == board.STA_ERR_CHECK_LOW_LIMIT:
    print("Below the lower limit: %d" %dis)
  elif board.last_operate_status == board.STA_ERR_DATA:
    print("No data!")



if __name__ == "__main__":

    # path to API_KEY
    home = os.path.expanduser("~")
    print(home)
    path = home +'/.API_KEYS/machinist_keys.json'
    f = open(path)
    json_data = json.load(f)
    data = json_data['keys']
    Authorization_str = 'Bearer'+ ' ' + data['API_KEY']

    # make header
    req_header = {
        'Content-Type': 'application/json',
        'Authorization': Authorization_str,
    }

    # make data
    req_data = json.dumps(
    {
      "agent": "Home",
      "metrics": [
        {
          "name": "temperature",
          "namespace": "Environment Sensor",
          "data_point": {
            "value": 30.6
          }
        }
      ]
    })

    url_machinist = "https://gw.machinist.iij.jp/endpoint"

    # post with header
    #req = requests.post(url_machinist, data=req_data, headers=req_header)
    # print status
    #print("data posted." + " status:", req.status_code)
    #print("check status? 200->ok! 4**->bad!")
    
    print ("program start")

    board = Board()
    dis_min = 0   #Minimum ranging threshold: 0mm
    dis_max = 4500 #Highest ranging threshold: 4500mm
    board.set_dis_range(dis_min, dis_max)
   
    start = time.time()
    time_out = 300

    f = open('time.csv', 'w')

    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(['start time','current time'])

    while True:
        distance = board.getDistance()
        time.sleep(0.3)
        
       #writer = csv.writer(f, lineterminator='\n')

        
        #writer.writerow(['start time','current time'])
       # print("time", time.time())
        
        
       # print("abs time : ", abs(time.time() - start))
        if time.time() - start > 60:
            print("start time",start)
            start = time.time()

            req_data = json.dumps(
            {
              "agent": "Home",
              "metrics": [
                {
                  "name": "water level",
                  "namespace": "Ultrasonic wave sensor",
                  "data_point": {
                    "value": distance
                  }
                }
              ]
            })
            req = requests.post(url_machinist, data=req_data, headers=req_header)
            print_distance(distance)
      #time.sleep(0.3) #Delay time < 0.6s
        elif abs(start - time.time()) > time_out:
            start = time.time()
        else:
            if abs(start - time.time()) > 50:
                print("start time ", start)
                print("current time ", time.time())
                writer.writerow([start,time.time()])
            pass

       # print (start)
       # print (time.time())
