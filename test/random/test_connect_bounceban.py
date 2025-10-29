from requests import request

BOUNCEBAN_API_KEY = "1ce278670c06f7170e28eab013718756"

headers = {
    "Authorization" : BOUNCEBAN_API_KEY,
    "Content-Type" : "application/json"
}

# body = {
#     "emails" : ["janca.aleksandar1@gmail.com", "alex@code2b.co", "alex@roompulse.io"]
# }
#
# response = request(method="POST", url="https://api.bounceban.com/v1/verify/bulk", headers=headers, json=body)
# print(response.json())


params = {
    "id" : "68f77f12f53fc9143c1ff422",
    "state" : "deliverable",
    "retrieve_all" : 1
}

response = request(method="GET", url="https://api.bounceban.com/v1/verify/bulk/dump", headers=headers, params=params)
print(response.json())