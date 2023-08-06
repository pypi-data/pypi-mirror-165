<h1>bluenav-ipc-thread</h1>
<p>Un package python à utiliser dans un environement d'éxécution GreengrassCoreV2</p>
<p>Ce package permet d'encapsuler l'API IPC de Greengrass afin de l'utiliser simplement pour échanger des données 
entre les différents processus ou envoyer des messages MQTT vers AWS IOT Core</p>
<hr/>
<h2>Installation</h2>
<br/>
```bash
pip install git+https://bitbucket.org/bluenav/bluenav-ipc-thread/src/master/
```
<hr/>
<h2>API</h2>
<br/>
<p></p>
```Python
import threading
from ipc_thread import IPCThread
from queue import Queue

sub_queue = Queue()
pub_queue = Queue()
sub_core_queue = Queue()
pub_core_queue = Queue()

# Publier des messages dans un contexte local, dès qu'un message arrive dans la pub_queue il est extrait et envoyé automatiquement
# Le message doit être un dict contenant une clé topic et une clé message
threading.Thread(target=IPCThread.IPCThreadPublish,args=(pub_queue, )).start()
pub_queue.put({"topic": "navigation/CourseOverGround", "message": {"value": 2.765, "unit": "m/s", "PGN": 129026, "SID": 14, "timestamp": 1654847536}})


# Souscrire à un topic dans un contexte local afin de recevoir tous les messages transitants sur ce topic dans la sub_queue
IPCThread.IPCThreadSubscribe(sub_queue, ["navigation/CourseOverGround", ...])

# Pour le même fonctionnement mais dans un contexte distant (IoT Core <-> Machine locale) utiliser: 
# IPCThread.IPCThreadPublishToCore, IPCThread.IPCThreadSubscribeToCore
```