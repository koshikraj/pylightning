import grpc
import os

from lightning_libs import rpc_pb2 as ln, rpc_pb2_grpc as lnrpc

def create_stub():
    os.environ["GRPC_SSL_CIPHER_SUITES"] = "HIGH+ECDSA"
    cert = open('/home/koshik/.lnd/tls.cert').read()
    creds = grpc.ssl_channel_credentials(cert)
    channel = grpc.secure_channel('localhost:10002', creds)
    stub = lnrpc.LightningStub(channel)
    return stub