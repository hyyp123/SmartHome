"""SmartHome URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from SmartServer.device.DevicesChange import DevicesChange
from SmartServer.device.DeviceControl import DeviceControl
from SmartServer.clock.ClockOneTime import ClockOneTime
from SmartServer.views.Welcome import Welcome

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^device/addDevice', DevicesChange.addDevice),
    url(r'^device/deleteDevice', DevicesChange.deleteDevice),

    url(r'^device/oneDeviceOn',DeviceControl.oneDeviceOn),
    url(r'^device/oneDeviceOff',DeviceControl.oneDeviceOff),
    url(r'^device/allDeviceOn',DeviceControl.allDeviceOn),
    url(r'^device/allDeviceOff',DeviceControl.allDeviceOff),
    url(r'^order/oneDevice',ClockOneTime.oneDevicesOrder),
    url(r'.*',Welcome.Welcome),
]
