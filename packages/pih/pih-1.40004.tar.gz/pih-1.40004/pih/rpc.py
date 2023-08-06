from dataclasses import dataclass
from typing import Any, Callable, Tuple
import grpc

from concurrent import futures

import pih.rpcCommandCall_pb2_grpc as pb2_grpc
import pih.rpcCommandCall_pb2 as pb2
from pih.tools import DataTools, ParameterList


@dataclass
class rpcCommand:
    host: str
    port: int
    name: str


class RPC:

    class UnaryService(pb2_grpc.UnaryServicer):

        def __init__(self, handler: Callable, *args, **kwargs):
            self.handler = handler

        def internal_handler(self, command_name: str, parameters: str, context) -> dict:
            print(f"RPC call: {command_name}")
            if command_name == "ping":
                return "pong"
            return self.handler(command_name, ParameterList(parameters), context)

        def rpcCallCommand(self, command, context):
            parameters = command.parameters
            if parameters and parameters != "":
                parameters = DataTools.rpc_unrepresent(parameters)
            return pb2.rpcCommandResult(data=DataTools.represent(self.internal_handler(command.name, parameters, context)))

    class Server:

        @staticmethod
        def serve(server_host_name: str, server_name: str, port: int, handler: Callable, libs: Tuple = None) -> None:
            from pih.pih import PIH, PR
            PR.init()
            PIH.VISUAL.rpc_server_header(server_host_name, server_name)
            server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
            pb2_grpc.add_UnaryServicer_to_server(
                RPC.UnaryService(handler), server)
            server.add_insecure_port(f"{server_host_name}:{port}")
            server.start()
            server.wait_for_termination()

    class rpcCommandClient():

        def __init__(self, host: str, port: int):
            self.host = host
            self.server_port = port
            self.channel = grpc.insecure_channel(
                f"{self.host}:{self.server_port}")
            self.stub = pb2_grpc.UnaryStub(self.channel)

        def call_command(self, name: str, parameters: str = None):
            return self.stub.rpcCallCommand(pb2.rpcCommand(name=name, parameters=parameters))

    @staticmethod
    def call(command: rpcCommand, parameters: Any = None) -> str:
        return RPC.rpcCommandClient(command.host, command.port).call_command(command.name, DataTools.rpc_represent(parameters)).data
