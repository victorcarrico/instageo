import os
import json
import httplib

from django.shortcuts import render_to_response
from django.template import RequestContext

from instagram.client import InstagramAPI


CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
api = InstagramAPI(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

	
def get_client_ip(request):
	xff = request.META.get('HTTP_X_FORWARDED_FOR')
	if xff:
		return x_forwarded_for.split(',')[0]
	return request.META.get('REMOTE_ADDR')

def get_client_position(request):
	"""
	Get client position according to his ip.
	Returns:
	{"timezone":"--","isp":"--","region_code":"--","country":"--",
	"dma_code":"--","area_code":"--","region":"--","ip":"--","latitude":--,
	"country_code":"-","country_code3":"--"}
	"""

	conn = httplib.HTTPConnection("www.telize.com")
	conn.request("GET", "/geoip/150.161.219.79") #Ajeitar issaque
	r = conn.getresponse()
	data = json.loads(r.read())
	return data

def get_photos_city(request):
	city = get_client_position(request)['city']
	medias, next_ = api.tag_recent_media(count=20, tag_name=city)
	return medias, next_

def get_photos_pos(request):
	data = get_client_position(request)
	places = api.location_search(lat=int(data['latitude']),lng=int(data['longitude']),count=10)
	#incompleta

def index(request):
	c = RequestContext(request)
	c['photos'], next_ = get_photos_city(request)
	return render_to_response('index.html', c)