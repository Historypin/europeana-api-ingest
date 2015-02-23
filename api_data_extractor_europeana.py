from application.models.api_data_extractor import *
import logging, re, urllib2

from datetime import datetime, date

# TODO - Check Licenses before updating


class API_DataExctractor_Europeana(API_DataExctractor_Interface):
	data_date_taken = ''
	
	def _proxy(self, field):
		return self.data['object']['proxies'][0].get(field, {'def': ['']})['def'][0]
	
	def get_type(self): return 2 if self.data['object']['type'] == 'SOUND' else 1
	def get_content_type(self)		: return self.data['object']['proxies'][0]['edmType']
	def get_content_theme(self)		: return self.data['object']['proxies'][0]['edmType']
	def get_caption(self)			: return self.data['object']['title'][0]
	def get_description(self)		: return self._proxy('dcDescription')
	def get_tags(self)				: return ','.join(self.data['object']['proxies'][0].get('dcSubject', {'def': ['']})['def'])
	def get_youtube_url(self)		: return urllib2.unquote(urllib2.unquote(self.data['object']['aggregations'][0]['edmIsShownAt'].split('shownAt=')[1].split('&')[0]))
	
	def get_date_created(self)		: return datetime.strptime(self.data['object']['timestamp_created'].split('.')[0], '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
	def get_date_taken(self)		: return self._proxy('dcDate') or self.data['object']['timespans'][1]['begin']['def'][0] or self.data['object']['timespans'][1]['end']['def'][0] or self.data_date_taken
	def get_date_interval(self)		: return 0
	def get_date_filters(self)		: '' #return self._proxy('dcPublisher')
	
	def get_license_type(self)		: return self.data['object']['europeanaAggregation']['edmRights']['def'][0].encode('utf-8')
	def get_author(self)			: return self._proxy('dcCreator')
	def get_link(self)				:
		l = urllib2.unquote(urllib2.unquote(self.data['object']['aggregations'][0]['edmIsShownAt'].split('shownAt=')[1].split('&')[0]))
		if l == '' or l == None:
			l = urllib2.unquote(urllib2.unquote(self.data['object']['aggregations'][0]['edmIsShownBy']))
		return l
	
	def get_lat(self)				:
		try:
			return self.data['object'].get('places', [{'latitude': '0'}])[0]['latitude']
		except Exception, e:
			logging.critical('No latitude found!')
			return 0
	
	def get_lng(self)				:
		try:
			return self.data['object'].get('places', [{'longitude': '0'}])[0]['longitude']
		except Exception, e:
			logging.critical('No longitude found!')
			return 0
	
	def get_lang(self)				: return self.data['object']['language'][0]
	
	# def get_remote_id(self)		: return self.data['object']['europeanaAggregation']['about'] 
	def get_remote_id(self)			: return self.data['object']['about']
	def get_media_provider(self)	: return self.data['object']['aggregations'][0]['edmDataProvider']['def'][0]
	def get_archive(self)			: return self.data['object']['aggregations'][0]['edmDataProvider']['def'][0]
	def get_author_url(self)		: ''
	def get_publisher_url(self)		: return self._proxy('dcPublisher')
	def get_original_format(self)	: return self._proxy('dcFormat')
	def get_duration(self)			: return self._proxy('dctermsExtent')
	def get_genre(self)				: return ','.join(self.data['object']['proxies'][0]['dcType']['def'])
	def get_kind(self)				: return ','.join( self.data['object']['proxies'][0]['dcType']['def'])
	def get_medial_language(self)	: return self.data['object']['language'][0]
	def get_aggregator(self)		:
		d = self.data['object']['aggregations'][0]['edmProvider']
		if 'def' in d:
			return d['def'][0]
		elif 'en' in d:
			return d['en'][0]
	def get_urn_value(self)			: return urllib2.unquote(urllib2.unquote(self.data['object']['aggregations'][0]['edmIsShownBy']))
		
	def get_direct_link(self)		: return ''
	
	def get_date_from(self)			: return date(int(self.get_date_taken().split('-')[0]), 1, 1)
	def get_date_to(self)			: return date(int(self.get_date_taken().split('-')[0]), 12, 31)
	
