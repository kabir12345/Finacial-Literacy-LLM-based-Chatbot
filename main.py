from flask import Flask
from flask import request
from flask import Response
import requests 
import openai
import random
import json
import sys
from importlib import reload 	


random.randint(0, 9)
TOKEN = "6131219520:AAHMdyXIDsQYw02_VXyxfLnAivnJqPTa31M"
app = Flask(__name__)
def gpt_reply(prompt):
    model_engine = "text-davinci-003"
    prompt = prompt
    max_tokens = 350
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=0.5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0)
    a=completion.choices[0].text
    a = a.replace("'","")
    a.replace('\n','')
    return a


    
def parse_message(message):
    chat_id = message['message']['chat']['id']
    txt = message['message']['text']
    print("chat_id-->", chat_id)
    return chat_id,txt

def tel_send_image(chat_id,prompt):
    apikey = "AIzaSyBdf22iIr3MA-fDHWT-lwtWmJV0-OLmfQM"  # click to set to your apikey
    lmt = 8
    ckey = "my_test_app"
    contentFilter="med"  # set the client_key for the integration and use the same value for all API calls
    search_term = str(gpt_reply(prompt+'summarize this topic of this question in one word'))+"meme"
    print(search_term)
    r = requests.get(
    "https://tenor.googleapis.com/v2/search?q=%s&key=%s&client_key=%s&limit=%s&contentFilter=%s" % (search_term, apikey, ckey,  lmt, contentFilter))
    if r.status_code == 200:
    # load the GIFs using the urls for the smaller GIF sizes
        top_8gifs = json.loads(r.content)
        gifurl=top_8gifs['results'][3]['url']
    else:
        return None
    url = f'https://api.telegram.org/bot{TOKEN}/sendPhoto'
    payload = {
        'chat_id': chat_id,
        'photo': gifurl,

    }
 
    r = requests.post(url, json=payload)
    return r
def tel_send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
                'chat_id': chat_id,
                'text': text
                }
   
    r = requests.post(url,json=payload)
    return r
 
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
       
        chat_id,txt = parse_message(msg)
        if len(txt) > 6:
            t=random.randint(1, 5)
            if t==1 or t==2 or t==3:
                tel_send_message(chat_id,gpt_reply(txt+"answer this question in a quirky way to a teenager"))
                tel_send_image(chat_id,txt)
            elif t==3 or t==4:
                tel_send_message(chat_id,gpt_reply(txt))
                
            else:
                tel_send_message(chat_id,gpt_reply(txt))
        elif len(txt)<=6:
            tel_send_message(chat_id,"Hi, I am Penny The Bot how can I help you today?")
        elif txt=="/start":
            tel_send_message(chat_id,"Lets start. Tell me how can I help you with your finances?")
        else:
            tel_send_message(chat_id,'Sorry I might be facing some problems')
       
        return Response('ok', status=200)
    else:
        return "<h1>Welcome!</h1>"
 
if __name__ == '__main__':
   app.run(debug=True)