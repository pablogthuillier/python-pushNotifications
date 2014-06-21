python-pushNotifications
========================

A simple library for sending push notifications to an Android or iOS device

Android
=======

Requirements:
-------------
```bash
pip install python-gcm
```

Use:
---

Sending push notifications to an Android device is really simple.
You just need the API KEY provided by Google and use the class like this:
(Remenber: your api key is valid for every device which uses the app, the device token is generated for each device which install the app)

```python
androidNotificator = AndroidPushNotifications(api_key="WriteYourApiKeyHere")
your_message = "Hi, I am sending a message!"
your_token_device = "WriteYourTokenDeviceHere"
androidNotificator.send_push_notification(message = your_message, token_device = your_token_device)
```




iOS
===

Requirements:
-------------
```bash
pip install pyOpenSSL
```

Use:
----
Sending push notification to an iOS device requires more steps, but not complicated.

First at all, you need the two p12 files provided by X-code:
- The private key
- The certificate

In order to use the APNS (Apple Push Notification Service) pem files are required instead of p12 files.

For converting these files into pem files follow these steps:

```bash
#When ask a password, set one, but it will be removed from the pem file 

openssl pkcs12 -clcerts -nokeys -out certificate.pem -in certificate.p12
openssl pkcs12 -nocerts -out privatekey.pem -in privatekey.p12
openssl rsa -in privatekey.pem -out privatekey-noenc.pem
cat certificate.pem privatekey-noenc.pem > apns.pem
```

Now you have two files:
- The private key (privatekey-noenc.pem)
- The certificate (apns.pem)

Now you can use the class like in Android:
```python

privatekey = "privatekey-noenc.pem"
certificate = "certificate.pem"
ios = IOSPushNotifications(privatekey_filepath = privatekey, certificate_filepath=certificate)
#You can test the class before sending a push adding a "sandbox" argument to constructor (sandbox = True)
your_message = "Hi, I am sending a message!"
your_token_device = "WriteYourTokenDeviceHere"
ios.send_push_notification(message = your_message, token_device = your_token_device, badge = 1)

```






