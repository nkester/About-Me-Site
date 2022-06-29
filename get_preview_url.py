import json

hosting = json.load(open('channels.txt','r'))

preview_url = hosting['result']['channels'][0]['url']

print(preview_url)
#with open('build.env','w') as f:
#    f.write("PREVIEW_URL={}".format(preview_url))