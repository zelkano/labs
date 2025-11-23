exec(open('0_global_vars.py').read())

my_user = 'admin'
my_pass = getpass.getpass(prompt='Enter Pass: ')
bigip = 'bigip-a.example.net'
if_name='1.1'
url=f"https://{bigip}/mgmt/tm/net/interface/{if_name}"

auth_to_encode = f"{my_user}:{my_pass}"
b64_auth = base64.b64encode(auth_to_encode.encode()).decode()
basic = f"Basic {b64_auth}"


f5_authheader = {'Content-Type': 'application/json','Authorization' : basic}

test = requests.get(url, headers=f5_authheader,verify=False)
outs = test.json()
output = json.dumps(outs, indent=4)
print(output)

if outs.get("enabled") is True:
    print("1.1 is Enabled")
elif outs.get("disabled") is True:
    print("1.1 is Disabled")
else:
    print("Unknown")

payload = {"disabled" : True}
test2 = requests.patch(url, json=payload,headers=f5_authheader,verify=False)

print(test2.status_code)

test = requests.get(url, headers=f5_authheader,verify=False)
outs = test.json()
output = json.dumps(outs, indent=4)
print(output)

if outs.get("enabled") is True:
    print("1.1 is Enabled")
elif outs.get("disabled") is True:
    print("1.1 is Disabled")
else:
    print("Unknown")