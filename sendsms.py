import nexmo
#below keys are sepicific to the trail account
NEXMO_API_KEY = "d0c337c5"
NEXMO_API_SECRET = "IsX2MD8dcQaaFKlO"

to_number = +13174578822

client = nexmo.Client(key=NEXMO_API_KEY, secret=NEXMO_API_SECRET)

response = client.send_message({
    'from': 'Acme Inc',
    'to': to_number ,
    'text': 'Dear User, Your data is safe with us. Cheers to healthy lifestyle. From: Healthcare Management System',
})  
print("response: ", response)
response = response['messages'][0]

if response['status'] == '0':
  print ('Sent message', response['message-id'])
else:
    print("error: ",response['message-id'])