import grpc
import sys
from concurrent import futures
import time
import pair_pb2
import pair_pb2_grpc
import centralizer_pb2_grpc
import socket
import threading



class PairServicer(pair_pb2_grpc.PairServicer):
    def __init__(self, activate, stop_event, adrress):
        self.key_value_store = {}
        self.activate = activate
        self.stop_event = stop_event
        self.adrress = adrress

    def Insert(self, request, context):
        key = request.key
        value = request.value

        if key in self.key_value_store:
            return pair_pb2.Response(result=-1)
        else:
            self.key_value_store[key] = value
            return pair_pb2.Response(result=0)
    
    def Consult(self, request, context):
        key = request.key
        service_identifier = self.key_value_store.get(key, "")
        return pair_pb2.ConsultResponse(service_identifier=service_identifier)

    def Activate(self, request, context):
        if self.activate:
            channel = grpc.insecure_channel(request.service)
            stub = pair_pb2_grpc.Part2ServicesStub(channel)
            #terminar na parte 2
            "..."
        else: 
            return pair_pb2.ActivateResponse(result=0)


    def Terminate(self, request, context):
        self.stop_event.set()

        return pair_pb2.TerminateResponse(result=0)

def serve():
    port = sys.argv[1]
    address = '%s:%s' % (socket.INADDR_ANY, port)
    
    activate = False

    if len(sys.argv) > 2:
        activate = True

    stop_event = threading.Event()  
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))    

    pair_pb2_grpc.add_PairServicer_to_server(PairServicer(activate, stop_event, '%s:%s' % (socket.getfqdn(), port)), server)
    
    # Start server
    server.add_insecure_port(address)
    server.start()
    stop_event.wait()   
    server.stop(2)      
    
if __name__ == '__main__':
    serve()
