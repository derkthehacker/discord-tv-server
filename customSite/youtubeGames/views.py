from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from game_queue import game_queue
import requests as req
import asyncio, re, os

"""
'https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&id=Ks-_Mh1QhMc&key=[YOUR_API_KEY]' \
  --header 'Authorization: Bearer [YOUR_ACCESS_TOKEN]' \
  --header 'Accept: application/json' \
"""

async def get_game_list():
    games = game_queue()
    game = await games.create_queue(1)
    return(game[0])

def getSeconds(time):
    total_time = 0
    hour = re.search('([0-9])+H', time)
    if hour != None:
        hour = hour.group(0)
        hour = hour[:-1]
        total_time += int(hour) * 60 * 60
    minute = re.search('([0-9])+M', time)
    if minute != None:
        minute = minute.group(0)
        minute = minute[:-1]
        total_time += int(minute) * 60
    second = re.search('([0-9])+S', time)
    if second != None:
        second = second.group(0)
        second = second[:-1]
        total_time += int(second)
        total_time = total_time * 1000
    return(total_time)

def get_duration(game):
    api_token = os.env('YouTube_API')
    url = 'https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&id={id}&key={key}'.format(id=game, key = api_token)
    response = req.get(url=url)
    resp = response.json()
    duration = resp['items'][0]['contentDetails']['duration']
    return(getSeconds(duration))

# Create your views here.
def index(request):
    #nest_asyncio.apply()
    game = asyncio.run(get_game_list())
    time = get_duration(game)
    game = 'https://www.youtube.com/embed/' + game + '?autoplay=1&mute=1&enablejsapi=1'
    #template = loader.get_template("gamePull/index.html")
    #context = {"video": game}
    return render(request, "gamePull/index.html", {"video": game, "reload": time})
    #return HttpResponse(template.render(context, request))
    
