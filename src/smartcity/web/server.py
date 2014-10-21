from django.template import Library, Node

from django.db.models import get_model

import os.path


TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), 'templates'),)


register = Library()



class LatestContentNode(Node):

    def __init__(self, model, num, varname):

        self.num, self.varname = num, varname

        self.model = get_model(*model.split('.'))



    def render(self, context):

        context[self.varname] = self.model._default_manager.all()[:self.num]

        return ''



def get_latest(parser, token):

    bits = token.contents.split()

    if len(bits) != 5:

        raise Exception("get_latest tag takes exactly four arguments")

    if bits[3] != 'as':

        raise Exception("third argument to get_latest tag must be 'as'")

    return LatestContentNode(bits[1], bits[2], bits[4])



get_latest = register.tag(get_latest)




