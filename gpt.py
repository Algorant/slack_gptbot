#!/usr/bin/env python3

import os
import openai
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack import WebClient
from slack_bolt import App

# langchain stuff
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.prompts.chat import ChatPromptTemplate


# Keys and Tokens
os.environ['SLACK_BOT_TOKEN'] = SLACK_BOT_TOKEN
os.environ['SLACK_APP_TOKEN'] = SLACK_APP_TOKEN
os.environ['OPENAI_API_KEY']  = OPENAI_API_KEY

# Event API & Web API
app = App(token=os.environ['SLACK_BOT_TOKEN'])
client = WebClient(os.environ['SLACK_BOT_TOKEN'])


# Write ChatGPT Logic
llm = ChatOpenAI(openai_api_key=os.environ['OPENAI_API_KEY'],
             model_name="gpt-3.5-turbo",
             temperature=0,
             max_tokens=1024)

# Keep last 10 conversation exchanges in memory
window_memory = ConversationBufferWindowMemory(k=10)


@app.event("app_mention")
def handle_message_events(body, logger):
    # Log message
    print(str(body["event"]["text"]).split(">")[1])

    # Create prompt for ChatGPT
    prompt = str(body["event"]["text"]).split(">")[1]

    # # Write ChatGPT Logic
    # llm = ChatOpenAI(openai_api_key=os.environ['OPENAI_API_KEY'],
    #              model_name="gpt-3.5-turbo",
    #              temperature=0,
    #              max_tokens=1024)

    # # Keep last 10 conversation exchanges in memory
    # window_memory = ConversationBufferWindowMemory(k=10)

    # Conversation Logic
    convo = ConversationChain(
    llm=llm,
    verbose=False,
    memory=window_memory
    )

    # Get response from ChatGPT
    last_reply = convo.predict(input=prompt)

    # Feed back to Slack
    response = client.chat_postMessage(channel=body["event"]["channel"],
                                       thread_ts=body["event"]["event_ts"],
                                       text=last_reply)

    print(window_memory)

# instantiate App with token
if __name__ == "__main__":
    SocketModeHandler(app,
                      os.environ['SLACK_APP_TOKEN']).start()
