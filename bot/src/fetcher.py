import aiohttp
import json

URL = 'https://gitlab.easy-dev.ru'
token = 'glpat-fX6f8x_XAaq_Qkb-KiHc'


async def get_data(url, token, project_id):
    header = {'PRIVATE-TOKEN': token}
   

    async with aiohttp.ClientSession(url, headers=header) as session:

        resp = await session.get(f'/api/v4/projects/{project_id}/events')
        data = await resp.json()
        resp.close()
        return data




async def post_to_server(url, token, project_id, chat_id, data):
    url = 'http://127.0.0.1:8000'

    async with aiohttp.ClientSession(url) as session:

        resp = await session.post('/api/create/', 
                                                                    
                                                                    data={
                                                                        'chat_id' : chat_id,
                                                                        'json' : json.dumps(data),
                                                                        'project_id' : project_id,
                                                                        'token' : token,
                                                                        'url' : url,
    
                                                                    })
        
        data = await resp.json()
        resp.close()
        return data


async def get_from_server(chat_id):
    url = 'http://127.0.0.1:8000'
    async with aiohttp.ClientSession(url) as session:

        try:
            resp = await session.get(f'/api/{chat_id}/')
            if resp.status != 500:
                data = await resp.json()
                resp.close()
                return data
            else:
                resp.close()
                return 500
        except:
            resp.close()
            return 500
    


async def patch_to_server(chat_id, data):
    url = 'http://127.0.0.1:8000'
    async with aiohttp.ClientSession(url) as session:
        resp = await session.patch(f'/api/{chat_id}/', data={'json' : json.dumps(data)})
        data = await resp.json()
        resp.close()
                                                                    
        return data
