# -*- coding: utf-8 -*-
"""
Álvaro Pleguezuelos Escobar

PROGRAMACIÓN PARALELA EJERCICIOS MQTT

"""

import random
from paho.mqtt.client import Client
from time import sleep
from multiprocessing import Process, Manager

CLIENTES = 'clientes'
NUMEROS = 'numbers'
TIMER_STOP = f'{CLIENTS}/timerstop'
HUMEDAD = 'humedad'

def esprimo(n):    #funcion para ver si es o no primo un número
    i = 2
    while i*i < n and n % i != 0:
        i += 1
    return i*i > n

def temporizador(time, data):
    mqttc = Client()
    mqttc.connect(data['broker'])
    msg = f'Temporizador corriendo. timeout: {time}'
    print(msg)
    mqttc.publish(TIMER_STOP, msg)
    sleep(time)
    msg = f'Temporizador corriendo. timeout: {time}'
    mqttc.publish(TIMER_STOP, msg)
    print('Temporizador parado')
    mqttc.disconnect()

    
def on_log(mqttc, userdata, level, string):
    print("LOG", userdata, level, string)


def mensaje(mqttc, data, msg):
    print(f"MENSAJE:data:{data}, msg.topic:{msg.topic}, payload:{msg.payload}")
    try:
        #if esprimo(int(msg.payload)):
        if int(msg.payload) % 2 == 0:
            worker = Process(target=temporizador,
                             args=(random.random()*20, data))
            worker.start()
    except ValueError as e:
        print(e)
        pass
    
def main(broker):
    data = {'client':None,
            'broker': broker}
    mqttc = Client(userdata=data)
    data['client'] = mqttc
    mqttc.enable_logger()
    mqttc.mensaje = mensaje
    mqttc.on_log = on_log
    mqttc.connect(broker)
    mqttc.subscribe(NUMEROS)
    mqttc.loop_forever()
    
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} broker")
        sys.exit(1)
    broker = sys.argv[1]
    main(broker)