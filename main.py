import os
import time

import discord
from dotenv import load_dotenv, set_key, find_dotenv
import requests

load_dotenv()
PORTAINER_URL = os.getenv("PORTAINER_URL")
PORTAINER_PASSWORD = os.getenv("PORTAINER_PASSWORD")
PORTAINER_USERNAME = os.getenv("PORTAINER_USERNAME")


def get_container_id():
    x = requests.get(url=PORTAINER_URL + "/api/endpoints/2/docker/containers/json?all=true",
                     headers={"Authorization": JWT_TOKEN})
    containers = x.json()
    for container in containers:
        # print(container["Names"])
        if container["Names"][0] == "/twitch-watcher":
            os.environ["CONTAINER_ID"] = container["Id"]
            # set_key(find_dotenv(), key_to_set="CONTAINER_ID", value_to_set=os.environ["CONTAINER_ID"])
            break
        else:
            continue


def generate_portainer_token():
    # dotenv_path = find_dotenv()
    x = requests.post(url=PORTAINER_URL + "/api/auth",
                      json={"Username": PORTAINER_USERNAME, "Password": PORTAINER_PASSWORD})
    # os.environ["JWT_TOKEN"] = x.json()['jwt']
    # set_key(dotenv_path, key_to_set="JWT_TOKEN", value_to_set=os.environ["JWT_TOKEN"])
    return x.json()['jwt']


JWT_TOKEN = "Bearer " + generate_portainer_token()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
get_container_id()
CONTAINER_ID = os.getenv("CONTAINER_ID")

client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


def start_container(jwt_TOKEN=JWT_TOKEN):
    x = requests.post(url=PORTAINER_URL + "/api/endpoints/2/docker/containers/" + CONTAINER_ID + "/start",
                      headers={"Authorization": jwt_TOKEN})
    return str(x)


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    content = "Fan Rewards are available"
    me = await client.fetch_user("767771024791830528")

    if content in message.content:
        response_code = start_container()
        count = 0
        while "401" in response_code or count < 5:
            if "204" in response_code:
                await me.send("twitch-watcher is now running")
                break

            elif "304" in response_code:
                await me.send("twitch-watcher is already running")
                break
            elif "401" in response_code:
                await me.send("twitch-watcher can not be started due unexpected error\nTrying again")
                jwt_TOKEN = "Bearer " + generate_portainer_token()
                start_container(jwt_TOKEN)
                count += 1


# print(CONTAINER_ID)
client.run(DISCORD_TOKEN)

# print("401" in str(start_container()))
# generate_portainer_token()
# time.sleep(5)
# print(os.getenv("JWT_TOKEN"))
