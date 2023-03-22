# SLACK_BOT_TOKEN = "YOUR_TOKEN"
# SLACK_APP_TOKEN = "YOUR_TOKEN"
# OPENAI_API_KEY  = "YOUR_TOKEN"

import os
import openai
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack import WebClient
from slack_bolt import App

os.environ['SLACK_BOT_TOKEN'] = 'xoxb-585973544673-4981785562195-XF1B8jJMAIZcJIv8a2LZp1eY'
os.environ['SLACK_APP_TOKEN'] = 'xapp-1-A04UVQHUDBL-4981890774642-f9edd01ebb63d09393bb692d41e88ee9b43f996e5734708a6412f6cf140bce59' 
os.environ['OPENAI_API_KEY']  = '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'

# Event API & Web API
app = App(token=os.environ['SLACK_BOT_TOKEN']) 
client = WebClient(os.environ['SLACK_BOT_TOKEN'])

# This gets activated when the bot is tagged in a channel    
@app.event("app_mention")
def handle_message_events(body, logger):
    # Log message
    print(str(body["event"]["text"]).split(">")[1])
    
    # Create prompt for ChatGPT
    prompt = str(body["event"]["text"]).split(">")[1]
    
    qna = f"Q: {prompt}\nA:"
    
    # Let the user know that we are busy with the request 
    # response = client.chat_postMessage(channel=body["event"]["channel"], 
    #                                    thread_ts=body["event"]["event_ts"],
    #                                    text=f"Hello from your bot! :robot_face: \nThanks for your request, I'm on it!")
    
    # Check ChatGPT
    openai.api_key = os.environ['OPENAI_API_KEY']
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=qna,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5).choices[0].text
    
    
    # Reply to thread 
    response = client.chat_postMessage(channel=body["event"]["channel"], 
                                       thread_ts=body["event"]["event_ts"],
                                       text=response)

if __name__ == "__main__":
    SocketModeHandler(app, 
                      os.environ['SLACK_APP_TOKEN']).start()
