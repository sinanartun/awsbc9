import base64

encoded_secret = "lKMFVA1rDOPDXj8DmHHx9y3SSdTcxJodtp5M/2G722M="
decoded_secret = base64.b64decode(encoded_secret)

print(len(decoded_secret))