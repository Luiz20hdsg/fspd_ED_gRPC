import grpc
from concurrent import futures
import time
import centralizer_pb2
import centralizer_pb2_grpc

class CentralizerServicer(centralizer_pb2_grpc.CentralizerServicer):
    def __init__(self):
        self.key_directory = {}

    def Register(self, request, context):
        service_identifier = request.service_identifier
        keys = request.keys

        # Tratamento de colisões
        for key in keys:
            self.key_directory[key] = service_identifier

        return centralizer_pb2.Response(result=len(keys))

    def Map(self, request, context):
        key = request.key
        service_identifier = self.key_directory.get(key, "")
        return centralizer_pb2.MapResponse(service_identifier=service_identifier)

    def Terminate(self, request, context):
        return centralizer_pb2.Response(result=len(self.key_directory))

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    centralizer_pb2_grpc.add_CentralizerServicer_to_server(CentralizerServicer(), server)
    "..."

if __name__ == '__main__':
    serve()
