# -*- coding: utf-8 -*-

import requests
import json
import re
import traceback

from requests_oauthlib import OAuth1Session
from pickle import NONE
try:
	from urllib.parse import quote_plus
except:
	from urllib import quote_plus

from base64 import b64decode as bd

from .CSFDLog import LogCSFD
from .CSFDSettings2 import config

# ######################################################################################

class CSFDAndroidClient:
	def __init__( self, login_token=None ):
		data = "MDYxMDI1MjQxMDQ5ODhhZjk1MjZlZTk2NzE3OWh0dHBzOi8vYW5kcm9pZC1hcGkuY3NmZC5jei9Vc2VyLUFnZW50Q1NGRHJvaWQvMi4zLjMuMTU0NCAoU2Ftc3VuZyBHYWxheHkgUzc7IDYuMCBSRUwpWC1BcHAtVmVyc2lvbjE1NDQg"
		data = bd( data.encode( 'utf-8' ) ).decode('utf-8')

		self.oauth_token=None
		self.oauth_token_secret=None

		if login_token != None:
			s = login_token.split(':')
			
			if len(s) == 2:
				self.oauth_token = s[0]
				self.oauth_token_secret = s[1]

		self.client_key=data[:12]
		self.client_secret=data[12:28]
		self.api_url=data[28:55]
		self.headers = { data[56:66]: data[66:114], data[114:127]: data[127:131] }

		self.init_oauth_session()
		
	# ######################################################################################
	
	def is_logged(self):
		return self.oauth.authorized
	
	# ######################################################################################
	
	def get_login_token(self):
		if self.oauth_token != None and self.oauth_token_secret != None:
			return self.oauth_token + ':' + self.oauth_token_secret
		else:
			return ''
		
	# ######################################################################################
	
	def init_oauth_session(self):
		self.oauth = OAuth1Session( self.client_key, client_secret=self.client_secret, resource_owner_key=self.oauth_token, resource_owner_secret=self.oauth_token_secret )
	
	# ######################################################################################
	
	def __login( self, username, password ):
		# Init oauth with oauth callback
		callback_uri='csfdroid://oauth-callback'
		self.oauth = OAuth1Session( self.client_key, client_secret=self.client_secret, callback_uri=callback_uri )

		# Step 1 - fetch request token
		self.oauth.fetch_request_token( self.api_url + '/oauth/request-token', headers={ 'User-Agent': 'Apache-HttpClient/UNAVAILABLE (java 1.4)' } )

		# Step 2 - create authorization url, and do login
		headers = {
			"User-Agent": 'Mozilla/5.0 (Linux; Android 6.0; Samsung Galaxy S7 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.186 Mobile Safari/537.36',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
			'X-Requested-With': 'cz.csfd.csfdroid'
		}

		auth_url = self.oauth.authorization_url( self.api_url + '/oauth/authorize', None, oauth_callback=callback_uri, fb_callback='https://www.csfd.cz/csfdroid/fb/init' )

		# Step 3 - download login page
		login_page = requests.get(auth_url, headers=headers)
		
		if login_page.status_code != 200:
			raise ValueError("Wrong status code for login page: %d" % login_page.status_code)
		
		# Step 4 - extract login url + login form data
		login_url, form_data = self.process_login_page( login_page.text, username, password )

		headers['Origin'] = self.api_url
		headers['Referer'] = auth_url
		
		# Step 5 - submit login form, handle redirects and extract login response
		with requests.Session() as ls:
			r = ls.post(login_url, headers=headers, data=form_data, allow_redirects=False, timeout=config.misc.CSFD.DownloadTimeOut.getValue())
			
			while True:
				if r.status_code == 200:
					login_response = r.text
					break
				elif r.status_code >= 400 and r.status_code < 500:
					raise ValueError("Unauthorized: %d" % r.status_code)
				elif r.status_code >= 300 and r.status_code < 400:
					login_url = r.headers['Location']
					
					if r.headers['Location'].startswith( callback_uri ):
						login_response = login_url
						break
					
					r = ls.get(login_url, headers=headers, allow_redirects=False, timeout=config.misc.CSFD.DownloadTimeOut.getValue())
				else:
					raise ValueError("Wrong status code for login request received: %d" % r.status_code)
		
		# Step 6 - extract data from login response
		self.oauth.parse_authorization_response(login_response)
		
		# Step7 - fetch access token
		ret = self.oauth.fetch_access_token( self.api_url + '/oauth/access-token', headers={ 'User-Agent': 'Apache-HttpClient/UNAVAILABLE (java 1.4)' } )
		self.oauth_token = ret.get('oauth_token')
		self.oauth_token_secret = ret.get('oauth_token_secret')
	
	# ######################################################################################
	
	def login( self, username, password ):
		try:
			self.__login( username, password)
		except:
			self.init_oauth_session()
			print( traceback.format_exc() )
			return False
		
		return True

	# ######################################################################################

	def logout( self ):
		if self.is_logged():
			self.do_request( '/oauth/logout' )
			self.oauth_token=None
			self.oauth_token_secret=None
			self.init_oauth_session()

	# ######################################################################################
	
	def process_login_page( self, login_page, username, password ):
		form_data = {}
		have_username = False
		have_password = False
		form_data["username"] = username
		form_data["password"] = password
		
		login_form_str = re.search('<form .*</form>', login_page, re.DOTALL | re.IGNORECASE ).group(0)
		login_url = re.search('action="(.*?)"', login_form_str, re.IGNORECASE ).group(1)
		login_method = re.search('method="(.*?)"', login_form_str, re.IGNORECASE ).group(1)
		
		if login_method != "post":
			raise ValueError("login method %s is not supported" % login_method )
		
		input_name_mask = re.compile( 'name="(.*?)"', re.IGNORECASE )
		input_value_mask = re.compile( 'value="(.*?)"', re.IGNORECASE )

		for input_str in re.findall('<input .*?>', login_form_str, re.DOTALL | re.IGNORECASE ):
			
			input_name = input_name_mask.search(input_str).group(1)
			input_value_match = input_value_mask.search(input_str)
			
			if input_value_match == None:
				input_value = None
			else:
				input_value = input_value_match.group(1)
			
			if input_name == "username":
				have_username = True
			elif input_name == "password":
				have_password = True
			elif input_value == None:
				raise ValueError("input name \"%s\" without value" % input_name )
			else:
				form_data[input_name] = input_value
	
		if not have_username or not have_password:
			raise ValueError("No username or password form field detected")
		
		return login_url, form_data

	# ######################################################################################
	
	def do_request( self, params ):
		try:
			response = self.oauth.get( self.api_url + '/' + params, headers=self.headers, timeout=config.misc.CSFD.DownloadTimeOut.getValue() )
		except:
			return {
				"http_error": 666,
				"http_error_text": "exception"
				}
		
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
	
	def get_user_identity(self):
		if self.is_logged():
			return self.do_request('identity')['identity']
		else:
			return {}
	
	# ######################################################################################

	def get_user_info(self, user_id=None):
		if user_id == None:
			x = self.get_user_identity()
			if "id" in x:
				user_id = x['id']
			else:
				return {}
			
		if self.is_logged():
			return self.do_request( 'user/%d' % user_id )
		else:
			return {}
	
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
			
			ret = { "info": data1, "creators" : data2 }
			
			if "root_id" in data1:
				ret["root_info"] = self.get_movie_info( data1["root_id"] )["info"]
				
			return ret 

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
		elif uri.startswith('#movie_premiere#'):
			LogCSFD.WriteToFile( "Requesting movie premiere for \"%s\"\n" % uri[16:], 2 )

			return {}
		elif uri.startswith('#creator#'):
			return self.get_creator_info( uri[9:])
		
		return { "internal_error": "unknown uri %s" % uri }
	
	# ######################################################################################
	