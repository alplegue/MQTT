# -*- coding: utf-8 -*-
"""
Álvaro Pleguezuelos Escobar

PROGRAMACIÓN PARALELA EJERCICIOS MQTT

"""
from paho.mqtt.client import Client
from threading import Lock 
from time import sleep

def mensaje(mqttc, data, msg):
    print ('mensaje', msg.topic, msg.payload)
    n = len('temperatura/')
    lock = data['lock']
    lock.acquire()
    try:
        key = msg.topic[n:]
        if key in data:
            data['temperatura'][key].append(msg.payload)
        else:
            data['temperatura'][key]=[msg.payload]
    finally:
        lock.release()
    print ('mensaje', data)
    
def main(broker):
    data = {'lock':Lock(), 'temperatura':{}}
    mqttc = Client(userdata=data)
    mqttc.mensaje = mensaje
    mqttc.connect(broker)
    mqttc.subscribe('temperatura/#')
    mqttc.loop_start()
    
    while True:
        sleep(3)
        for key,temp in data['temperatura'].items():
            media = sum(map(lambda x: int(x), temp))/len(temp)
            print(f'media {key}: {media}')
            data[key]=[]
            
if __name__ == "__main__":
    import sys
    if len(sys.argv)<2:
        print(f"Usage: {sys.argv[0]} broker")
        sys.exit(1)
    broker = sys.argv[1]
    main(broker)