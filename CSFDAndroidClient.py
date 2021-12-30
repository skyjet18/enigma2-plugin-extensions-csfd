# -*- coding: utf-8 -*-

import requests
import json
from requests_oauthlib import OAuth1Session
try:
	from urllib.parse import quote_plus
except:
	from urllib import quote_plus


from CSFDLog import LogCSFD

# ######################################################################################

class CSFDAndroidClient:
	def __init__( self ):
		self.client_key="061025241049"
		self.client_secret="88af9526ee967179"
		self.api_url="https://android-api.csfd.cz/"
		self.headers = {
			'User-Agent': 'CSFDroid/2.3.3.1544 (Samsung Galaxy S7; 6.0 REL)',
			'X-App-Version': '1544'
		}
		
		self.oauth = OAuth1Session( self.client_key, client_secret=self.client_secret )

	# ######################################################################################	
	
	def do_request( self, params ):
		response = self.oauth.get( self.api_url + params, headers=self.headers )
		
		if response.status_code == 200:
			LogCSFD.WriteToFile( "Status: %d, Response: %s\n" % (response.status_code, response.text), 2 )
#			print( response.text )
			return json.loads(response.text)
		
		LogCSFD.WriteToFile( "Status: %d, Response: %s\n" % (response.status_code, response.text), 2 )
		return {
			"http_error": response.status_code,
			"http_error_text": response.text
			}
	
	# ######################################################################################
	
	def search_by_name( self, name, offset=0, limit=10 ):
#		name = quote_plus( name )

		return self.do_request( 'search?q=%s&offset=%d&limit=%d' % ( name, offset, limit ) )
	
	# ######################################################################################
	
	# Vrati mapovanie kategorii videi na nazvy
	def get_video_types( self ):
		return self.do_request( 'video/types' )
	
	# ######################################################################################
	
	def get_movie_info( self, movie_id ):
		return self.do_request( 'film/%d' % int(movie_id) )

	# ######################################################################################

	def movie_info_additional( self, movie_id, command, offset=0, limit=0 ):
		if offset != 0 or limit != 0:
			command = command + '?offset=%d&limit=%d' % (offset, limit)
			
		return self.do_request( 'film/%d/%s' % (int(movie_id), command ) )

	# ######################################################################################
	
	def get_movie_creators( self, movie_id, offset=0, limit=10 ):
		return self.movie_info_additional( movie_id, "creators", offset, limit )

	# ######################################################################################

	# zaujimavosti z filmu
	def get_movie_trivia( self, movie_id, offset=0, limit=10 ):
		return self.movie_info_additional( movie_id, "trivia", offset, limit )

	# ######################################################################################
	
	def get_movie_photos( self, movie_id, offset=0, limit=10 ):
		return self.movie_info_additional( movie_id, "photos", offset, limit )
	
	# ######################################################################################
	
	def get_movie_videos( self, movie_id, offset=0, limit=10 ):
		return self.movie_info_additional( movie_id, "videos", offset, limit )

	# ######################################################################################
	
	def get_movie_comments( self, movie_id, offset=0, limit=10 ):
		return self.movie_info_additional( movie_id, "comments", offset, limit )
	
	# ######################################################################################

	def get_movie_episodes( self, movie_id, offset=0, limit=10 ):
		return self.movie_info_additional( movie_id, "episodes", offset, limit )
	
	# ######################################################################################
	
	def get_movie_related( self, movie_id, offset=0, limit=10 ):
		return self.movie_info_additional( movie_id, "related", offset, limit )
	
	# ######################################################################################

	def get_movie_similar( self, movie_id, offset=0, limit=10 ):
		return self.movie_info_additional( movie_id, "similar", offset, limit )
	
	# ######################################################################################

	def get_creator_info( self, creator_id ):
		return self.do_request( 'creator/%d' % int(creator_id) )

	# ######################################################################################

	def creator_info_additional( self, creator_id, command, offset=0, limit=0 ):
		if offset != 0 or limit != 0:
			command = command + '?offset=%d&limit=%d' % (offset, limit)
			
		return self.do_request( 'creator/%d/%s' % (int(creator_id), command ) ) # + ?return=array

	# ######################################################################################
	
	def get_creator_movies( self, creator_id, offset=0, limit=10 ):
		return self.creator_info_additional( creator_id, "films", offset, limit )
	
	# ######################################################################################
	
	def get_json_by_uri(self, uri, page=1 ):
		
		if uri.startswith('#search_movie#'):
			LogCSFD.WriteToFile( "Searching movie: \"%s\"\n" % uri[14:], 2 )

			return self.search_by_name( uri[14:], (page - 1) * 30, 30 )
			
		elif uri.startswith('#movie#'):
			LogCSFD.WriteToFile( "Requesting movie info for \"%s\"\n" % uri[7:], 2 )

			data1 = self.get_movie_info( uri[7:])["info"]
			data2 = self.get_movie_creators( uri[7:], 0, 30 )["creators"]
			
			return { "info": data1, "creators" : data2 }

		elif uri.startswith('#movie_photos#'):
			LogCSFD.WriteToFile( "Requesting movie photos for \"%s\"\n" % uri[14:], 2 )

			return self.get_movie_photos( uri[14:], (page - 1) * 20, 20 )
		elif uri.startswith('#movie_videos#'):
			LogCSFD.WriteToFile( "Requesting movie videos for \"%s\"\n" % uri[14:], 2 )

			return self.get_movie_videos( uri[14:], (page - 1) * 20, 20 )
		elif uri.startswith('#movie_comments#'):
			LogCSFD.WriteToFile( "Requesting movie comments for \"%s\"\n" % uri[16:], 2 )

			return self.get_movie_comments( uri[16:], (page - 1) * 10, 10 )
		elif uri.startswith('#movie_trivia#'):
			LogCSFD.WriteToFile( "Requesting movie trivia for \"%s\"\n" % uri[14:], 2 )

			return self.get_movie_trivia( uri[14:], (page - 1) * 10, 10 )
		elif uri.startswith('#creator#'):
			return self.get_creator_info( uri[9:])
		
		return { "internal_error": "unknown uri %s" % uri }
	
	# ######################################################################################
	