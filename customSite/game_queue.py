import pandas as pd
import numpy as np
from requests_html import AsyncHTMLSession
import random
import asyncio
import re


class game_queue:
    def __init__(self, game_list_weights = {'CSGO': [.33], 'MW2': [.33], 'TARKOV': [.16], 'TF2': [.17]}):
        self.game_list_weights = game_list_weights
        self.queue = []

    async def __pick_game(self, game_list):
        #select a random number from 0-1
        current_weight = 0
        random.seed(None)
        random_number = random.random()
        #print(random_number)

        #Calculate game list weighting. Update to handle numbers that don't add up to 1 in the future. Average out from total w/value.
        for item in range(0, len(game_list)): 
             game = list(game_list.keys())[item]

             if item == 0:
                 previous_weight = game_list[game][0]
                 game_list[game][0] = 0
                 game_list[game].append(previous_weight)
                 current_weight += game_list[game][1]
                 continue
             
             previous_weight = game_list[game][0] 
             game_list[game][0] = current_weight

             #remove this. Code shit
             if(item == len(game_list)):
                 game_list[game].append(1)
                 break

             game_list[game].append(previous_weight + game_list[game][0])
             current_weight = game_list[game][1]

        #Select game from random number. inneficient, yes
        for item in game_list:
             if(random_number >= game_list[item][0] and random_number <= game_list[item][1]):
                return item

    #generates the url with the game name in mind. Will add modifications to the game query.
    async def __generate_url(self, game):
        return 'https://www.youtube.com/results?search_query={game}+clips'.format(game=game)
    
    #returns a url for a video :D
    async def __find_video(self, url):
        session = AsyncHTMLSession()
        response = await session.get(url)
        await response.html.arender(sleep=1, keep_page = True, scrolldown = 2, timeout = 20)
        video_arr = []
        for links in response.html.find('a#video-title'):
            link = next(iter(links.absolute_links))
            video_arr.append(link)
        await session.close()
        choice = random.choice(video_arr)
        id = re.search('v=([a-zA-Z0-9_-])+', choice)
        id = id.group(0)[2:]
        return id
        #print(id[0])
        #embeded  = 'https://www.youtube.com/embed/' + id + '?autoplay=1&mute=1&enablejsapi=1'
        #return embeded
    
    async def add_video(self, video):
        self.queue.append(video)

    async def remove_video(self):
        self.queue.pop(0)
    
    async def create_queue(self, size):
        for i in range(0, size):
            game = await self.__pick_game(self.game_list_weights)
            url = await self.__generate_url(game)
            video = await self.__find_video(url)
            await self.add_video(video)
        print(self.queue)
        return(self.queue)
        
async def main():
    games = game_queue()
    await games.create_queue(2)

if __name__ == '__main__':
    asyncio.run(main())