import os
import time
import json
import logging
import platform
import datetime
from pyicloud import PyiCloudService

def getiCloudCalendarEvents(eventsList: list):
    account = ""
    password = ""
    if platform.system() == "Windows":
        accountFile = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config\\icloud.json')
    else:
        accountFile = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config/icloud.json')
        
    if os.path.exists(accountFile):
        with open(accountFile, 'r') as configData:
            try:
                data = json.loads(configData.read())
                account = data["account"]
                password = data["password"]
            except:
                logging.error('icloud.json content error...')
                return
    else:
        logging.error(accountFile + ' doesn\'t exist')
        return

    time.strftime("%X %x %Z")
    os.environ["TZ"] = "Asia/Taipei"

    try:
        api = PyiCloudService(account, password)

        if api.requires_2fa:
            logging.warning("Two-factor authentication required.")
            code = input("Enter the code you received of one of your approved devices: ")
            result = api.validate_2fa_code(code)
            logging.warning("Code validation result: %s" % result)

            if not result:
                logging.error("Failed to verify security code")
                return

            if not api.is_trusted_session:
                logging.waring("Session is not trusted. Requesting trust...")
                result = api.trust_session()
                logging.waring("Session trust result %s" % result)

                if not result:
                    logging.error("Failed to request trust. You will likely be prompted for the code again in the coming weeks")
        elif api.requires_2sa:
            import click
            logging.waring("Two-step authentication required. Your trusted devices are:")

            devices = api.trusted_devices
            for i, device in enumerate(devices):
                logging.info(
                    "  %s: %s" % (i, device.get('deviceName',
                    "SMS to %s" % device.get('phoneNumber')))
                )

            device = click.prompt('Which device would you like to use?', default=0)
            device = devices[device]
            if not api.send_verification_code(device):
                logging.error("Failed to send verification code")
                return

            code = click.prompt('Please enter validation code')
            if not api.validate_verification_code(device, code):
                logging.error("Failed to verify verification code")
                return

        #
        # Events
        #
        from_dt = datetime.datetime.now() + datetime.timedelta(days=1)
        to_dt = from_dt + datetime.timedelta(days=31)
        
        events = api.calendar.events(from_dt, to_dt)
        for event in events:
            eventsList.append([datetime.datetime(event["localStartDate"][1], event["localStartDate"][2], event["localStartDate"][3]), event["title"]])

    except:
        logging.error('icloud api error...')
