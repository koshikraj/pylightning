import codecs
import grpc
import os

from lightning_libs import rpc_pb2 as ln, rpc_pb2_grpc as lnrpc


class gRPCDriver:

    def __init__(self):
        self.stub = self.get_stub()

    def get_stub(self):

        def metadata_callback(context, callback):

            with open('resources/admin.macaroon', 'rb') as f:
                macaroon_bytes = f.read()
                macaroon = codecs.encode(macaroon_bytes, 'hex')

            callback([('macaroon', macaroon)], None)

        os.environ["GRPC_SSL_CIPHER_SUITES"] = "HIGH+ECDSA"
        cert = open('resources/tls.cert').read()

        # build ssl credentials using the cert the same as before
        cert_creds = grpc.ssl_channel_credentials(cert)

        # now build meta data credentials
        auth_creds = grpc.metadata_call_credentials(metadata_callback)

        # combine the cert credentials and the macaroon auth credentials
        # such that every call is properly encrypted and authenticated
        combined_creds = grpc.composite_channel_credentials(cert_creds, auth_creds)

        # finally pass in the combined credentials when creating a channel
        channel = grpc.secure_channel('projects.koshikraj.com:10009', combined_creds)
        stub = lnrpc.LightningStub(channel)
        return stub

    # create invoice for amount and return payment_request
    def generate_invoice(self, amt, memo=None):
        request = ln.Invoice(value=amt, memo=memo)
        response = self.stub.AddInvoice(request)
        return response

    def is_received(self, pay_req):
        # first decode pay_req to get pay_hash
        request = ln.PayReqString(pay_req = pay_req)
        response = self.stub.DecodePayReq(request)
        pay_hash = response.payment_hash

        # check if settled
        request = ln.PaymentHash(r_hash_str = pay_hash)
        response = self.stub.LookupInvoice(request)
        return response.settled

    # send payment by request
    def send_payment(self, pay_req):
        request = ln.SendRequest(payment_request = pay_req)
        response = self.stub.SendPaymentSync(request)
        return True