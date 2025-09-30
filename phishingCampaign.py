import base64, email.utils, hmac, hashlib, requests, urllib, csv, sys, json
from time import sleep

def main():

    with open("config.json", "r") as config:
        apiKeys = json.load(config)

    userList = csvReader(sys.argv[1])
    for username in userList:
        pushRequest(username, apiKeys["AUTH_IKEY"],apiKeys["AUTH_SKEY"],apiKeys["API_HOSTNAME"])
        sleep(5)


def sign(params, method, host, path, skey, ikey):
    # create canonical string
    now = email.utils.formatdate()
    canon = [now, method.upper(), host.lower(), path]
    args = []
    for key in sorted(params.keys()):
        val = params[key].encode("utf-8")
        args.append(
            '%s=%s' % (urllib.parse.
                       quote(key, '~'), urllib.parse.quote(val, '~')))

    canon.append('&'.join(args))
    canon = '\n'.join(canon)
    # sign canonical string
    sig = hmac.new(bytes(skey, encoding='utf-8'),
                   bytes(canon, encoding='utf-8'),
                   hashlib.sha1)
    auth = '%s:%s' % (ikey, sig.hexdigest())
    # return headers
    return {'Date': now, 'Authorization': 'Basic %s' % base64.b64encode(bytes(auth, encoding="utf-8")).decode()}

def pushRequest(username, ikey, skey, api_host):
    METHOD = "POST"
    API_PATH = "/auth/v2/auth"
    PARAMS = {"device":"auto", "factor":"push", "username":username}
    URL = f'https://{api_host}{API_PATH}'

    headers = sign(PARAMS, METHOD,api_host,API_PATH,skey, ikey)
    response = requests.post(URL, headers=headers, data=PARAMS)
    response = response.json()

    if "code" in response:
        print(f"No push capable devices found for {username}")
        print(response)

    elif "response" in response:
        print(username + ": " + response["response"]["result"])
        print(response)

def csvReader(filename):
    usernames = []

    with open(filename, "r") as csvf:
        reader = csv.DictReader(csvf, delimiter=",")
        for row in reader:
            usernames.append(row["Username"])

    return usernames

main()

