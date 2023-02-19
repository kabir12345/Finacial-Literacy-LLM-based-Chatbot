import openai
import requests
import json
def gpt_reply(prompt):
    model_engine = "text-davinci-003"
    prompt = prompt
    max_tokens = 500
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=0.5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0)
    print(completion.choices[0].text)

prompt=("What is fincace answer in aquirky way to a teenager?")
gpt_reply(prompt)


apikey = "AIzaSyBdf22iIr3MA-fDHWT-lwtWmJV0-OLmfQM"  # click to set to your apikey
lmt = 8
ckey = "my_test_app"  # set the client_key for the integration and use the same value for all API calls

# our test search
search_term = gpt_reply(prompt+'summarize this topic of this question in one word with a happy feeling')

# get the top 8 GIFs for the search term
r = requests.get(
    "https://tenor.googleapis.com/v2/search?q=%s&key=%s&client_key=%s&limit=%s" % (search_term, apikey, ckey,  lmt))

if r.status_code == 200:
    # load the GIFs using the urls for the smaller GIF sizes
    top_8gifs = json.loads(r.content[1])
    print(top_8gifs)
else:
    top_8gifs = None