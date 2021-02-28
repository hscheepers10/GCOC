import os
import time
import Adafruit_DHT
import RPi.GPIO as GPIO

#DHT Sensor setup, and DHT PIN
DHT_PIN1 = 4
DHT_SENSOR = Adafruit_DHT.AM2302

#GPIO Setup, and Relay PIN
relPin = 14
GPIO.setmode(GPIO.BCM)
GPIO.setup(relPin, GPIO.OUT)

#fan on
def fanOn(relPin):
    GPIO.output(relPin, GPIO.LOW)
    
#fan off
def fanOff(relPin):
    GPIO.output(relPin, GPIO.HIGH)

filename = time.strftime("%Y %m %d")

try:
    f = open('/home/pi/gcoc/gcoc_logs/gcoc_3 '+filename+'.csv', 'a+')
    if os.stat('/home/pi/'+filename+'.csv').st_size == 0:
            f.write('Date,Time,Temperature,Humidity\r\n')
except:
    pass

while True:
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN1)
    hum = int(humidity)
    temp = int(temperature)

    if humidity is not None and temperature is not None:
        print("Temp: {0:0.0f}*C      Humidity: {1:0.0f}%".format(temperature, humidity))
        f.write('{0},{1},{2:0.0f}*C,{3:0.0f}%\r\n'.format(time.strftime('%y/%m/%d'), time.strftime('%H:%M'), temperature, humidity))

        #----------------------TEST TEMP --------------------
        #IF TEMP is less than 40, fans stays OFF.  
        if temp < 40:
            fanOff(relPin)
            
        #IF TEMP goes over 50, fans go ON.  
        if temp > 50:
            fanOn(relPin)
            
        #----------------------------------------------------
        
    else:
        print("Failed, continuing...")
    
    time.sleep(10)      #Sleep for short test (30 seconds)
#     time.sleep(360)     #Sleep for long test (6 minutes)
GPIO.cleanup()
print("sequence finished...")


