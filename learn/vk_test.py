#!/usr/bin/env python3
"""
Get user first and last name in vk.com
"""

import vk_requests


def getInfo(api, ID):
    user = api.users.get(user_ids=ID)[0]
    if user["first_name"] != "DELETED":
        print("ID: {:8} First name: {:15} Last name: {}".
              format(user["id"], user["first_name"], user["last_name"]))


def start():
    api = vk_requests.create_api(app_id=6480738, service_token="31cc5d6031cc5d6031cc5d604e31\
aebe02331cc31cc5d606b3059678598a91622bc33d3")

    for ID in range(1, 100):
        getInfo(api, ID)


if __name__ == "__main__":
    start()

