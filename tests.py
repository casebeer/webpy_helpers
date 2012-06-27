
from paste.fixture import TestApp
from nose.tools import *

import itertools

import web
import webpy_helpers

class TestController(object):
	@classmethod
	def path(cls):
		return "/%s" % cls.__name__

#### Web.py controller classes testing each exception
class BadRequest(TestController):
	status = 400
	body = "foobar"
	def GET(self):
		raise webpy_helpers.BadRequest("foobar")
class JsonBadRequest(BadRequest):
	body = """{"message": "foobar"}"""
	def GET(self):
		raise webpy_helpers.JsonBadRequest({"message":"foobar"})
class JsonBadRequest_string(JsonBadRequest):
	def GET(self):
		raise webpy_helpers.JsonBadRequest("foobar")

class NotFound(TestController):
	status = 404
	body = "foobar"
	def GET(self):
		raise webpy_helpers.NotFound("foobar")
class JsonNotFound(NotFound):
	body = """{"message": "foobar"}"""
	def GET(self):
		raise webpy_helpers.JsonNotFound({"message":"foobar"})
class JsonNotFound_string(JsonNotFound):
	def GET(self):
		raise webpy_helpers.JsonNotFound("foobar")

# enumerate all test classes
classes = [cls for name,cls in locals().items() if type(cls) == type and issubclass(cls, TestController) and cls != TestController ]

urls = tuple(itertools.chain(*[(cls.path(), cls) for cls in classes]))

print urls

app = web.application(urls, globals())

def setup():
	global test_app
	test_app = TestApp(app.wsgifunc())

def test_runner():
	for cls in classes:
		yield run, cls.path(), cls.status, cls.body

def run(path, status, body):
	res = test_app.get(path, expect_errors=True)
	assert_equal(res.status, status)
	assert_equal(res.body, body)

