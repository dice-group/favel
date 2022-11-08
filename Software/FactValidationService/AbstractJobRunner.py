import threading
import socket
import logging
from datastructures.Assertion import Assertion
from FactValidationService.Message import Message

class AbstractJobRunner(threading.Thread):
    """
    Abstract class that implements basic functionality.
    Able to connect to a fact validation approach via TCP, send assertions in
    turtle format and receive their score.
    """

    def __init__(self, approach:str, port:int):
        threading.Thread.__init__(self)
        self.approach = approach
        self.port = port
        self.server = None
    
    def _validateAssertion(self, assertion:Assertion):
        """
        Validate a single assertion.
        """
            
        # Send assertion
        self._send(Message(type="test", subject=assertion.subject, predicate=assertion.predicate, object=assertion.object))
        
        # Receive score
        return Message(text=self._receive())
    
    def _trainAssertion(self, assertion:Assertion):
        """
        Send the assertion to a supervised approach as training data.
        """
        self._send(Message(
            type="train", subject=assertion.subject, predicate=assertion.predicate, object=assertion.object, score=assertion.expectedScore))
        return Message(text=self._receive())

    def _trainingStart(self):
        self._send(Message(type="call", content="training_start"))
        return Message(text=self._receive())
    
    def _trainingComplete(self):
        self._send(Message(type="call", content="training_complete"))
        return Message(text=self._receive())
        
    def _type(self):
        self._send(Message(type="call", content="type"))
        return Message(text=self._receive())
    
    def _connect(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.connect(("127.0.0.1", self.port))
        except ConnectionRefusedError as ex:
            logging.warning("Cannot connect to approach '{}'".format(self.approach))
            raise(ex)
        
    def _send(self, message:Message):
        if self.server == None:
            self._connect()
        self.server.send(message.serialize().encode())
        
    def _receive(self):
        return self.server.recv(1024).decode()
