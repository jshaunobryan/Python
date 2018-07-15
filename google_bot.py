import webbrowser, requests
webbrowser.open("http://ezproxy.sfpl.org/login?url=http://www.referenceusa.com/")

url = 'http://ezproxy.sfpl.org/login'
values = {'name': '21223203815652',
			'pin': '7451'}
r = requests.post(url, data=values)
#print r.content