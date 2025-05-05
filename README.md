# AI-Chat-Bot-on-discord-account
This code will run an AI chat bot to reply for you on your discord account, it fetches the responses via websocket
# Config.json file
```json
{
    "token": "",
    "api": "",
    "prefix": ""
    "chan_id": "",
    "typing": ""
    "waiting_time": "yes",
    "limit": 70,
    "reading_speed": 3
}
```
- In the `token` option you'll put your discord token, you can fetch with the dev tools
- in `api` there'll be your https://console.groq.com/keys API key`
- If `prefix` is empty it will reply to every messages, but if add a prefix it reply only with the messages starting with the prefix defined, example: "`!hello`" with `!` as prefix
- You can restrict the channel the AI texts in by inserting the channel ID in `chan_id`, for DMs you have to find the DM ID
- If you don't want the AI to wait a few seconds to simulate user typing leave `typing` empty, but it's not really necessary
- `waiting_time` will simulate how the AI waits like humans a few seconds before replying, this option also allows the AI not to flood the chat with a reply every single message if people talk with multiple messages at once
- `limit` is the number of messages the AI will recall, after the limit is reached the memory is emptied
- `reading_speed` is the amount of seconds the AI waits before replying, set to a low number if you're in a chat with a lot of people, if `waiting_time` is disabled then this option will not be used
# Other settings
Inside the code you can specify your prompt here:
```py
starting_prompt:str = """
These are the previous messages so you can have context, if it's '(No messages yet)', ignore, the messages with '(You)' as sender, were sent by you previously:
Note: if a message if empty, it was media content that you cannot visualize
    
%s
Now provide a reply to this message, send only your reply as a response:
%s: %s

You will have the personality of [Here you can describe anything you wish for] plus don't sound self repeating
""";
```
Make sure to change only the text inside of the brackets, or else the code might not work properly
