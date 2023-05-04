 # -*- coding: utf-8 -*-
"""
Álvaro Pleguezuelos Escobar

PROGRAMACIÓN PARALELA EJERCICIOS MQTT

"""

from paho.mqtt.client import Client

TEMPERATURA = 'temperatura'
HUMIDITY = 'humedad'

def mensaje(mqttc, data, msg):
    print (f'mensaje:{msg.topic}:{msg.payload}:{data}')
    if data['status'] == 0:
        temp = int(msg.payload)
        if temp>data['temperatura_limite']:
            print(f'Se ha superado la temperatura limite {temp}, suscribiendo a humedad')
            mqttc.subscribe(HUMIDITY)
            data['status'] = 1
    elif data['status'] == 1:
        if msg.topic==HUMIDITY:
            humidity = int(msg.payload)
            if humidity>data['humedad_limite']:
                print(f'Se ha superado la humedad limite {humidity}, cancelando suscripción')
                mqttc.unsubscribe(HUMIDITY)
                data['status'] = 0
        elif TEMPERATURA in msg.topic:
            temp = int(msg.payload)
            if temp<=data['temperatura_limite']:
                print(f'temperatura {temp} por debajo del limite, cancelando suscripción')
                data['status']=0
                mqttc.unsubscribe(HUMIDITY)
                
def on_log(mqttc, data, level, buf, msg):
    print(f'LOG: {data}:{msg}')
    
def main(broker):
    data = {'temperatura_limite':30,
            'humedad_limite':100,
            'status': 0}
    mqttc = Client(userdata=data)
    mqttc.mensaje = mensaje
    mqttc.enable_logger()
    
    mqttc.connect(broker)
    mqttc.subscribe(f'{TEMPERATURA}/t1')
    mqttc.loop_forever()
    
if __name__ == "__main__":
    import sys
    if len(sys.argv)<2:
        print(f"Usage: {sys.argv[0]} broker")
        sys.exit(1)
    broker = sys.argv[1]
    main(broker)
