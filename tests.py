'''
Tests for webpy_helpers

- Automatically generated web.py test controllers for all HTTPError
  exceptions.

Run tests via Nose:

    $ nosetests
    ....................................
    ----------------------------------------------------------------------
    Ran 36 tests in 0.372s
    
    OK

or setup.py:

    $ python setup.py test

TODO: More in depth manual testing of basic exception funcationality
      for one HTTPError subclass, since most behavior is shared amongst 
	  all the error classes via subclassing and metaclasses. 
'''

from paste.fixture import TestApp
from nose.tools import *

import itertools
import json

import web
import webpy_helpers

# Dictionary to automatically generate test controllers
#
# For each key, the corresponding class with the same name, plus the
# class with that name preceded by "Json" in the webpy_helpers module
# will be exercised, basic expected functionality checked, and the 
# HTTP status code compared to the key's value.
tests = {
	"BadRequest": 400,
	"Unauthorized": 401,
	"Forbidden": 403,
	"NotFound": 404,
	"MethodNotAllowed": 405,
	"NoMethod": 405,
	"Conflict": 409,
	"Gone": 410,
	"UnsupportedMediaType": 415,
	"RequestedRangeNotSatisfiable": 416,
	"InternalServerError": 500,
	"InternalError": 500,
}

class TestController(object):
	'''Base class for all web.py test controllers.'''
	@classmethod
	def path(cls):
		return "/%s" % cls.__name__

def make_class(status_code, class_name, test_name, message_argument, expected_body):
	'''Generate a subclass of TestController with an automatically generated GET method.'''
	return type("%s%sTest" % (class_name, test_name),
		(TestController,),
		{
			'status': status_code,
			'body': expected_body,
			'GET': make_GET_method(class_name, message_argument)
		}
	)

def make_GET_method(class_name, message_argument):
	if message_argument:
		def GET(self):
			raise getattr(webpy_helpers, class_name)(message_argument)
	else:
		def GET(self):
			raise getattr(webpy_helpers, class_name)()
	return GET

def make_webpy_controllers(status_code, class_name):
	'''
	Make test controllers for a particular HTTP Error class

	For the provided status code and class name, generate three test controllers:

	1. For the named class, testing that HTML messages are passed through.
	2. For the class name prefixed with "Json," testing that JSON dicts are
	   passed through as response bodies.
	3. For the class name prefied with "Json," testing that string messages are
	   properly wrapped in JSON dicts and passed through as response bodies.
	'''

	html_test_class = make_class(
								status_code,
								class_name,
								"Html",
								"<p>This is the HTML test message.</p>",
								"<p>This is the HTML test message.</p>"
								)
	json_test_class = make_class(
								status_code,
								"Json%s" % (class_name,),
								"",
								{"message" : "This is the JSON dict-based test message."},
								{"message" : "This is the JSON dict-based test message."}
								)
	json_string_test_class = make_class(
								status_code,
								"Json%s" % (class_name,),
								"String",
								"This is the JSON str-based test message.",
								{"message": "This is the JSON str-based test message."}
								)
	return [html_test_class, json_test_class, json_string_test_class]

#### Gather the web.py controller classes testing each exception

# generate automatic test controllers
controllers = list(itertools.chain.from_iterable(
	[
		make_webpy_controllers(status, class_name) 
		for class_name, status 
		in tests.items()
	]
))

# include any manual test controllers by searching for all subclasses of TestController 
# (but not TestController itself) in the local scope
controllers += [
	obj
	for object_name, obj
	in locals().items() 
	if type(obj) == type and issubclass(obj, TestController) and obj != TestController
]

# sort test controllers by response code and class name for testing in order
controllers = sorted(controllers, key=lambda cls: (cls.status, cls.__name__))

#### Nose testing functions

def setup():
	'''Set up a web.py application to use for testing.'''
	global test_app
	# generate a tuple of paths and controller classes to set up web.py routing
	urls = tuple(itertools.chain.from_iterable(
		[
			(controller.path(), controller) 
			for controller 
			in controllers
		]
	))
	app = web.application(urls, globals())
	test_app = TestApp(app.wsgifunc())

def test():
	'''Test runner for coverage of all classes.'''
	print "%d classes to test" % len(list(controllers))
	for cls in controllers:
		test.__doc__ = """Testing status %s, controller %s""" % (cls.status, cls.__name__)
		yield run, cls

def run(cls):
	'''Run a specific test using the web.py test API to call and check a particular path.'''
	response = test_app.get(cls.path(), expect_errors=True)
	assert_equal(response.status, cls.status)
	if hasattr(cls.body, 'keys'):
		# we expect a dictionary, so json decode the body and compare raw dicts
		try: 
			assert_equal(json.loads(response.body), cls.body)
		except ValueError,e:
			print "Error decoding JSON body (%s):\n\t%s\nexpected:\n\t%s" % (e, response.body, json.dumps(cls.body))
			raise
	else:
		assert_equal(response.body, cls.body)

if __name__ == '__main__':
	import sys
	sys.stderr.write("Error, please run tests using nosetests.\n")
	sys.exit(1)

