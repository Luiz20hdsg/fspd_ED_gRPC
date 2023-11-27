import sys
import grpc
import pair_pb2
import pair_pb2_grpc

def run(stub):

    try:
        while True:
            command = input()
            if not command:
                break
            command_ = command.split(',')
            if command_[0] == 'I':
                #response = stub.Insert(pair_pb2.Request(key=int(command_[1])), value=command_[2])
                response = stub.Insert(pair_pb2.Request(key=int(command_[1]), value=command_[2]))

                print(response.result)
            elif command_[0] == 'C':
                response = stub.Consult(pair_pb2.ConsultRequest(key=int(command_[1])))
                if response.service_identifier:
                    response_retrieve = stub.Retrieve(pair_pb2.Request(key=int(command_[1])))
                    print(response_retrieve.value)
                else:
                    empty_string = ''
                    print(empty_string)
            elif command_[0] == 'A':
                response = stub.Activate(pair_pb2.ActivateRequest(service_identifier=command_[1]))
                print(response.result)
            elif command_[0] == 'T':
                response = stub.Terminate(pair_pb2.Empty())
                print(response.result)
                break

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
    stub = pair_pb2_grpc.PairStub(channel)

    run(stub)

    channel.close()


