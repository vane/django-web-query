#django-web-query
Small utility that allows to manipulate django model directly from web browser or any http enabled framework.
What it does now is simply invoke querysets from models on the django. 
GET method is tested by me, other methods to be implemented soon.
Response now only in json format

##configuration
Simply put this in your urls.py where models is your application models:

<pre>
from djangowebquery import api

api.Api.registry.quick_register('/api/v1/', models)
</pre>

and add this url to your urls patterns

<pre>
url(r'^api/', api.Api.urls)
</pre>
now try to put url with name of your model like that

<pre>
http://127.0.0.1:8000/api/v1/Test/?data=[] 
</pre>

where Test is name of your model

Now look for more specific examples:
<pre>
http://127.0.0.1:8000/api/v1/Test/?data=[{"order_by":"-date"},{"filter":{"name_id__in":[1, 2, 6, 10, 11, 21, 26, 27, 29, 32, 36]}},{"filter":{"date":{"date__range":["2014.11.04 00:00 UTC", "2014.11.06 23:59 UTC"]}}},{"limit":{"start":null,"end":9}}]

http://127.0.0.1:8000/api/v1/Test/?data=[{"order_by":"-date"},{"limit":{"end":9}}]

http://127.0.0.1:8000/api/v1/Test/?data=[{"order_by":"-date"},{"filter":{"symbol":11}},{"limit":{"end":9}}]
</pre>
so as you see it's passing the json

##TODO
a) PUT, DELETE, POST, OPTIONS - test
<br>
b) support only get commands by url
<br>
c) examples of (fields limitation, authenticated methods, hard limits per database table)
<br>
d) other response types
<br>
e) documentation
<br>
f) tests