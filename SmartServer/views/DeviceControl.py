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
            return HttpResponse(DeviceControl.deviceControlJsonHelper(0,""))

        status = devicesDb.deviceStatus
        if status == 1:
            return HttpResponse(DeviceControl.deviceControlJsonHelper(0, ""))

        raspberryId = devicesDb.raspberryId
        retValue = RaspberryControl.raspberryOn(raspberryId)

        if retValue == True:
            devicesDb.deviceStatus = 1
            devicesDb.save()
            return HttpResponse(DeviceControl.deviceControlJsonHelper(1,"on success"))
        else:
            return HttpResponse(DeviceControl.deviceControlJsonHelper(0, "on fail"))


    @staticmethod
    def oneDeviceOff(request):

        devicename = "电饭煲"

        try:
            devicesDb = DevicesDbTable.object.gets(devicename=devicename)
        except DevicesDbTable.DoesNotExist:
            return HttpResponse(DeviceControl.deviceControlJsonHelper(0, ""))

        status = devicesDb.deviceStatus
        if status == 0:
            return HttpResponse(DeviceControl.deviceControlJsonHelper(0, ""))

        raspberryId = devicesDb.raspberryId
        retValue = RaspberryControl.raspberryOff(raspberryId)

        if retValue == True:
            devicesDb.deviceStatus = 0
            devicesDb.save()
            return HttpResponse(DeviceControl.deviceControlJsonHelper(1, "off success"))
        else:
            return HttpResponse(DeviceControl.deviceControlJsonHelper(0, "off fail"))

    @staticmethod
    def allDeviceOn(request):
        devicename = "电饭煲"

        try:
            devicesDbs = DevicesDbTable.objects.all()
        except DevicesDbTable.DoesNotExist:
            return HttpResponse(DeviceControl.deviceControlJsonHelper(0, ""))

        for devicesDb in devicesDbs:

            status = devicesDb.deviceStatus
            if status == 1:
                # return HttpResponse(DeviceControl.deviceControlJsonHelper(0, ""))
                continue

            raspberryId = devicesDb.raspberryId
            retValue = RaspberryControl.raspberryOn(raspberryId)

            if retValue == True:
                devicesDb.deviceStatus = 1
                devicesDb.save()
                # return HttpResponse(DeviceControl.deviceControlJsonHelper(1, "on success"))
            # else:
                # return HttpResponse(DeviceControl.deviceControlJsonHelper(0, "on fail"))

    @staticmethod
    def allDeviceOff(request):

        try:
            devicesDbs = DevicesDbTable.objects.all()
        except DevicesDbTable.DoesNotExist:
            return HttpResponse(DeviceControl.deviceControlJsonHelper(0, ""))

        for devicesDb in devicesDbs:

            status = devicesDb.deviceStatus
            if status == 0:
                # return HttpResponse(DeviceControl.deviceControlJsonHelper(0, ""))
                continue

            raspberryId = devicesDb.raspberryId
            retValue = RaspberryControl.raspberryOff(raspberryId)

            if retValue == True:
                devicesDb.deviceStatus = 0
                devicesDb.save()
                # return HttpResponse(DeviceControl.deviceControlJsonHelper(1, "on success"))
            # else:
                # return HttpResponse(DeviceControl.deviceControlJsonHelper(0, "on fail"))
