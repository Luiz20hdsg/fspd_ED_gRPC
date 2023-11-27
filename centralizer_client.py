
import sys
import grpc
import centralizer_pb2
import centralizer_pb2_grpc
import pair_pb2
import pair_pb2_grpc


def run(stub):
    try:
        while True:
            command = input()
            if not command:
                break
            command_ = command.split(',')
            if command_[0] == 'C':
                    response = stub.Map(centralizer_pb2.MapRequest(key=int(command_[1])))
                    if response.service:
                        print(response.service,':', end='', sep='')
                        channel = grpc.insecure_channel(response.service)
                        sub_stub = pair_pb2_grpc.PairServicer(channel)
                        pair_pb2.ConsultRequest
                        response = sub_stub.Consult(pair_pb2.ConsultRequest(key=int(command_[1])))
                        print(response.service)
                        channel.close()
                    else:
                        print("")
            else:
                print("Invalid command")

    except KeyboardInterrupt:
        pass


if __name__ == '__main__':

    if(len(sys.argv) != 2):
        print("Usage: python3 client.py <address:port>")
        sys.exit(1)
    
    port = sys.argv[1]
    # Connet to a server
    channel = grpc.insecure_channel(port)
    stub = centralizer_pb2_grpc.PairStub(channel)

    run(stub)

    channel.close()