import pprint

__author__ = 'busta'


def pre_get_register(request, lookup):
    pprint.pprint("hi")


def pre_post_register(request):
#    del request.json['devicef']
    pprint.pprint("hiya")