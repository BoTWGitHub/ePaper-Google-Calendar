import json

def main():
    with open('/etc/pisugar-server/config.json', 'r') as file:
        content = file.read()
        data = json.loads(content)
        print(data)

if __name__=='__main__':
    main()
