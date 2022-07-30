from saveAPI import *
import requests
import json
import shodan

shodan_api = shodan.Shodan(shodan_read())


list = []
results = shodan_api.search('apache')
for server in results['matches']:
    print(f"data:\n{server['data']}")
    print(f"port:{server['port']}")
    print(f"hostnames:{server['hostnames']}")
    print(f"domains:{server['domains']}")
    print(f"ip_str:{server['ip_str']}")
    print("=============================================================")

    # list.append(server['ip_str'])


# print(list)
# print(len(list))

# print(results['data'])
