from firebase import firebase
firebase = firebase.FirebaseApplication("https://fastgate-d2d06.firebaseio.com/",None)

res = firebase.get('/USER/jO558PE7qzMdKsTAZUa85qRTCKD2/request',None)
print(res['permission'])