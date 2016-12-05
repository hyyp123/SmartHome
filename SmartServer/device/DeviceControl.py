#! -*-coding=utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import json

from django.http import Http404,HttpResponse

from SmartServer.models import DevicesDbTable
from SmartServer.raspberry.RaspberryControl import RaspberryControl

class DeviceControl(object):

    @staticmethod
    def deviceControlJsonHelper(value,info):
        item = {}
        item.setdefault("value",value)
        item.setdefault("info",info)
        return json.dumps(item)

    @staticmethod
    def oneDeviceOn(request):

        if request.method == 'GET':
            deviceName = request.GET['name']
            num = request.GET['num']

        try:
            devicesDb = DevicesDbTable.objects.get(deviceName=deviceName)
        except DevicesDbTable.DoesNotExist:
            return HttpResponse(DeviceControl.deviceControlJsonHelper(0,"数据库中不存在该设备信息"))

        status = devicesDb.deviceStatus
        if status == 1:
            print '%s 设备已经启动' %deviceName
            return HttpResponse(DeviceControl.deviceControlJsonHelper(0, "该设备已经启用"))

        pin = devicesDb.raspberryId
        retValue = RaspberryControl.GetInstance().raspberryOn(pin)

        if retValue == True:
            devicesDb.deviceStatus = 1
            devicesDb.save()
            print '%s 设备启动成功 ' %deviceName
            return HttpResponse(DeviceControl.deviceControlJsonHelper(1,"设备启动成功"))
        else:
            print "%s 设备启动失败" %deviceName
            return HttpResponse(DeviceControl.deviceControlJsonHelper(0, "设备启动失败"))


    @staticmethod
    def oneDeviceOff(request):

        if request.method == 'GET':
            deviceName = request.GET['name']
            num = request.GET['num']

        try:
            devicesDb = DevicesDbTable.objects.get(deviceName=deviceName)
        except DevicesDbTable.DoesNotExist:
            return HttpResponse(DeviceControl.deviceControlJsonHelper(0, "数据库中不存在该设备信息"))

        status = devicesDb.deviceStatus
        if status == 0:
            return HttpResponse(DeviceControl.deviceControlJsonHelper(0, "该设备已经关闭"))

        pin = devicesDb.raspberryId
        retValue = RaspberryControl.GetInstance().raspberryOff(pin)

        if retValue == True:
            devicesDb.deviceStatus = 0
            devicesDb.save()
            print "%s 设备关闭成功" %deviceName
            return HttpResponse(DeviceControl.deviceControlJsonHelper(1, "设备关闭成功"))
        else:
            print "%s 设备关闭失败" % deviceName
            return HttpResponse(DeviceControl.deviceControlJsonHelper(0, "设备关闭失败"))

    @staticmethod
    def allDeviceOn(request):

        try:
            devicesDbs = DevicesDbTable.objects.all()
        except DevicesDbTable.DoesNotExist:
            return HttpResponse(DeviceControl.deviceControlJsonHelper(0, "数据库中没有记录"))

        for devicesDb in devicesDbs:
            status = devicesDb.deviceStatus
            if status == 1:
                continue

            pin = devicesDb.raspberryId
            retValue = RaspberryControl.GetInstance().raspberryOn(pin)

            if retValue == True:
                devicesDb.deviceStatus = 1
                devicesDb.save()

        return HttpResponse(DeviceControl.deviceControlJsonHelper(1,"所有的设备都尝试启动"))


    @staticmethod
    def allDeviceOff(request):

        try:
            devicesDbs = DevicesDbTable.objects.all()
        except DevicesDbTable.DoesNotExist:
            return HttpResponse(DeviceControl.deviceControlJsonHelper(0, "数据库中没有记录"))

        for devicesDb in devicesDbs:

            status = devicesDb.deviceStatus
            if status == 0:
                continue

            pin = devicesDb.raspberryId
            retValue = RaspberryControl.GetInstance().raspberryOff(pin)

            if retValue == True:
                devicesDb.deviceStatus = 0
                devicesDb.save()

        return HttpResponse(DeviceControl.deviceControlJsonHelper(1, "所有的设备都尝试关闭"))
