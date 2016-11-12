#!-*- coding=utf-8 -*-

import json

from django.http import Http404,HttpResponse

from SmartServer.models import DevicesDbTable


class DevicesChange(object):

    @staticmethod
    def devicesChangeJosnHelper(value,info):
        item = {}
        item.setdefault("value",value)
        item.setdefault("info",info)
        # item.setdefault("other",other)
        return json.dumps(item)

    @staticmethod
    def addDevice(request):

        body1 = {"name":"电饭煲","status":"0"}
        # body2 = {"name": "电水壶", "status": "0"}
        # body3 = {"name": "电磁炉", "status": "0"}
        # body4 = {"name": "煮蛋器", "status": "0"}

        deviceObj = json.loads(body1)
        deviceName=deviceObj["name"]
        deviceStatus=deviceObj["status"]
        raspberryId=0

        try:
            deviceDb = DevicesDbTable.objects.get(deviceName=deviceName)
        except DevicesDbTable.DoesNotExist:
            deviceDb=DevicesDbTable(deviceName=deviceName,
                                    deviceStatus=deviceStatus,
                                    raspberryId=raspberryId)
            deviceDb.save()
            return HttpResponse(DevicesChange.devicesChangeJosnHelper(0,"insert to db success",deviceDb.id))

        return HttpResponse(DevicesChange.devicesChangeJosnHelper(0,"name has been exist",0))

    @staticmethod
    def deleteDevice(request):
        body1 = {"name": "电饭煲", "status": "0"}
        # body2 = {"name": "电水壶", "status": "0"}
        # body3 = {"name": "电磁炉", "status": "0"}
        # body4 = {"name": "煮蛋器", "status": "0"}

        deviceObj = json.loads(body1)
        deviceName = deviceObj["name"]
        deviceStatus = deviceObj["status"]
        raspberryId = 0

        try:
            deviceDb = DevicesDbTable.objects.get(deviceName=deviceName)
        except DevicesDbTable.DoesNotExist:
            return HttpResponse(DevicesChange.devicesChangeJosnHelper(0, "name is not exist", 0))

        deviceDb.delete()
        return HttpResponse(DevicesChange.devicesChangeJosnHelper(1, "delete db success", 0))
