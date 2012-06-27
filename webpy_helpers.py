#### web.py helpers 

import web
try:
	import simplejson as json
except ImportError:
	import json

class BadRequest(web.HTTPError):
	'''Allow customized messages on 400 errors.'''
	def __init__(self,message="bad request",headers={"Content-type":"text/html"}):
		status = "400 Bad Request"
		web.HTTPError.__init__(self, status, headers, message)
class JsonBadRequest(BadRequest):
	'''Allow customized JSON responses on 400 errors.'''
	def __init__(self,
					message={"message":"Bad request"},
					headers={"Content-type":"application/json"}
				):
		if isinstance(message, basestring):
			message = {"message":unicode(message)}
		BadRequest.__init__(self, json.dumps(message), headers)

class NotFound(web.HTTPError):
	'''Allow customized messages on 404 errors.'''
	def __init__(self,message="Not found",headers={"Content-type":"text/html"}):
		status = "404 Not Found"
		web.HTTPError.__init__(self, status, headers, message)
class JsonNotFound(NotFound):
	'''Allow customized JSON responses on 404 errors.'''
	def __init__(self,
					message={"message":"Not found"},
					headers={"Content-type":"application/json"}
				):
		if isinstance(message, basestring):
			message = {"message":unicode(message)}
		NotFound.__init__(self, json.dumps(message), headers)

