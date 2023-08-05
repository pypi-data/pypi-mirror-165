import requests
import multibase
import json
import io
import threading
import time
import itertools

_SUBS = {}

def parse_endpoint(endpoint):

    ip = endpoint.split("/dns/")[1].split("/")[0]
    port = int(endpoint.split("/tcp/")[1].split("/")[0])
    return ip,port

def encode_topic(topic):
    return multibase.encode("base64url",topic).decode("utf8")

def decode(data):
    return multibase.decode(data)


def pub(endpoint,topic,data):
    ip,port = parse_endpoint(endpoint)

    file = io.BytesIO(data if type(data) == bytes else data.encode("utf8"))

    files = {'file': file}

    requests.post("http://"+ip+":"+str(port)+"/api/v0/pubsub/pub?arg="+encode_topic(topic),files=files)

def unsub(topic):
    global _SUBS
    if topic in _SUBS.keys():
        for i in range(len(_SUBS[topic][0])-1,-1,-1):
            if not _SUBS[topic][0][i] is None:
                _SUBS[topic][i][0].close()
                _SUBS[topic][i][0] = None
        _SUBS[topic][1] = False

def sub(endpoint,topic,callback):
    global _SUBS

    if not topic in _SUBS.keys():
        _SUBS[topic] = [[],True]
    _SUBS[topic][1] = True
    th = threading.Thread(target=_sub,args=(endpoint,topic,callback,))
    th.daemon = True
    th.start()

def _sub(endpoint,topic,callback):
    global _SUBS
    
    ip,port = parse_endpoint(endpoint)

    seq_offset = -1
    with requests.post("http://"+ip+":"+str(port)+"/api/v0/pubsub/sub?arg="+encode_topic(topic), stream=True) as r:
        _SUBS[topic][0].append(r)
        while True:
            try:
                for m in r.iter_lines():
                    j = json.loads(m.decode("utf8"))
                    j["data"] = decode(j["data"])
                    j["seqno"] = int.from_bytes(decode(j["seqno"]),"big")

                    if seq_offset == -1:
                        seq_offset = j["seqno"]
                    j["seqno"] = j["seqno"] - seq_offset

                    for i in range(len(j["topicIDs"])):
                        j["topicIDs"][i] = decode(j["topicIDs"][i])


                    callback(data=j["data"],seqno=j["seqno"],topic_ids=j["topicIDs"],cid=j["from"])
            except:
                if not topic in _SUBS.keys() or _SUBS[topic][1] == False:
                    print ("Unsub:",topic)
                    return