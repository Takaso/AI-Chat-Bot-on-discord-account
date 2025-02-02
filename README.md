# AI-Chat-Bot-on-discord-account
This code will run an AI chat bot to reply for you on your discord account, it fetches the responses via websocket
# Config.json file
```json
{
    "token": "",
    "api": "",
    "prefix": ""
}
```
In the `token` option you'll put your discord token, in `api` there'll be your https://console.groq.com/keys API key, lastly if `prefix` is empty it will reply to every messages, but if add a prefix it reply only with the messages starting with the prefix defined
