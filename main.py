import requests; import threading;
import websocket; import json; # Get API keys here: https://console.groq.com/keys
import time; import random;
starting_prompt:str = """
These are the previous messages so you can have context, if it's '(No messages yet)', ignore, the messages with '(You)' as sender, were sent by you previously:
Note: if a message if empty, it was media content that you cannot visualize
    
%s
Now provide a reply to this message, send only your reply as a response:
%s: %s

You will have the personality of a [Insert your personality prompt here], plus don't sound self repeating
""";
with open("config.json") as f: json_obj = json.load(f);
token = json_obj.get("token"); API_KEY = json_obj.get("api"); prefix = json_obj.get("prefix"); t_chan_id_ = json_obj.get("chan_id");
typing = json_obj.get("typing"); waiting_time = json_obj.get("waiting_time");
limit:int = int(json_obj.get("limit")); # This is the memory, the amount of messages it can recall
reading_speed:int = int(json_obj.get("reading_speed"));
def sleep_timer() -> None:
    global memory_channels
    while True:
        if memory_channels != {}:
            time.sleep(1);
            for _ in memory_channels:
                if memory_channels[_]['sleep_time'] > 0: memory_channels[_]['sleep_time']-=1;
def send_json_request(ws, request): ws.send(json.dumps(request));
def receive_json_response(ws):
    response = ws.recv();
    if response: return json.loads(response);
def heartbeat(interval, ws):
    while True:
        time.sleep(interval);
        heartbeatJSON = {
            "op": 1,
            "d": "null"
        };
        send_json_request(ws, heartbeatJSON);
def messagelogger():
    global memory_channels
    ws = websocket.WebSocket();
    ws.connect("wss://gateway.discord.gg/?v=6&encording=json");
    event = receive_json_response(ws);
    heartbeat_interval = event['d']['heartbeat_interval']/1000;
    threading._start_new_thread(heartbeat, (heartbeat_interval, ws));
    payload = {
        "op": 2,
        "d": {
            "token": token,
            "properties": {
                "$os": "windows",
                "$browser": "chrome",
                "$device": "pc"
            }
        }
    };
    send_json_request(ws, payload); print("Ready.");
    memory_channels = {}; #{"": {
    #    "sleep_time": reading_speed,
    #    "channels": [],
    #    "last_sender_id": "",
    #    "message_id": "",
    #    "has_replied": False
    #}};
    threading.Thread(target=sleep_timer).start();
    sender_user_id = str(__import__("base64").b64decode(token.split(".")[0]+"==").decode("utf-8"));
    while True:
        event = receive_json_response(ws);
        try:
            chan_id:str = str(event['d']['channel_id']);
            if t_chan_id_ == "" or chan_id == t_chan_id_:
                if not chan_id in memory_channels:
                    memory_channels.update({chan_id:{"sleep_time": reading_speed, "channels": [], "last_sender_id": str(event['d']['author']['id']), "message_id": str(event['d']['id']), "has_replied": False}});
                memory_channels[chan_id]['last_sender_id'] = str(event['d']['author']['id']);
                memory_channels[chan_id]['message_id'] = str(event['d']['id']);
                memory_channels[chan_id]['sleep_time'] = reading_speed;
                memory_channels[chan_id]['has_replied'] = False;
                username = str(event['d']['author']['username']);
                _input = str(event['d']['content']);
                memory_channels[chan_id]['channels'].append("%s: %s" % (username if not sender_user_id==memory_channels[chan_id]['last_sender_id'] else "(You)", _input if not _input.startswith(prefix) else _input[len(prefix):]));
                if len(memory_channels[chan_id]['channels'])>limit: memory_channels[chan_id]['channels'] = [];
                print(memory_channels)
        except KeyError: pass;
        except Exception as y:
            print(y);
        if not memory_channels == {}:
            for channel_queue in memory_channels:
                if memory_channels[channel_queue]['sleep_time'] == 0 or waiting_time == "" and memory_channels[channel_queue]['has_replied'] == False:
                    if (_input.startswith(prefix) or prefix=="") and not memory_channels[channel_queue]['last_sender_id']==sender_user_id:
                        if not prefix=="": _input = _input[len(prefix):];
                        final_prompt:str = starting_prompt % ("".join([i+"\n" for i in memory_channels[channel_queue]['channels']] if not memory_channels[channel_queue]['channels']==[] else "(No messages yet)"), username, _input);
                        #print(final_prompt, end="\n===========================\n");
                        typing_request = requests.post(f"https://discord.com/api/v9/channels/{channel_queue}/typing", headers={
                            "Authorization": token
                        });
                        AI_response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers={
                            "Content-Type": "application/json",
                            "Authorization": "Bearer "+API_KEY
                        }, json={
                            "model": "llama-3.3-70b-versatile",
                            "messages": [
                                {
                                    "role": "user",
                                    "content": final_prompt
                                },
                            ],
                        });
                        AI_reply:str = AI_response.json()['choices'][0]['message']['content'];
                        if not typing == "":
                            time.sleep(random.randint(2, 4));
                        message_request = requests.post(f"https://discord.com/api/v9/channels/{channel_queue}/messages", headers={
                            "Authorization": token
                        }, json={
                            "content": AI_reply,
                            "message_reference": {
                                "channel_id": channel_queue,
                                "message_id": memory_channels[channel_queue]['message_id']
                            }
                        });
                        if message_request.ok:
                            memory_channels[channel_queue]['has_replied'] == True;
threading.Thread(target=messagelogger).start();
