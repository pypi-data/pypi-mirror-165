from django.shortcuts import render

from gears import SerializersMixin


class MyModelViewSet(
    SerializersMixin,
):
    serializers = {
        'default': MyModelSerializer
    }
