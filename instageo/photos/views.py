import os
import json
import httplib

from django.template import RequestContext

from django.views.generic.base import TemplateView

from instagram.client import InstagramAPI

CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
api = InstagramAPI(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)


class GeoPhotosView(TemplateView):

	template_name='index.html'

	def get_context_data(self, **kwargs):
		context = super(GeoPhotosView, self).get_context_data(**kwargs)
		context['photos'], context['city'] = self.get_photos_city()
		return context


	def get_client_ip(self):
		return '150.161.219.79' ###### Tirar isso aqui! So pra teste local!

		try:
			xff = self.request.META.get('HTTP_X_FORWARDED_FOR')
			if xff:
				return xff.split(',')[0]
			return self.request.META.get('REMOTE_ADDR')
		except:
			return '150.161.219.79'


	def get_client_info(self):
		"""
		Get client information according to his ip address.
		Returns:
		{"timezone":"--","isp":"--","region_code":"--","country":"--",
		"dma_code":"--","area_code":"--","region":"--","ip":"--","latitude":--,
		"country_code":"-","country_code3":"--"}
		"""

		client_ip = self.get_client_ip()
		conn = httplib.HTTPConnection("www.telize.com")
		conn.request("GET", "/geoip/" + client_ip)
		r = conn.getresponse()
		data = json.loads(r.read())
		return data

	def get_photos_city(self):
		"""
		First, it tries to get the client city name to get photos by the tag "#city_name".
		If the client information doesnt have his city name, then we try to get the photos 
		by his latitude and longitude.
		"""

		data = self.get_client_info()
		city = None

		try:
			city = data['city']
			photos, next_ = api.tag_recent_media(count=20, tag_name=city)
		except:
			print 'Client info does not have city name.'
			try:
				lat = data['latitude']
				lng = data['longitude']
				photos = api.media_search(count=20, lat=lat, lng=lng)
			except:
				print 'Client ip does not have information enough.'

		return photos, city