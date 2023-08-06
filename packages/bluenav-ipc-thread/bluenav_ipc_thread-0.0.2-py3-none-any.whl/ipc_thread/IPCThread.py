import queue
import json
from awsiot.greengrasscoreipc.model import UnauthorizedError, ComponentUpdatePolicyEvents
from .IPC import IPC
import time as t
import logging
import traceback
import os

# Reuse one IPC client
IPC_client = IPC()

"""
The IPC client V1 can't send new requests or process new event messages while the thread
is blocked, this package is a wrapper to help the usage of Thread around IPC client v1
"""

class IPCThreadSubscribe():
    """
    Handle local IPC message reception through queue (IPCClientV1)
    
        Args:
            sub_queue (Queue): The queue on which IPC local messages will arrive
            topics (list[str]): List of string containing the MQTT topics to listen for
    """
    def __init__(self, sub_queue: queue.Queue, topics: list[str] = []) -> None:
        self.sub_queue = sub_queue

        for topic in topics:
            try:
                IPC_client.subscribe(topic).set_handler(self.provider)
            except UnauthorizedError:
                logging.info(f'Unauthorized to subscribe to topic {topic}')

    def provider(self, message: str, topic: str) -> None:
        """
        Callback function on message event
        """
        self.sub_queue.put({"message": message, "topic": topic})
    
    def add_subscription(self, topic: str) -> bool:
        """
        Add a new MQTT topic to listen for
        """
        try:
            IPC_client.subscribe(topic).set_handler(self.provider)
            return True
        except UnauthorizedError:
            logging.info(f'Unauthorized to subscribe to topic {topic}')
            return False


class IPCThreadPublish():
    """
    Handle local IPC message publication

        Args:
            pub_queue (Queue): Listen for new MQTT messages to send. 
            Any message on this Queue should be a dict with a key topic and message
    """
    def __init__(self, pub_queue: queue.Queue) -> None:
        self.pub_queue = pub_queue
        self.consumer()
    
    def consumer(self):
        while True:
            data = self.pub_queue.get()
            if data:
                try:
                    IPC_client.publish(data["topic"], data["message"])
                except:
                    pass


class IPCThreadPublishToCore():
    """
    Publish MQTT messages on IoT Core

        Args:
            pub_queue (Queue): Listen for new MQTT messages to send to IoT Core.
            Any message on this Queue should be a dict with a key topic and message
    """
    def __init__(self, pub_core_queue: queue.Queue) -> None:
        self.pub_core_queue = pub_core_queue
        self.consumer()

    def consumer(self):
        while True:
            data = self.pub_core_queue.get()
            if data:
                try:
                    IPC_client.publish_to_core(data["topic"], data["message"])
                except Exception:
                    t.sleep(0.5)


class IPCThreadSubscribeToCore():
    """
    Subscribe to MQTT messages from IoT Core

        Args:
            sub_queue (Queue): The queue on which MQTT messages from IoT Core will arrive
    """
    def __init__(self, sub_queue: queue.Queue, topics: list) -> None:
        self.sub_queue = sub_queue

        for topic in topics:
            try:
                IPC_client.subscribe_to_core(topic).set_handler(self.provider)
            except UnauthorizedError:
                logging.info(f'Unauthorized to subscribe to topic {topic}')

    def provider(self, message: str, topic: str):
        """
        Callback function on message event
        """
        try:
            msg = json.loads(message)
            self.sub_queue.put({"message": msg, "topic": topic})
        except:
            logging.info(f'Unable to parse data')


class SubscribeComponentUpdate():
    """
    Handle deployment notification

        Args:
            updated_queue (Queue): This queue is used to inform a new update and success deployment
            flag_path (str): Path to check the flag to accept or delay the update
    """
    def __init__(self, updated_queue: queue.Queue, flag_path: str) -> None:
        self.updated_queue = updated_queue
        self.flag_path = flag_path

        try:
            IPC_client.subscribe_to_component_update().set_handler(self.on_component_update)
        except:
            logging.info("Unable to subscribe to component update")

    def on_component_update(self, event: ComponentUpdatePolicyEvents) -> None:
        try:
            if event.pre_update_event is not None:
                if os.path.exists(f"{self.flag_path}/AcceptedFlag"):
                    IPC_client.acknowledge_update(event.pre_update_event.deployment_id)
                    logging.info(f'Acknowledged update for deployment {event.pre_update_event.deployment_id}')
                else:
                    IPC_client.defer_update(event.pre_update_event.deployment_id)
                    logging.info(f'Deferred update for deployment {event.pre_update_event.deployment_id}')
                    # Put the message in the queue to inform the system an update is needed
                    self.updated_queue.put({"request": event})
                    return

            elif event.post_update_event is not None:
                try:
                    os.remove(f"{self.flag_path}/AcceptedFlag")
                except:
                    pass

                try:
                    os.remove(f"{self.flag_path}/UpdateFlag.txt")
                except:
                    pass
                
                logging.info(f"Applied update for deployment {event.post_update_event.deployment_id}")
                self.updated_queue.put({"applied": True})
        except:
            traceback.print_exc()