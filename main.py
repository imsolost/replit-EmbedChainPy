import os

import chainlit as cl
from embedchain import Pipeline as App
from replit import db

fileList = os.listdir("docs")

@cl.on_chat_start
async def on_chat_start():
    app = App.from_config(config={
        'app': {
            'config': {
                'name': 'chainlit-app'
            }
        },
        'llm': {
            'config': {
                'stream': True,
            }
        }
    })
    # import your data here
    for file in fileList:
      keys = db.keys()
      if file not in keys:
        print("Loading " + file)
        app.add(f"docs/{file}")
        db[file] = None
      else:
        print("Skipping " + file)
    app.collect_metrics = False
    cl.user_session.set("app", app)

@cl.on_message
async def on_message(message: cl.Message):
    app = cl.user_session.get("app")
    msg = cl.Message(content="")
    for chunk in await cl.make_async(app.chat)(message.content):
        await msg.stream_token(chunk)

    await msg.send()