import json
import falcon

import codecs
import os

from lightning_libs.grpc import gRPCDriver, ln


grpc_driver = gRPCDriver()

class VerifyMessage:

    def on_get(self, req, res):

        try:


            verifymessage_resp = grpc_driver.stub.VerifyMessage(ln.VerifyMessageRequest(msg=b"1234", signature="rdmz61jkcbr5itef3rojay38ssfu8a8zxsp6fis7xfsi3g6jt9nf1ik6xxbopgezeppuo5rbgabprzs78kw6yrpxot55qyrnc95qtz86"))

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

            add_invoice_resp = grpc_driver.generate_invoice(amt=10000, memo="Test Memo")
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

class SendPayment:

    def on_get(self, req, res):

        try:
            payment_request=req.params['pay_req']
            send_payment_resp = grpc_driver.send_payment(pay_req=payment_request)


            res.status = falcon.HTTP_200
            res.body = json.dumps({'status': send_payment_resp,
                                   'data': [],
                                   'message': 'success'
                                   })
        except Exception as e:
            res.status = falcon.HTTP_400
            res.body = json.dumps({'status': False,
                                   'data': [],
                                   'message': str(e)
                                   })
