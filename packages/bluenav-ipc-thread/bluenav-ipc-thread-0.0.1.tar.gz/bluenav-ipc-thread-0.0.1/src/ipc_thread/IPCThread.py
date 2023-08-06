import queue
import json
from awsiot.greengrasscoreipc.model import UnauthorizedError, ComponentUpdatePolicyEvents
from .IPC import IPC
import time as t
import logging
import traceback
import os

# Subscribe to IPC topics and put message received in the Queue
class IPCThreadSubscribe():
    def __init__(self, sub_queue: queue.Queue, topics: list = []) -> None:
        self.__IPC = IPC()
        self.sub_queue = sub_queue

        for topic in topics:
            try:
                self.__IPC.subscribe(topic).set_handler(self.provider)
            except UnauthorizedError:
                logging.info(f'Unauthorized to subscribe to topic {topic}')

    def provider(self, message: str, topic: str):
        self.sub_queue.put({"message": message, "topic": topic})
    
    def add_subscription(self, topic):
        try:
            self.__IPC.subscribe(topic).set_handler(self.provider)
        except UnauthorizedError:
            logging.info(f'Unauthorized to subscribe to topic {topic}')

# Check queue to see if there is IPC message to send (dict with key topic and key message)
class IPCThreadPublish():
    def __init__(self, pub_queue: queue.Queue) -> None:
        self.__IPC = IPC()
        self.pub_queue = pub_queue
        self.consumer()
    
    def consumer(self):
        while True:
            data = self.pub_queue.get()
            if data:
                try:
                    self.__IPC.publish(data["topic"], data["message"])
                except:
                    pass


# Check queue to see if there is MQTT messages to send to IoT Core
class IPCThreadPublishToCore():
    def __init__(self, pub_core_queue: queue.Queue) -> None:
        self.__IPC = IPC()
        self.pub_core_queue = pub_core_queue
        self.consumer()

    def consumer(self):
        while True:
            data = self.pub_core_queue.get()
            if data:
                try:
                    self.__IPC.publish_to_core(data["topic"], data["message"])
                except Exception:
                    t.sleep(0.5)


# Subscribe to MQTT IoT Core topic and put message received in the Queue
class IPCThreadSubscribeToCore():
    def __init__(self, sub_queue: queue.Queue, topics: list) -> None:
        self.__IPC = IPC()
        self.sub_queue = sub_queue

        for topic in topics:
            try:
                self.__IPC.subscribe_to_core(topic).set_handler(self.provider)
            except UnauthorizedError:
                logging.info(f'Unauthorized to subscribe to topic {topic}')

    def provider(self, message: str, topic: str):
        try:
            msg = json.loads(message)
            self.sub_queue.put({"message": msg, "topic": topic})
        except:
            logging.info(f'Unable to parse data')


class SubscribeComponentUpdate():
    def __init__(self, updated_queue: queue.Queue) -> None:
        self.__IPC = IPC()
        self.updated_queue = updated_queue

        try:
            self.__IPC.subscribe_to_component_update().set_handler(self.on_component_update)
        except:
            logging.info("Unable to subscribe to component update")

    def on_component_update(self, event: ComponentUpdatePolicyEvents) -> None:
        try:
            if event.pre_update_event is not None:
                if os.path.exists("/data/conf/update/AcceptedFlag"):
                    self.__IPC.acknowledge_update(event.pre_update_event.deployment_id)
                    logging.info(f'Acknowledged update for deployment {event.pre_update_event.deployment_id}')
                else:
                    self.__IPC.defer_update(event.pre_update_event.deployment_id)
                    logging.info(f'Deferred update for deployment {event.pre_update_event.deployment_id}')
                    # Put the message in the queue to inform the system an update is needed
                    self.updated_queue.put({"request": event})
                    return

            elif event.post_update_event is not None:
                try:
                    os.remove("/data/conf/update/AcceptedFlag")
                except:
                    pass

                try:
                    os.remove("/data/conf/update/UpdateFlag.txt")
                except:
                    pass
                
                logging.info(f"Applied update for deployment {event.post_update_event.deployment_id}")
                self.updated_queue.put({"applied": True})
        except:
            traceback.print_exc()