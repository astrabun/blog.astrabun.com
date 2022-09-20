#!/usr/bin/env python
import json
from os import getenv
from time import sleep
import requests
from datetime import datetime

API_ENDPOINT = getenv("TIKTOK_USER_INFO_API_ENDPOINT")
TOKEN = getenv("TIKTOK_USER_INFO_API_TOKEN")
SLEEP_TIME = 1


def main():
  ### get original notes into usernames file, this is unnecessary now
  # with open("accounts_manual_notes.json", "r") as f:
  #   a = json.load(f)
  # usernames = [u['username'] for u in a]
  # with open("usernames.json", "w") as f:
  #   f.write(json.dumps(usernames, indent=4))
  header_obj = {"User-Agent": "AstraBunScripting/1.0"}
  updated = False
  try:
    with open("user_data.json", "r") as f:
      user_data = json.load(f)
  except:
    print("user_data.json not found, continuing with fresh run")
    user_data = {
      "metadata": {
        "last_updated": datetime.now().isoformat(sep="-")
      },
      "users": {}
    }

  with open("usernames.json", "r") as f:
    users = json.load(f)

  for idx, user in enumerate(users):
    print(f"Checking {user}... ({idx+1}/{len(users)})")
    if user not in user_data['users'].keys():
      api_url = f"{API_ENDPOINT}?token={TOKEN}&username={user}"
      while True:
        try:
          r = requests.get(api_url, headers=header_obj)
          break
        except Exception as e:
          print(f"Encountered exception, retrying... {e}")
          sleep(SLEEP_TIME)
      try:
        user_data['users'][user] = r.json()
        updated = True
      except:
        print(f"Unable to save data for {user}")
      print(f"Checking {user}... DONE")
      sleep(SLEEP_TIME)
    else:
      print(f"Checking {user}... DONE (skipped; already cached)")
  ts = datetime.now().isoformat(sep="-")
  if updated == True:
    user_data['metadata'] = {}
    user_data['metadata']['last_updated'] = ts
  with open("user_data.json", "w") as f:
    f.write(json.dumps(user_data, indent=4))
  with open(f"user_data_snapshot-{ts}.json", "w") as f:
    f.write(json.dumps(user_data, indent=4))

  print(f"DONE. Wrote data about {len(user_data['users'].keys())} user(s)")
  



if __name__ == "__main__":
  main()