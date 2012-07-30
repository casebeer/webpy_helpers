#### web.py helpers 

import web
try:
	import simplejson as json
except ImportError:
	import json

#### Util class and function 

class _HTTPError(web.HTTPError):
	"""Base class for customized error message bodies"""
	message = None
	def __init__(self,message=None,headers={"Content-type":"text/html"}):
		if message == None:
			message = self.message if self.message else self.status[1]
		web.HTTPError.__init__(self, " ".join(self.status), headers, message)
		#print(self, " ".join(self.status), headers, message if message else self.status[1])

def _make_json_init(init_f):
	"""Wrap an error class __init__ function and prep to return JSON, not HTML."""
	def __init__(
				self,
				message=None,
				headers={"Content-type":"application/json"}
				):
		if not message:
			message = {"message":self.status[1]}
		if isinstance(message, basestring):
			message = {"message":unicode(message)}
		init_f(self, json.dumps(message), headers)
	return __init__

class _JsonHttpErrorMeta(type):
	'''Metaclass to create error subclass with JSON response body from _HTTPError subclass.'''
	def __new__(self, name, bases, dir):
		overrides = {
			'__init__': _make_json_init(bases[0].__init__),
			'__doc__': "%s with JSON response body" % bases[0].__doc__,
		}
		# override __init__ and __doc__ of base class, but only if not explicitly set in subclass
		overrides.update(dir)
		return type.__new__(self, name, bases, overrides)

#### API
class BadRequest(_HTTPError):
	'''Allow customized messages on 400 errors'''
	status = "400", "Bad Request"
class JsonBadRequest(BadRequest):
	__metaclass__ = _JsonHttpErrorMeta

class Unauthorized(_HTTPError):
	'''Allow customized messages on 401 errors'''
	status = "401", "Unauthorized"
class JsonUnauthorized(Unauthorized):
	__metaclass__ = _JsonHttpErrorMeta

class Forbidden(_HTTPError):
	'''Allow customized messages on 403 errors'''
	status = "403", "Forbidden"
class JsonForbidden(Forbidden):
	__metaclass__ = _JsonHttpErrorMeta

class NotFound(_HTTPError):
	'''Allow customized messages on 404 errors'''
	status = "404", "Not Found"
class JsonNotFound(NotFound):
	__metaclass__ = _JsonHttpErrorMeta

class MethodNotAllowed(_HTTPError):
	'''Allow customized messages on 405 errors'''
	status = "405", "Method Not Allowed"
class JsonMethodNotAllowed(MethodNotAllowed):
	__metaclass__ = _JsonHttpErrorMeta
# for web.py compat
NoMethod = MethodNotAllowed
JsonNoMethod = JsonMethodNotAllowed

class Gone(_HTTPError):
	'''Allow customized messages on 410 errors'''
	status = "410", "Gone"
class JsonGone(Gone):
	__metaclass__ = _JsonHttpErrorMeta

class Conflict(_HTTPError):
	'''Allow customized messages on 409 errors'''
	status = "409", "Conflict"
class JsonConflict(Conflict):
	__metaclass__ = _JsonHttpErrorMeta

class UnsupportedMediaType(_HTTPError):
	'''Allow customized messages on 415 errors'''
	status = "415", "Unsupported Media Type"
class JsonUnsupportedMediaType(UnsupportedMediaType):
	__metaclass__ = _JsonHttpErrorMeta

class RequestedRangeNotSatisfiable(_HTTPError):
	'''Allow customized messages on 415 errors'''
	status = "416", "Requested Range Not Satisfiable"
class JsonRequestedRangeNotSatisfiable(RequestedRangeNotSatisfiable):
	__metaclass__ = _JsonHttpErrorMeta

class InternalServerError(_HTTPError):
	'''Allow customized messages on 500 errors'''
	status = "500", "Internal Server Error"
class JsonInternalServerError(InternalServerError):
	__metaclass__ = _JsonHttpErrorMeta
# web.py compat
InternalError = InternalServerError
JsonInternalError = JsonInternalServerError


