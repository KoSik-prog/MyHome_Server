import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging

class Notifications:
    tokens = {"kosik":"cx-Nog-HSm6QOutoyDJPJi:APA91bGcLLmpYyDt2RpeP3Rli4zJ_hTS6nVmJfWhqJXEnabIMVWp85MZhoEbhs3IVh16Xzc4v9wrf8xdZOBo89u9qqpiY73BzxD4b6D8XQ8W1g5cJ89AviI5caSBD6nNcdpm2wn7zLV6"}

    def __init__(self, keyFileName):
        self.cred = credentials.Certificate(keyFileName)
        firebase_admin.initialize_app(cred)

    def update_token(self, user, token):
        if user in self.tokens:
            print("Token for user {} has been updated".format(user))
        else:
            print("Token for user {} has been created".format(user))
        self.tokens[user] = token
        return True
    
    def send_notification(self, title, message):
        registration_tokens = [token for token in self.tokens.values()]

        message = messaging.MulticastMessage(
            notification=messaging.Notification(
                title=title,
                body=message
            ),
            tokens=registration_tokens,
        )

        response = messaging.send_multicast(message)
        print('Notifications sent: ', response.success_count, ' / failed:', response.failure_count)

        for idx, resp in enumerate(response.responses):
            if not resp.success:
                print('Token send error', registration_tokens[idx], ':', resp.exception)


phoneNotification = Notifications('firebase/myhome-7a62a-firebase-adminsdk-dxnth-6a54be3a53.json')