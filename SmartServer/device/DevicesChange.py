#!-*- coding=utf-8 -*-

import json

from django.http import Http404,HttpResponse

from SmartServer.models import DevicesDbTable


class DevicesChange(object):

    @staticmethod
    def devicesChangeJsonHelper(value, info):
        item = {}
        item.setdefault("value",value)
        item.setdefault("info",info)
        # item.setdefault("other",other)
        return json.dumps(item)

    @staticmethod
    def addDevice(request):

        if request.method == 'GET':
            # deviceName=request.GET['name']
            deviceStatus=request.GET['status']
            raspberryId=0

            try:
                deviceDb = DevicesDbTable.objects.get(deviceName=deviceName)
            except DevicesDbTable.DoesNotExist:
                deviceDb=DevicesDbTable(deviceName=deviceName,
                                        deviceStatus=deviceStatus,
                                        raspberryId=raspberryId)
                deviceDb.save()
                return HttpResponse(DevicesChange.devicesChangeJsonHelper(1, "插入设备信息到数据库中"))

            return HttpResponse(DevicesChange.devicesChangeJsonHelper(0, "数据库中存在该设备名"))

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
            return HttpResponse(DevicesChange.devicesChangeJsonHelper(0, "要删除的设备信息不存在"))

        deviceDb.delete()
        return HttpResponse(DevicesChange.devicesChangeJsonHelper(1, "从数据库中删除设备信息"))
