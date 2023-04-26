import os
import sys
import time
import json
import click
import datetime
from pyicloud import PyiCloudService

def main():
    print("Setup Time Zone")
    time.strftime("%X %x %Z")
    os.environ["TZ"] = "Asia/Taipei"

    account = ""
    password = ""
    cfgdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'icloud.json')
    if os.path.exists(cfgdir):
        with open(cfgdir, 'r') as configData:
            data = json.loads(configData.read())
            account = data["account"]
            password = data["password"]

    print("Py iCloud Services")
    api = PyiCloudService(account, password)

    if api.requires_2fa:
        print("Two-factor authentication required. Your trusted devices are:")

        devices = api.trusted_devices
        for i, device in enumerate(devices):
            print(
                "  %s: %s"
                % (i, device.get("deviceName", "SMS to %s" % device.get("phoneNumber")))
            )

        device = click.prompt("Which device would you like to use?", default=0)
        device = devices[device]
        if not api.send_verification_code(device):
            print("Failed to send verification code")
            sys.exit(1)

        code = click.prompt("Please enter validation code")
        if not api.validate_verification_code(device, code):
            print("Failed to verify verification code")
            sys.exit(1)

    #
    # Events
    #
    print("Events")

    from_dt = datetime.datetime.now() + datetime.timedelta(days=1)
    to_dt = datetime.datetime.now() + datetime.timedelta(days=31)
    
    events = api.calendar.events(from_dt, to_dt)
    test = []
    for event in events:
        test.append([datetime.datetime(event["localStartDate"][1], event["localStartDate"][2], event["localStartDate"][3]), event["title"]])

    test.sort()
    for event in test:
        print(event[0].month, '/', event[0].day, ':', event[1])

if __name__=='__main__':
    main()
