# -*- coding: utf-8 -*-

import requests
import json
import re
import traceback
import time

from .oauth.requests_oauthlib import OAuth1Session
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

http_adaptor = HTTPAdapter(max_retries=Retry(total=3, backoff_factor=0.1))

try:
	from urllib.parse import quote_plus
except:
	from urllib import quote_plus

from base64 import b64decode as bd

from .CSFDLog import LogCSFD
from .CSFDSettings2 import config
from .CSFDTools import internet_on

try:
	from functools import lru_cache
except:
	from .lru import lru_cache
	
# ######################################################################################

class CSFDAndroidClient:
	def __init__( self, login_token=None ):
		data = "MDYxMDI1MjQxMDQ5ODhhZjk1MjZlZTk2NzE3OWh0dHBzOi8vYW5kcm9pZC1hcGkuY3NmZC5jei9Vc2VyLUFnZW50Q1NGRHJvaWQvMi4zLjMuMTU0NCAoU2Ftc3VuZyBHYWxheHkgUzc7IDYuMCBSRUwpWC1BcHAtVmVyc2lvbjE1NDQg"
		data = bd( data.encode( 'utf-8' ) ).decode('utf-8')

		self.oauth_token=None
		self.oauth_token_secret=None
		self.logged_user=None
		self.logged_user_id=None
		
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
		self.oauth.mount('http://', http_adaptor)
		self.oauth.mount('https://', http_adaptor)

	# ######################################################################################
	
	def __login( self, username, password ):
		if username == None or username == '':
			raise ValueError("Username is empty")

		if password == None or password == '':
			raise ValueError("Password is empty")

		data = 'Y3NmZHJvaWQ6Ly9vYXV0aC1jYWxsYmFja1VzZXItQWdlbnRBcGFjaGUtSHR0cENsaWVudC9VTkFWQUlMQUJMRSAoamF2YSAxLjQpTW96aWxsYS81LjAgKExpbnV4OyBBbmRyb2lkIDYuMDsgU2Ftc3VuZyBHYWxheHkgUzcgQnVpbGQvTVJBNThLOyB3dikgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgVmVyc2lvbi80LjAgQ2hyb21lLzc0LjAuMzcyOS4xODYgTW9iaWxlIFNhZmFyaS81MzcuMzZBY2NlcHR0ZXh0L2h0bWwsYXBwbGljYXRpb24veGh0bWwreG1sLGFwcGxpY2F0aW9uL3htbDtxPTAuOSxpbWFnZS93ZWJwLGltYWdlL2FwbmcsKi8qO3E9MC44LGFwcGxpY2F0aW9uL3NpZ25lZC1leGNoYW5nZTt2PWIzWC1SZXF1ZXN0ZWQtV2l0aGN6LmNzZmQuY3NmZHJvaWQvb2F1dGgvcmVxdWVzdC10b2tlbi9vYXV0aC9hdXRob3JpemUvb2F1dGgvYWNjZXNzLXRva2VuaHR0cHM6Ly93d3cuY3NmZC5jei9jc2Zkcm9pZC9mYi9pbml0'
		data = bd( data.encode( 'utf-8' ) ).decode('utf-8')
		
		# Init oauth with oauth callback
		self.oauth = OAuth1Session( self.client_key, client_secret=self.client_secret, callback_uri=data[0:25] )

		# Step 1 - fetch request token
		self.oauth.fetch_request_token( self.api_url + data[392:412], headers={ data[25:35]: data[35:75] } )

		# Step 2 - create authorization url, and do login
		auth_url = self.oauth.authorization_url( self.api_url + data[412:428], None, oauth_callback=data[0:25], fb_callback=data[447:483] )

		# Step 3 - download login page
		headers = { data[25:35]: data[75:236], data[236:242]: data[242:360], data[360:376]: data[376:392] }
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
					
					if r.headers['Location'].startswith( data[0:25] ):
						login_response = login_url
						break
					
					r = ls.get(login_url, headers=headers, allow_redirects=False, timeout=config.misc.CSFD.DownloadTimeOut.getValue())
				else:
					raise ValueError("Wrong status code for login request received: %d" % r.status_code)
		
		# Step 6 - extract data from login response
		self.oauth.parse_authorization_response(login_response)
		
		# Step7 - fetch access token
		ret = self.oauth.fetch_access_token( self.api_url + data[428:447], headers={ data[25:35]: data[35:75] } )
		self.oauth_token = ret.get('oauth_token')
		self.oauth_token_secret = ret.get('oauth_token_secret')
	
	# ######################################################################################
	
	def login( self, username, password ):
		try:
			self.__login( username, password)
		except:
			self.init_oauth_session()
			LogCSFD.WriteToFile( "Login to CSFD failed:", 2 )
			LogCSFD.WriteToFile( traceback.format_exc() )
			return False
		
		return True

	# ######################################################################################

	def logout( self ):
		if self.is_logged():
			self.do_request( '/oauth/logout' )
			self.oauth_token=None
			self.oauth_token_secret=None
			self.logged_user = None
			self.logged_user_id = None
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
	@lru_cache(maxsize=64)
	def do_request( self, params, data=None ):
		try:
			if data == None:
				response = self.oauth.get( self.api_url + '/' + params, headers=self.headers, timeout=config.misc.CSFD.DownloadTimeOut.getValue() )
			else:
				response = self.oauth.post( self.api_url + '/' + params, headers=self.headers, data=data, timeout=config.misc.CSFD.DownloadTimeOut.getValue() )
		except:
			LogCSFD.WriteToFile( "Exception in requests\n", 2 )
			return {
				"http_error": 666,
				"http_error_text": "exception"
				}
		
		if response.status_code == 200:
			return json.loads(response.text)
		
		LogCSFD.WriteToFile( "Status: %d, Response: %s\n" % (response.status_code, response.text), 2 )
		return {
			"http_error": response.status_code,
			"http_error_text": response.text
			}
	
	# ######################################################################################
	
	def get_user_identity(self):
		if self.is_logged():
			ret = self.do_request('identity')['identity']
			
			if self.logged_user == None:
				self.logged_user = ret["nick"]
				self.logged_user_id = int(ret["id"])
			return ret
		else:
			return None
	
	# ######################################################################################

	def get_user_info(self, user_id=None):
		if user_id == None:
			if self.logged_user_id == None:
				self.get_user_identity()
				user_id = self.logged_user_id
			
		if self.is_logged() and user_id != None:
			return self.do_request( 'user/%d' % user_id )
		else:
			return {}
	
	# ######################################################################################
	
	def get_logged_user(self):
		if self.logged_user == None or self.logged_user_id == None:
			self.get_user_identity()
		
		return self.logged_user, self.logged_user_id
	
	# ######################################################################################

	def set_movie_rating(self, movie_id, rating):
		if self.is_logged():
			if movie_id.startswith('#movie#'):
				movie_id = movie_id[7:]
			return self.do_request( 'film/%d/my-rating' % int(movie_id), 'rating=%d' % int(rating) )
		
		return None
	
	# ######################################################################################
	
	def search_by_name( self, name, offset=0, limit=10 ):
		name = quote_plus( name )

		return self.do_request( 'search?q=%s&offset=%d&limit=%d' % ( name, offset, limit ) )
	
	# ######################################################################################

	def autocomplete_by_name( self, name, offset=0, limit=10 ):
		name = quote_plus( name )

		return self.do_request( 'autocomplete?q=%s&offset=%d&limit=%d' % ( name, offset, limit ) )
	
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

	def get_tv_stations( self ):
		return self.do_request( 'tv/stations' )
			
	# ######################################################################################

	def set_tv_stations( self, stations ):
		if type(stations) == list:
			data = '%2C'.join(str(sid) for sid in stations)
		else:
			data = stations
		return self.do_request( 'tv/stations', data='stations=' + data )
	
	# ######################################################################################
	
	def set_all_tv_stations( self ):
		sl = []
		need_set = False
		try:
			for station in self.get_tv_stations()['stations']:
				sl.append(station['id'])
				if station['selected'] == False:
					need_set = True
			
			if need_set:
				self.set_tv_station( sl )
				
		except:
			pass

		return
	
	# ######################################################################################

	def get_tv_schedule( self, day, offset=0, limit=20 ):
		return self.do_request( 'tv/schedule/?limit=%d&offset=%d&date=%s' % (limit, offset, day) )
	
	# ######################################################################################
	
	def get_json_by_uri(self, uri, page=1, load_full=True ):
		try:
			if uri.startswith('#search_movie#'):
				LogCSFD.WriteToFile( "Searching movie: \"%s\"\n" % uri[14:], 2 )
	
				a = self.autocomplete_by_name( uri[14:], (page - 1) * 30, 30 )
				b = self.search_by_name( uri[14:], (page - 1) * 30, 30 )
				return { 'films': a['films'] + b['films'] }
				
			elif uri.startswith('#movie#'):
				LogCSFD.WriteToFile( "Requesting movie info for \"%s\"\n" % uri[7:], 2 )
	
				data1 = self.get_movie_info( uri[7:])["info"]
				ret = { "info": data1 }
				
				if load_full:
					ret["creators"] = self.get_movie_creators( uri[7:], 0, 30 )["creators"]
					
					if "root_id" in data1:
						ret["root_info"] = self.get_movie_info( data1["root_id"] )["info"]
					
					if 'parent_id' in data1:
						ret['parent_info'] = self.get_movie_info( data1['parent_id'] )['info']

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
		except:
			return { "internal_error": "download error for uri: " % uri }
		
		return { "internal_error": "unknown uri %s" % uri }
	
	# ######################################################################################

csfdAndroidClient = None

def CreateCSFDAndroidClient( ignore_checks=False, try_new_login=True ):
	LogCSFD.WriteToFile('[CSFD] CreateCSFDAndroidClient - zacatek\n', 1)

	global csfdAndroidClient
	
	if csfdAndroidClient == None:
		# create anonymous session
		csfdAndroidClient = CSFDAndroidClient()

	if csfdAndroidClient.is_logged():
		LogCSFD.WriteToFile('[CSFD] CreateCSFDAndroidClient - aktualni session jiz je autorizovana\n', 1)
		LogCSFD.WriteToFile('[CSFD] CreateCSFDAndroidClient - konec\n', 1)
		return
		
	if ignore_checks == False:
		if not config.misc.CSFD.LoginToCSFD.getValue():
			LogCSFD.WriteToFile('[CSFD] CreateCSFDAndroidClient - neprihlasovat do CSFD\n', 1)
			LogCSFD.WriteToFile('[CSFD] CreateCSFDAndroidClient - konec\n', 1)
			return
		
		if int(time.time()) - config.misc.CSFD.LastLoginError.getValue() < config.misc.CSFD.LoginErrorWaiting.getValue() * 60:
			LogCSFD.WriteToFile('[CSFD] CreateCSFDAndroidClient - jeste nevyprsel casovy limit z duvodu login chyby\n', 1)
			LogCSFD.WriteToFile('[CSFD] CreateCSFDAndroidClient - konec\n', 1)
			return
		
		if not internet_on():
			config.misc.CSFD.LastLoginError.setValue(int(time.time()))
			config.misc.CSFD.LastLoginError.save()
			LogCSFD.WriteToFile('[CSFD] CreateCSFDAndroidClient - neni funkcni internet\n', 1)
			LogCSFD.WriteToFile('[CSFD] CreateCSFDAndroidClient - konec\n', 1)
			return

	login_token = config.misc.CSFD.TokenCSFD.getValue()
	
	if login_token == None or login_token == '':
		# login anonymous session
		csfdAndroidClient.login( config.misc.CSFD.UserNameCSFD.getValue(), config.misc.CSFD.PasswordCSFD.getValue() )
		
		# save login token
		login_token = csfdAndroidClient.get_login_token()
		config.misc.CSFD.TokenCSFD.setValue( login_token )
		config.misc.CSFD.TokenCSFD.save()
		
		if login_token == None or login_token == '':
			config.misc.CSFD.LastLoginError.setValue(int(time.time()))
			config.misc.CSFD.LastLoginError.save()
			LogCSFD.WriteToFile('[CSFD] CreateCSFDAndroidClient - selhalo - spatne jmeno/heslo nebo jina chyba\n', 1)
		else:
			LogCSFD.WriteToFile('[CSFD] CreateCSFDAndroidClient - login token: ' + login_token + '\n', 1)

	else:
		# create authorized session using login_token
		csfdAndroidClient = CSFDAndroidClient(login_token)
		
		try:
			# check if login token is ok
			csfdAndroidClient.get_user_identity()
			csfdAndroidClient.set_all_tv_stations()
		except:
			# clean old login token
			config.misc.CSFD.TokenCSFD.setValue('')
			config.misc.CSFD.TokenCSFD.save()
			
			# create anonymous session
			csfdAndroidClient = CSFDAndroidClient()

			# try new login
			if try_new_login:
				CreateCSFDAndroidClient(True, False)
			else:
				LogCSFD.WriteToFile('[CSFD] CreateCSFDAndroidClient - login failed\n', 1)
		
		LogCSFD.WriteToFile('[CSFD] CreateCSFDAndroidClient - mam prihlasovaci token\n', 1)

	LogCSFD.WriteToFile('[CSFD] CreateCSFDAndroidClient - konec\n', 1)
	return

CreateCSFDAndroidClient()
