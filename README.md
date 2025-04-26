# AI-Chat-Bot-on-discord-account
This code will run an AI chat bot to reply for you on your discord account, it fetches the responses via websocket
# Config.json file
```json
{
    "token": "",
    "api": "",
    "prefix": ""
    "chan_id": "",
    "typing": "yes"
}
```
In the `token` option you'll put your discord token, in `api` there'll be your https://console.groq.com/keys API key, lastly if `prefix` is empty it will reply to every messages, but if add a prefix it reply only with the messages starting with the prefix defined

Additionally, you can restrict the channel the AI texts in by inserting the channel ID in `chan_id`, for DMs you have to find the DM ID, if you don't want the AI to simulate user typing leave `typing` blank
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
