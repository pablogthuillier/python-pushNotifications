"""

Developed by Pablo G. Thuillier
@pablogthuillier
https://github.com/pgonzalezt


For using this library you can write lines like these:

priv_filepath = "certifications/MyAppCert.pem"
cert_filepath = "certifications/MyAppKey.pem"
ios = IOSPushNotifications(privatekey_filepath=priv_filepath,certificate_filepath=cert_filepath)
ios.send_push_notification(message="This is a test push",token_device="abf02b")

Optional arguments in iOS push might be:
- badge (indicates the number badge in the app icon)
- sound (indicates the sound it must be sounded)


"""

from OpenSSL import SSL
from gcm import GCM
from socket import socket
import os
import json
import struct, binascii

class AndroidPushNotifications:
    """
    Constructor with one argument.
    api_key: the API KEY string proporcionated by Google
    """
    def __init__(self,api_key=None):
        self.__api_key = api_key

    def send_push_notification(self,**kwargs):
        try:
            if not len(kwargs):
                raise Exception("Message and token must be given")
            if "message" not in kwargs:
                raise Exception("Message not found")
            if "token_device" not in kwargs:
                raise Exception("Token device not found")
            if not self.__api_key:
                raise Exception("Api key not found")

            data = {'message': kwargs["message"].encode('utf-8')}
            if len(kwargs)>2:
                for key in kwargs:
                    if key!="message" and key!="token_device":
                        data[key] = kwargs[key]

            gcm = GCM(self.__api_key)
            gcm.plaintext_request(registration_id=kwargs["token_device"], data=data)
            return {'status':'success','response':'android_push_sent'}
        
        except Exception as e:
            return {'status':'failed','response':'push_notification_android_error','description':e.args[0]}


class IOSPushNotifications:
    """
    Constructor with two arguments.
    certificate_filepath: the certificate filepath (i.e. "certificates/MyAppCert.pem")
    privatekey_filepath: the private key filepath (i.e. "certificates/MyAppKey.pem")
    """
    def __init__(self,privatekey_filepath=None,certificate_filepath=None):
        self.__private_key = ""
        self.__public_cert = ""

        if privatekey_filepath and certificate_filepath:
            privatekey_file = os.path.join(os.path.dirname(__file__), privatekey_filepath)
            certificate_file = os.path.join(os.path.dirname(__file__), certificate_filepath)

            if os.path.isfile(privatekey_file) and os.path.isfile(certificate_file):
                self.__privatekey = privatekey_file
                self.__certificate = certificate_file


    def send_push_notification(self,**kwargs):
        try:
            if not len(kwargs):
                raise Exception("Message and token must be given")
            if "message" not in kwargs:
                raise Exception("Message not found")
            if "token_device" not in kwargs:
                raise Exception("Token device not found")

            if not self.__privatekey:
                raise Exception("Private key file not found")
            if not self.__certificate:
                raise Exception("Certificate file not found")

            apnHost = "gateway.push.apple.com"
            ctx=SSL.Context(SSL.SSLv3_METHOD)
            ctx.use_certificate_file(self.__certificate)
            ctx.use_privatekey_file(self.__privatekey)

            payload = {}
            aps = {}
            aps["alert"] = kwargs["message"].encode('utf-8')
            if len(kwargs)>2:
                for key in kwargs:
                    if key!="message" and key!="token_device":
                        aps[key] = kwargs[key]

            payload["aps"] = aps

            token = binascii.unhexlify(kwargs["token"])
            payloadstr = json.dumps(payload, separators=(',',':'))
            payloadLen = len(payloadstr)
            fmt = "!cH32sH%ds" % payloadLen
            command = '\x00'
            msg = struct.pack(fmt, command, 32, token, payloadLen, payloadstr)
            sock = socket()
            s = SSL.Connection(ctx, sock)
            s.connect((apnHost, 2195))
            s.send(msg)
            s.shutdown()
            s.close()
            return {'status':'success','response':'ios_push_sent'}

        except Exception as e:
            return {'status':'failed','response':'push_notification_ios_error','description':e.args[0]}
