#! -*- coding=utf-8 -*-
import logging
logging.basicConfig()

import datetime
import time
import os
import threading
import platform
import json

from apscheduler.schedulers.background import BackgroundScheduler
from django.http import Http404,HttpResponse

from SmartServer.raspberry.RaspberryControl import RaspberryControl
from SmartServer.models import DevicesDbTable

class ClockOneTime(object):

    instance = None
    mutex = threading.Lock()
    scheduler = None
    isRunning = False

    @staticmethod
    def clockOneTimeJsonHelper(value,info):
        item = {}
        item.setdefault("value",value)
        item.setdefault("info",info)
        return json.dumps(item)

    def __init__(self):
        pass

    @staticmethod
    def run(num):
        mid = int(num)
        print "id %d" %mid
        try:
            devicesDb = DevicesDbTable.objects.get(id=mid)
        except DevicesDbTable.DoesNotExist:
            # return HttpResponse(DeviceControl.deviceControlJsonHelper(0,"数据库中不存在该设备信息"))
            print ""+ClockOneTime.clockOneTimeJsonHelper(0,"数据库中不存在该设备信息")

        status = devicesDb.deviceStatus
        if status == 1:
            print '%s 设备已经启动' %deviceName
            # return HttpResponse(DeviceControl.deviceControlJsonHelper(0, "该设备已经启用"))
            print ""+ClockOneTime.clockOneTimeJsonHelper(0, "该设备已经启用")

        pin = devicesDb.raspberryId
        retValue = RaspberryControl.GetInstance().raspberryOn(pin)

        if retValue == True:
            devicesDb.deviceStatus = 1
            devicesDb.save()
            print '设备启动成功 '
            # return HttpResponse(DeviceControl.deviceControlJsonHelper(1,"设备启动成功"))
            print ClockOneTime.clockOneTimeJsonHelper(1,"设备启动成功")
        else:
            print " 设备启动失败"
            # return HttpResponse(DeviceControl.deviceControlJsonHelper(0, "设备启动失败"))
            print ClockOneTime.clockOneTimeJsonHelper(0, "设备启动失败")

    @staticmethod
    def GetInstance():
        if (ClockOneTime.instance == None):
            ClockOneTime.mutex.acquire()
            if (ClockOneTime.instance == None):
                ClockOneTime.instance = ClockOneTime()
                ClockOneTime.scheduler = BackgroundScheduler()
            ClockOneTime.mutex.release()

        return ClockOneTime.instance

    @staticmethod
    def oneDevicesOrder(request):
        ClockOneTime.GetInstance()

        if request.method == 'GET':
            deviceNum = request.GET['num']
            deviceName=request.GET['name']
            deviceTime=request.GET['time']

        print "deviceName " + deviceName + "deviceNum " + deviceNum + "deviceTime " + deviceTime

        times = deviceTime.split(':')
        devHour = int(times[0])
        devMinute = int(times[1])

        now = datetime.datetime.now()
        print now

        if(devHour>now.hour or (devHour==now.hour and devMinute>now.minute)):
            date = now
        else:
            date = now + datetime.timedelta(days=1)

        # date = now + datetime.timedelta(minutes=1)

        ClockOneTime.scheduler.add_job(ClockOneTime.run,
                                       'date',
                                       run_date=datetime.datetime(date.year,
                                                                  date.month,
                                                                  date.day,
                                                                  devHour,
                                                                  devMinute,
                                                                  0),
                                       id=deviceName,
                                       args=[deviceNum])
        try:
            if ClockOneTime.isRunning == False:
                ClockOneTime.scheduler.start()
                ClockOneTime.isRunning = True
        except (KeyboardInterrupt, SystemExit):
            ClockOneTime.scheduler.shutdown()
        ClockOneTime.scheduler.print_jobs()

        return HttpResponse(ClockOneTime.clockOneTimeJsonHelper(1,"success"))

    # @staticmethod
    # def clockDate(request):
    #     ClockOneTime.GetInstance()
    #     print datetime.now()
    #     mid = 'my_job_id %s' % datetime.now()
    #     ClockOneTime.scheduler.add_job(ClockOneTime.run,
    #                                    'date',
    #                                    run_date=datetime(2016, 12, 5, 2, 30, 30),
    #                                    id= mid)
    #     try:
    #         if ClockOneTime.isRunning == False:
    #            ClockOneTime.scheduler.start()
    #            ClockOneTime.isRunning = True
    #     except (KeyboardInterrupt, SystemExit):
    #         ClockOneTime.scheduler.shutdown()
    #     ClockOneTime.scheduler.print_jobs()
    #     return HttpResponse("HAHA")
    #
    # @staticmethod
    # def emurClockList(request):
    #     ClockOneTime.GetInstance()
    #
    #     mid = 'my_job_id %s' % datetime.now()
    #     ClockOneTime.scheduler.add_job(ClockOneTime.run,
    #                                    'date',
    #                                    run_date=datetime(2016, 12, 5, 2, 20, 30),
    #                                    id= mid)
    #
    #     ClockOneTime.scheduler.print_jobs()
    #     return HttpResponse("HAHA2")