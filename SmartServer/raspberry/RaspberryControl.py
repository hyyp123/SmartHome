#! -*- coding=utf -*-
# improt RPi.GPIO as GPIO

class RaspberryControl(object):

    @staticmethod
    def raspberryOn(index):
        print "下标为%d的树莓派已经启动" %index
        return True

    @staticmethod
    def raspberryOff(index):
        print "下标为%d的树莓派已经关闭" % index
        return True