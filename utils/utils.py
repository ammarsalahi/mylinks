from random import randint
import string
import random
from publiclink.models import *
from privatelink.models import *
from sharelink.models import *
def getcode():
    code ='{}-{}'.format(randint(1111,9999),randint(1111,9999))
    return code 

def getcodeurl():
    return "".join(random.choice(string.ascii_letters+string.digits) for _ in range(50))


def get_link(size: int) -> str:
    return "".join(random.choice(string.ascii_letters+string.digits) for _ in range(size))

def link_generator(_model):
    size=4
    link="s-{}".format(get_link(size))
    try:
        while _model.objects.get(shorturl=link) is not None :
            link=get_link(size+1)
    except _model.DoesNotExist:
        return link        
    return link      


def getIdType(link):
    ulink=None
    if link.linktype=='upublic':
        ulink=PublicLink.objects.get(link=link)
    elif link.linktype=='uprivate':
        ulink=PrivateLink.objects.get(link=link)
    elif link.linktype=='ushare':
        ulink=ShareLink.objects.get(link=link)    
    return ulink          

def getRandomUsername():
    return "".join(random.choice(string.ascii_letters) for _ in range(30))
        
