import requests

url = "https://www.fast2sms.com/dev/bulk"

msg = "Vehicle No: CG04DJ 1721\nDate: 21/10/2019\nTime: 12:30:15\n Visitor"


querystring = {"authorization":"my8icw0ebfonXukEPQYIjG1qLTSKMNWdBhJr3V72CvgFZ6aUslCl42JqOKsaUoWN7IruchnPfimzeFRG","sender_id":"FSTSMS","message":msg,"language":"english","route":"p","numbers":"9109791199"}

headers = {
    'cache-control': "no-cache"
}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)