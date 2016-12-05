#-*- coding = utf-8 -*-
from django.http import Http404,HttpResponse


class Welcome(object):

    @staticmethod
    def Welcome(request):
        return HttpResponse("success")
