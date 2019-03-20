import json
import falcon

from lightning_libs.grpc import create_stub, ln



class VerifyMessage:

    def on_get(self, req, res):

        try:

            stub = create_stub()
            verifymessage_resp = stub.VerifyMessage(ln.VerifyMessageRequest(msg=b"1234", signature="ryqpeqhocrcoqks7inasb8it79ri8idtm5a99x95irg7gjndnc7fwxdd87afof16ep4aqa51qqptw38967jpgfq91e15eutmbaugazyt"))

            res.status = falcon.HTTP_200
            res.body = json.dumps({'status': True,
                                   'data': {'verifiied': verifymessage_resp.valid },
                                   'message': 'success'
                                   })
        except Exception as e:
            res.status = falcon.HTTP_400
            res.body = json.dumps({'status': False,
                                   'data': [],
                                   'message': str(e)
                                   })


class GenerateInvoice:

    def on_get(self, req, res):

        try:

            stub = create_stub()

            add_invoice_resp = stub.AddInvoice(ln.Invoice(value=1000, memo="Test Memo"))
            payment_request = add_invoice_resp.payment_request

            res.status = falcon.HTTP_200
            res.body = json.dumps({'status': True,
                                   'data': {'invoice': payment_request},
                                   'message': 'success'
                                   })
        except Exception as e:
            res.status = falcon.HTTP_400
            res.body = json.dumps({'status': False,
                                   'data': [],
                                   'message': str(e)
                                   })
