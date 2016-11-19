#! -*- coding=utf -*-

from SmartServer.models import DevicesDbTable

import threading
import platform


class RaspberryControl(object):
    instance = None
    mutex = threading.Lock()

    def _init__(self):
        if platform.node() == 'raspberrypi':
            import RPi.GPIO as GPIO
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BOARD)

    @staticmethod
    def GetInstance():

        if (RaspberryControl.instance == None):
            RaspberryControl.mutex.acquire()
            if (RaspberryControl.instance == None):
                RaspberryControl.instance = RaspberryControl()
                RaspberryControl.mutex.release()

        return RaspberryControl.instance

    def raspberryOn(index):

        if platform.node() == 'raspberrypi':
            import RPi.GPIO as GPIO
            GPIO.output(index,GPIO.OUT)
            GPIO.output(index, GPIO.HIGH)
        print "下标为%d的树莓派已经启动" %index
        return True

    def raspberryOff(index):

        if platform.node() == 'raspberrypi':
            import RPi.GPIO as GPIO
            GPIO.output(index, GPIO.OUT)
            GPIO.output(index, GPIO.LOW)
        print "下标为%d的树莓派已经关闭" % index
        return True