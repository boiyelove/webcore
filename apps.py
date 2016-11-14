from django.apps import AppConfig


class WebcoreConfig(AppConfig):
    name = 'webcore'

    def ready(self):
    	import webcore.signals