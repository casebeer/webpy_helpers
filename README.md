# Web.py Helpers

Helper module for the [web.py][webpy] HTTP framework. 

<tt>webpy_helpers</tt> provides HTTP status and error objects that allow customization of their messages and content types. 

These helpers can be used to return JSON objects with messages and debugging information when using web.py to build an HTTP API. 

## Examples

### Status code exceptions

Use the provided status code exeptions in place of web.py-provided exceptions to customize the messages and content types of your non-200 responses. 

For example, to change the text of the 404 message from the default "not found," instead of:

    ...
    	raise web.notfound()
    ...

use:

    import webpy_helpers
    ...
    class Foo:
    	def GET(self, id):
    		if id not in data:
    			raise webpy_helpers.NotFound(
    					message="Your object ID does not exist",
    					headers={"Content-type":"text/plain"}
    					)

Note that we're also changing the Content-type header to text/plain, since this is just a plain text message, not an HTML document. 

Using this NotFound class, you could return a JSON error body by setting the Content-type header to application/json and serializing an object to a JSON string. The JsonNotFound class does this for you:

    ...
    class FooApi:
    	def GET(self, id):
    		if id not in data:
    			raise webpy_helpers.JsonNotFound(
							message={
								"message":"Your object ID does not exist",
								"id":id,
								"object_list":"http://example.com/list_of_all_objects"
							}
						)

In this case, the message argument must be a JSON-serializable object which should be returned to the client.

Returning a JSON object as an error page body can make it easier for programmatic HTML clients to parse specific information about the error that occured. In the example above, a client could follow the "object_list" link to get a list of valid IDs to try. 

Note that machine readable error page bodies *are not* a replacement for returning correct HTTP status codes: You *must* still set the correct status code to indicate via HTTP what error or status occured. 

For example, it would be wrong to say `{"error":"You provided bad data"}` with a 500 status code, even if the request caused server code to throw an exception. In this case, the error was the client's fault, so a 400 status code would be appropriate. A status code of 500 indicates that the fault lies with the server.

Similarly, returning a message `{"error":"the server crashed"}` with a 404 status code would also be wrong, since an error made by the server should have a 500 status code. 

See the [HTTP Status Code Definitions][httpcodes].

[webpy]: http://webpy.org/
[httpcodes]: http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html
