import aiohttp
import json

URL = 'https://gitlab.easy-dev.ru'
token = 'glpat-fX6f8x_XAaq_Qkb-KiHc'


async def get_data(url, token, project_id):
    header = {'PRIVATE-TOKEN': token}
   

    data = await aiohttp.ClientSession(url, headers=header).get(f'/api/v4/projects/{project_id}/events')
    
    return data

async def post_to_server(url, token, project_id, chat_id, data):
    url = 'http://127.0.0.1:8000'

    resp = await aiohttp.ClientSession(url).post('/api/create/', 
                                                                 
                                                                 data={
                                                                     'chat_id' : chat_id,
                                                                     'json' : json.dumps(data),
                                                                     'project_id' : project_id,
                                                                     'token' : token,
                                                                     'url' : url,
   
                                                                 })
    return resp

async def get_from_server(chat_id):
    url = 'http://127.0.0.1:8000'
    data = await aiohttp.ClientSession(url).get(f'/api/{chat_id}/')
    res = await data.json()
    
    return res


async def patch_to_server(chat_id, data):
    url = 'http://127.0.0.1:8000'

    resp = await aiohttp.ClientSession(url).patch(f'/api/{chat_id}/', data={'json' : json.dumps(data)})
                                                                 
                                                                                                                            
                                                                
                                                                
    return resp
