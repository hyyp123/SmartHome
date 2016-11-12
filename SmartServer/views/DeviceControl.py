#! -*-coding=utf-8 -*-

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

        devicename="电饭煲"

        try:
            devicesDb = DevicesDbTable.objects.get(devicename=devicename)
        except DevicesDbTable.DoesNotExist:
            return HttpResponse(DeviceControl.deviceControlJsonHelper(0,"数据库中不存在该设备信息"))

        status = devicesDb.deviceStatus
        if status == 1:
            return HttpResponse(DeviceControl.deviceControlJsonHelper(0, "该设备已经启用"))

        raspberryId = devicesDb.raspberryId
        retValue = RaspberryControl.raspberryOn(raspberryId)

        if retValue == True:
            devicesDb.deviceStatus = 1
            devicesDb.save()
            return HttpResponse(DeviceControl.deviceControlJsonHelper(1,"设备启动成功"))
        else:
            return HttpResponse(DeviceControl.deviceControlJsonHelper(0, "设备启动失败"))


    @staticmethod
    def oneDeviceOff(request):

        devicename = "电饭煲"

        try:
            devicesDb = DevicesDbTable.object.gets(devicename=devicename)
        except DevicesDbTable.DoesNotExist:
            return HttpResponse(DeviceControl.deviceControlJsonHelper(0, "数据库中不存在该设备信息"))

        status = devicesDb.deviceStatus
        if status == 0:
            return HttpResponse(DeviceControl.deviceControlJsonHelper(0, "该设备已经关闭"))

        raspberryId = devicesDb.raspberryId
        retValue = RaspberryControl.raspberryOff(raspberryId)

        if retValue == True:
            devicesDb.deviceStatus = 0
            devicesDb.save()
            return HttpResponse(DeviceControl.deviceControlJsonHelper(1, "设备关闭成功"))
        else:
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

            raspberryId = devicesDb.raspberryId
            retValue = RaspberryControl.raspberryOn(raspberryId)

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

            raspberryId = devicesDb.raspberryId
            retValue = RaspberryControl.raspberryOff(raspberryId)

            if retValue == True:
                devicesDb.deviceStatus = 0
                devicesDb.save()

        return HttpResponse(DeviceControl.deviceControlJsonHelper(1, "所有的设备都尝试关闭"))
