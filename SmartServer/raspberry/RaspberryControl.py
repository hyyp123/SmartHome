#! -*- coding=utf -*-
import threading
import platform

from SmartServer.models import DevicesDbTable

class RaspberryControl(object):
    instance = None
    mutex = threading.Lock()

    def _init__(self):
        if platform.node() == 'raspberrypi':
            import RPi.GPIO as GPIO
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BOARD)
            print "raspberrypi运行"
        else:
            print "非raspberrypi运行"

    @staticmethod
    def GetInstance():

        if (RaspberryControl.instance == None):
            RaspberryControl.mutex.acquire()
            if (RaspberryControl.instance == None):
                RaspberryControl.instance = RaspberryControl()
                RaspberryControl.mutex.release()

        return RaspberryControl.instance

    def raspberryOn(self,index):

        if platform.node() == 'raspberrypi':
            import RPi.GPIO as GPIO
            GPIO.setup(index,GPIO.OUT)
            GPIO.output(index, GPIO.HIGH)
            print "raspberrypi运行"
        else:
            print "非raspberrypi运行"
        print "下标为%d的树莓派已经启动" %index
        return True

    def raspberryOff(self,index):

        if platform.node() == 'raspberrypi':
            import RPi.GPIO as GPIO
            GPIO.setup(index, GPIO.OUT)
            GPIO.output(index, GPIO.LOW)
            print "raspberrypi运行"
        else:
            print "非raspberrypi运行"
        print "下标为%d的树莓派已经关闭" % index
        return True