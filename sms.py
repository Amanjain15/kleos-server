import requests
import keys
# from key.models import KeysData


def send_sms(mobile, msg, sender="GSTINV"):
    try:
        # authkey = str(KeysData.objects.get(key="msg91").value)
        authkey = keys.KEY_MSG91
        url = 'http://api.msg91.com/api/sendhttp.php?authkey=' + authkey + '&mobiles='
        url += mobile
        url += '&message=' + msg
        url += '&sender=' + sender + '&route=4'
        print url
        print requests.request('GET', url)
    except Exception as e:
        print(str(e))
