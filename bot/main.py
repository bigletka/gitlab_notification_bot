import logging, requests

from aiogram import Bot, Dispatcher, executor, types
from src.fetcher import get_data, get_from_server, post_to_server, patch_to_server
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
  

import time 



API_TOKEN = '6239884419:AAGxzyR4xtD3g5v-q8x0wcR9ffugRiCjFgE'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher


bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    token = State()
    url = State() 
    project_id = State()

    
@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.reply('Cancelled. To start write /start', reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(commands='start')    
async def start(message: types.Message):

    await Form.token.set()
    await message.answer('Please, write your gitlab personal access token')


@dp.message_handler(state=Form.token)
async def process_token(message: types.Message, state: FSMContext):
    """
    Process user name
    """
    async with state.proxy() as data:
        data['token'] = message.text

    await Form.next()
    await message.answer("Base url? Example: https://gitlab.easy-dev.ru")
   

@dp.message_handler(state=Form.url)
async def process_url(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['url'] = message.text

    await Form.next()
    await message.answer("Project id?")




@dp.message_handler(state=Form.project_id)
async def send_notification(message: types.Message, state: FSMContext):
    while True:
        async with state.proxy() as data:
            data['project_id'] = message.text
            data['projects'] = []
            data['chat_id'] = message.chat.id
       


       
            response_from_api = await get_data(token=data['token'], url=data['url'], project_id=data['project_id'])
            
          
            response_from_server = await get_from_server(data['chat_id'])
            

            if response_from_server != 500:
                data_from_server = response_from_server['json']
                data_to_show = [i for i in data_from_server + response_from_api if i not in data_from_server or i not in data_from_server]
                resp = await patch_to_server(chat_id=data['chat_id'], data=response_from_api)
               
               

            else:
                data_to_show = response_from_api
                resp = await post_to_server(url=data['url'], token=data['token'], project_id=data['project_id'],
                                            chat_id=data['chat_id'], data=response_from_api)
               
                
          
            for dat in data_to_show.reverse():
                if dat not in data['projects']:
                    data['projects'].append(dat)
                    action = dat['action_name']
                    user = dat['author']['name']
                    date, exact_time = dat['created_at'].split('T')
                    t=''
                        
                    if action == 'pushed to':
                        branch = dat['push_data']['ref']
                        commit = dat['push_data']['commit_title']
                        t=t+f'Branch Name: {branch} \n Title: {commit}'

                   
                    text = f'Action: {action} \n User: {user} \n Time:  {exact_time}\n  Date: {date}\n' + t
                    await message.answer(text)   
            
            time.sleep(5) 




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)