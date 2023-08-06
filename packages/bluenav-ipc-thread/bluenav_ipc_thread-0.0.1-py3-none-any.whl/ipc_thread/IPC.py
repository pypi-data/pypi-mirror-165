from typing import Callable, Tuple
from awsiot.eventstreamrpc import LifecycleHandler
import traceback
import awsiot.greengrasscoreipc
import awsiot.greengrasscoreipc.model as model
import awsiot.greengrasscoreipc.client as client
from awsiot.greengrasscoreipc.model import (
    SubscribeToTopicRequest,
    SubscribeToComponentUpdatesRequest,
    DeferComponentUpdateRequest,
    SubscriptionResponseMessage,
    PublishToTopicRequest,
    PublishMessage,
    JsonMessage,
    QOS,
    PublishToIoTCoreRequest,
    SubscribeToIoTCoreRequest,
    ComponentUpdatePolicyEvents
)
import json
from .SingletonMeta import SingletonMeta
import time
import logging



#============================ CLASS TopicStreamHandler ========================================

class TopicStreamHandler(client.SubscribeToTopicStreamHandler):
    __operation : client.SubscribeToTopicOperation

    #------------------------------------------------------------------------

    def __init__(self, topic: str):
        super().__init__()
        self.__topic = topic

    #------------------------------------------------------------------------

    def set_operation(self, operation: client.SubscribeToTopicOperation):
        self.__operation = operation

    #------------------------------------------------------------------------

    def stop(self) -> None:
        self.__operation.close()

    #------------------------------------------------------------------------

    def on_stream_event(self, event: SubscriptionResponseMessage) -> None:
        try:
            message = event.json_message.message
            if self.__handler:
                try:
                    self.__handler(message, self.__topic)
                except:
                    pass
        except:
            traceback.print_exc()

    #------------------------------------------------------------------------

    def on_stream_error(self, error: Exception) -> bool:
        traceback.print_exc()
        return False  # Return True to close stream, False to keep stream open.

    #------------------------------------------------------------------------

    def on_stream_closed(self) -> None:
        pass

    #------------------------------------------------------------------------

    def set_handler(self, callback: Callable[[str, str], None]) -> None:
        self.__handler = callback


#============================ CLASS CoreStreamHandler ========================================


class CoreStreamHandler(client.SubscribeToIoTCoreStreamHandler):
    __operation : client.SubscribeToIoTCoreOperation

    #------------------------------------------------------------------------

    def __init__(self, topic):
        super().__init__()
        self.__handler = None
        self.__topic = topic

    #------------------------------------------------------------------------

    def set_operation(self, operation: client.SubscribeToIoTCoreOperation):
        self.__operation = operation

    #------------------------------------------------------------------------

    def stop(self) -> None:
        self.__operation.close()

    #------------------------------------------------------------------------

    def on_stream_event(self, event: model.IoTCoreMessage) -> None:
        try:
            message = str(event.message.payload, "utf-8")
            topic_name = event.message.topic_name
            if self.__handler:
                self.__handler(message, self.__topic)
        except:
            traceback.print_exc()
    
    #------------------------------------------------------------------------

    def on_stream_error(self, error: Exception) -> bool:
        # Handle error.
        return True # Return True to close stream, False to keep stream open.
    
    #------------------------------------------------------------------------

    def on_stream_closed(self) -> None:
        # Handle close.
        pass

    def set_handler(self, callback: Callable[[str, str], None]) -> None:
        self.__handler = callback

#============================ CLASS LifeCycleHandler ========================================


class LifeCycleHandler(awsiot.eventstreamrpc.LifecycleHandler):
    
    def __init__(self):
        super().__init__()

    #------------------------------------------------------------------------

    def on_connect(self) -> None:
        pass

    #------------------------------------------------------------------------

    def on_disconnect(self, reason) -> None:
        pass

    #------------------------------------------------------------------------

    def on_error(self, error) -> None:
        pass

    #------------------------------------------------------------------------

    def on_ping(self, headers, payload) -> None:

        pass

#===================================================================================

class UpdateStreamHandler(client.SubscribeToComponentUpdatesStreamHandler):
    def __init__(self):
        super().__init__()
        self.__handler = None

    def on_stream_event(self, event: ComponentUpdatePolicyEvents) -> None:
        if self.__handler:
            self.__handler(event)
            
    def set_handler(self, handler):
        self.__handler = handler

#================================ CLASS IPC ========================================

class IPC(metaclass=SingletonMeta):

    __ipc_client = None

    #------------------------------------------------------------------------

    def __init__(self):
        self.connect()
        self.__TIMEOUT = 10

    #------------------------------------------------------------------------

    def connect(self) -> Tuple[bool, LifeCycleHandler]:
        try:
            self.__lifecycle_handler = LifecycleHandler()
            self.__ipc_client = awsiot.greengrasscoreipc.connect()
            return True, self.__lifecycle_handler
        except InterruptedError:
            self.__ipc_client = None
            time.sleep(10)
            return self.connect()
        except Exception as e:
            self.__ipc_client = None
            time.sleep(10)
            return self.connect()

    #------------------------------------------------------------------------

    def subscribe(self, topic:str) -> TopicStreamHandler:
        try:
            request = SubscribeToTopicRequest()
            request.topic = topic

            handler = TopicStreamHandler(topic)
            self.__operation = self.__ipc_client.new_subscribe_to_topic(handler)
            handler.set_operation(self.__operation)
            future = self.__operation.activate(request)
            future.result(self.__TIMEOUT)

            return handler
        except Exception as e:
            logging.error(f"Error subscribing to topic {topic}: {e}")
            time.sleep(10)
            return self.subscribe(topic)

    #------------------------------------------------------------------------

    def publish(self, topic:str, message:str):
        try:
            request = PublishToTopicRequest()
            request.topic = topic

            publish_message = PublishMessage()
            publish_message.json_message = JsonMessage()
            publish_message.json_message.message = message

            request.publish_message = publish_message

            operation = self.__ipc_client.new_publish_to_topic()
            operation.activate(request)

            future = operation.get_response()
            future.result(self.__TIMEOUT)
        except Exception as e:
            logging.error(f"Error publishing to topic {topic}: {e}")
            time.sleep(10)
            self.publish(topic, message)

    #------------------------------------------------------------------------

    def disconnect(self):
        if self.__ipc_client != None:
            self.__ipc_client.close()
            self.__ipc_client = None

    #------------------------------------------------------------------------

    def is_connected(self):
        return self.__ipc_client != None

    #------------------------------------------------------------------------

    def publish_to_core(self, topic:str, message:str):
        if self.__ipc_client != None:
            op = self.__ipc_client.new_publish_to_iot_core()
            op.activate(PublishToIoTCoreRequest(
                topic_name=topic,
                qos=model.QOS.AT_LEAST_ONCE,
                payload=json.dumps(message).encode(),
            ))
            result = op.get_response().result(timeout=5.0)

    #------------------------------------------------------------------------

    def subscribe_to_core(self, topic:str) -> CoreStreamHandler :
        try:
            qos = QOS.AT_LEAST_ONCE
            request = SubscribeToIoTCoreRequest()
            request.topic_name = topic
            request.qos = qos
            handler = CoreStreamHandler(topic)
            operation = self.__ipc_client.new_subscribe_to_iot_core(handler)
            handler.set_operation(operation)
            future = operation.activate(request)
            future.result(self.__TIMEOUT)

            return handler
        except Exception as e:
            logging.error(f"Error subscribing to core: {e}")
            time.sleep(10)
            return self.subscribe_to_core(topic)

    #------------------------------------------------------------------------
    def subscribe_to_component_update(self) -> UpdateStreamHandler:
        try:
            if self.__ipc_client != None:
                handler = UpdateStreamHandler()
                op = self.__ipc_client.new_subscribe_to_component_updates(handler)
                future = op.activate(SubscribeToComponentUpdatesRequest())
                future.result(self.__TIMEOUT)

                return handler
        except Exception as e:
            logging.error(f"Error in subscribe_to_component_update: {e}")
            time.sleep(10)
            return self.subscribe_to_component_update()

    #------------------------------------------------------------------------
    def defer_update(self, deployment_id: str):
        try:
            op = self.__ipc_client.new_defer_component_update()
            request = DeferComponentUpdateRequest()
            request.set_deployment_id(deployment_id)
            request.set_recheck_after_ms(60 * 1000 * 60 * 24 * 8000)

            future = op.activate(request)
            future.result(5)
        except Exception as e:
            return

    #------------------------------------------------------------------------
    def acknowledge_update(self, deployment_id: str):
        try:
            op = self.__ipc_client.new_defer_component_update()
            request = DeferComponentUpdateRequest
            request.set_deployment_id(deployment_id)
            # Specify recheck_after_ms=0 to acknowledge a component update.
            request.set_recheck_after_ms(0)

            future = op.activate(request)
            future.result(5)
        except Exception as e:
            return