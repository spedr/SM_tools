import ijson
import unidecode
import re
from datetime import datetime




csvfname = 'rts.csv'
csvfile = open(csvfname, 'w')

csvfile.write('username\tretweet_count\ttext\tpermalink\n')

json_export_file_path = 'rt_count/bbb18.json'

import re
def remove_emoji(string):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)


with open(json_export_file_path, 'r') as f:
    objects = ijson.items(f, 'item')
    items = list(objects)


most_retweeted_list = []
list_is_full = False

for tweet in items:
    tweet['text'] = remove_emoji(tweet['text'])


count = 0
for tweet in items:
    #if 'RT @' in tweet['text']:
    #    pass
    if tweet['retweet_count'] > 50:
    #    for t2 in most_retweeted_list:
    #        if t2['text'] == tweet['text']:
    #            pass
    #        else:
        flag = True
        try:
            if tweet['lang'] == 'pt':
                if 'RT @' in tweet['text']:
                    tweet['text'] = tweet['text'].split(' ', 2)[2]
                    for tw in most_retweeted_list:
                        if tweet['text'] == tweet['text']:
                            flag = False
                            count+=1
                            #print (count)
                            #break
                    if flag:
                        most_retweeted_list.append(tweet)
                        #count+=1
                        #print (count)
                    else:
                        #count+=1
                        #print (count)
                        pass

                else:
                    most_retweeted_list.append(tweet)
                    #count+=1
                    #print (count)
        except:
            pass

count = 0
f = open ('link_list.txt', 'w')
from requests.exceptions import HTTPError
from urllib.request import urlopen
import urllib
import time
from bs4 import BeautifulSoup
for tweet in sorted(most_retweeted_list, key = lambda x: x['retweet_count'], reverse=True):
    try:
        if count >= 150:
            break
        print ('https://twitter.com/i/web/status/' + str(tweet['id']))
        page = urlopen('https://twitter.com/i/web/status/'+str(tweet['id']))
        page_source = page.read()
        soup = BeautifulSoup(page_source, 'html.parser')
        rt_counthtml = soup.find(class_='js-stat-count js-stat-retweets stat-count')

        if rt_counthtml != None:
            tweet['retweet_count'] = int(rt_counthtml.a['data-tweet-stat-count'])
            count+=1
            time.sleep(1)
        else:
            print ('suspended?')
            most_retweeted_list.remove(tweet)
    except urllib.error.HTTPError:
        pass
        most_retweeted_list.remove(tweet)


count = 0
print ('\n#########   Printing most retweeted tweets   #########\n')
for tweet in sorted(most_retweeted_list, key = lambda x: x['retweet_count'], reverse=True):

    #print tweet['created_at_datetime']
    #print '@' + tweet['nome']
    print (tweet['text'])
    print ('Retweeted: ' + str(tweet['retweet_count']))
    print ('\n')
    f.write(str(tweet['id']))
    f.write('\n')
    csvtext = ' '.join([line.strip() for line in tweet['text'].strip().splitlines()])
    csvstring = tweet['username'] + '\t' + str(tweet['retweet_count']) + '\t' + csvtext + '\thttps://twitter.com/i/web/status/' + str(tweet['id']) + '\n'
    csvfile.write(csvstring.encode('utf-16', 'surrogatepass').decode('utf-16'))

    if count == 150:
        break
    count+=1
