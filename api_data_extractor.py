import json
import urllib2

class API_DataExctractor_Interface:
	def __init__(self, url):
		self.url = url
		self.fetch(url)
	
	def fetch(self, url):
		raw_data = urllib2.urlopen(self.url, timeout = 60).read()
		self.decode(raw_data)
	
	def decode(self, raw_data):
		self.data = json.loads(raw_data)
	
	def get_data_full(self):
		return self.get_data_item(), self.get_data_item_location(), self.get_data_additional()
	
	def get_data_item(self):
		fields = [
			'type', 'content_type', 'content_theme',
			'caption', 'description', 'tags', 'youtube_url',
			'location_known',
			'date_created', 'date_known', 'date_taken', 'date_interval', 'not_sure', 'not_sure_month', 'not_sure_day', 'use_date',
			'license', 'license_type', 'author', 'link', 'archive',
			'complete', 'lang',
		]
		
		return { f: getattr(self, 'get_' + f)() for f in fields }
	def get_data_item_location(self):
		fields = [
			'lat', 'lng', 'date_from', 'date_to'
		]
		
		return { f: getattr(self, 'get_' + f)() for f in fields }
	
	def get_data_additional(self):
		fields = [
			'remote_id',
			'media_provider', 'author', 'author_url', 'publisher_url', 'original_format', 
			'duration', 'genre', 'kind', 'medial_language', 'aggregator', 'direct_link', 'urn_value',
		]
		
		
		return { f: getattr(self, 'get_' + f)() for f in fields }


	#def get_id(self):	raise NotImplementedError()
	def get_type(self)				: raise NotImplementedError()
	def get_content_type(self)		: raise NotImplementedError()
	def get_content_theme(self)		: raise NotImplementedError()
	def get_caption(self)			: raise NotImplementedError()
	def get_description(self)		: raise NotImplementedError()
	def get_tags(self)				: raise NotImplementedError()
	def get_youtube_url(self)		: raise NotImplementedError()
	def get_location_known(self)	: return 1 if self.get_lat() and self.get_lng() else 0
	
	def get_date_created(self)		: raise NotImplementedError()
	def get_date_known(self)		: return 1 if self.get_date_taken() else 0
	def get_date_taken(self)		: raise NotImplementedError()
	def get_date_interval(self)		: raise NotImplementedError()
	def get_not_sure(self)			: return 0
	def get_not_sure_month(self)	: return 0
	def get_not_sure_day(self)		: return 0
	def get_use_date(self)			: return 1 if self.get_date_taken() else 0
	
	def get_license(self)			: return 1 if self.get_license_type() else 0
	def get_license_type(self)		: raise NotImplementedError()
	def get_author(self)			: raise NotImplementedError()
	def get_link(self)				: raise NotImplementedError()
	def get_archive(self)			: raise NotImplementedError()  # Repository
	
	def get_complete(self)			: return 1 if self.get_location_known() and self.get_date_taken() and self.get_caption() else 0
	def get_lang(self)				: raise NotImplementedError()
	
	def get_lat(self)				: raise NotImplementedError()
	def get_lng(self)				: raise NotImplementedError()
	
	def get_remote_id(self)			: raise NotImplementedError()
	def get_media_provider(self)	: raise NotImplementedError()
	def get_author_url(self)		: raise NotImplementedError()
	def get_publisher_url(self)		: raise NotImplementedError()
	def get_original_format(self)	: raise NotImplementedError()
	def get_duration(self)			: raise NotImplementedError()
	def get_genre(self)				: raise NotImplementedError()
	def get_kind(self)				: raise NotImplementedError()
	def get_medial_language(self)	: raise NotImplementedError()
	def get_aggregator(self)		: raise NotImplementedError()
	def get_urn_value(self)			: raise NotImplementedError()
	def get_direct_link(self)		: raise NotImplementedError()
	
	def get_date_filters(self)		: raise NotImplementedError()
	def get_publisher_name(self)	: raise NotImplementedError()
	
	def get_date_from(self)			: raise NotImplementedError()
	def get_date_to(self)			: raise NotImplementedError()



