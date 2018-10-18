

fname = 'link_list.txt'
with open(fname) as f:
    content = f.readlines()
content = [x.strip() for x in content]


html_page_name = 'top_rts.html'

html_page = open(html_page_name, 'w')

html_page.write('<!DOCTYPE html><html>')

head = """
<meta charset="UTF-8"> 
<head>
	<title>Ranking de Tweets</title>
	<link href="https://fonts.googleapis.com/css?family=Roboto:400,100italic" rel="stylesheet" type="text/css">
"""

style = """
	<style>
		body {
			font-family: 'Roboto', sans-serif;
		}
		#wrap {
			width: 774px;
			margin: 10% auto;
		}
		h1 {
			font-style: italic;
			font-weight: 100;
			font-size: 4em;
		}
	</style>
</head>
"""

body1 = """
<body>
	<div id="wrap">
		<h3>Ranking de Tweets</h3>
		<div>
"""




html_page.write(head)
html_page.write(style)
html_page.write(body1)




#import urllib2
import time
from requests.exceptions import HTTPError
from urllib.request import urlopen
import urllib

import json

count = 0
def get_oembed(id):
    global count
    global html_page
    oembed = 'https://api.twitter.com/1.1/statuses/oembed.json?id='
    try:
        #response = urllib2.urlopen(oembed+id)
        #page_source = response.read()


        page = urlopen(oembed+id)
        page_source = page.read()
        #print (str(page_source))

        json_element = json.loads(page_source.decode('utf-8'))
        #print (json_element['html'])
        count +=1
        html_page.write('<p>' + str(count) + '.</p>')
        html_page.write(json_element['html'])
        html_page.write('<br>')
    except urllib.error.HTTPError:
        pass
    except urllib.error.URLError:
        pass
        time.sleep(3)
        get_oembed(id)


for id in content:
    if count == 150:
        break
    get_oembed(id)

body2 = """
		</div>
	</div>
</body>
</html>
"""

html_page.write(body2)
html_page.close()
