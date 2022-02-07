#-*- coding: utf-8 -*-

from mastodon import Mastodon
import subprocess
import json
import os
from os.path import join, dirname
from dotenv import load_dotenv

# Import keys from .env
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Generate Mastodon API instance
mastodon = Mastodon(
    access_token = os.environ.get("TOKEN"),
    api_base_url = os.environ.get("DOMAIN")
)

# Run generator
def res_cmd(cmd):
  return subprocess.Popen(
      cmd, stdout=subprocess.PIPE,
      shell=True).communicate()[0]

# Remove risky words from result
def remover(result):
  # Load banned.json
  json_open = open('data/banned.json', 'r')
  json_load = json.load(json_open)
  # Delete detected words from original sentences
  for w in json_load['words']:
    result = result.replace(w, '')
  return result

def main():
  # Get original sentences generated from markov-chains
  ## Run text_generator.py to get sentence.
  cmd = ("python3 text_generator.py")
  ## Put the generated sentence into 'result' variable
  result = res_cmd(cmd)
  result = result.decode()

  # Remove risky words from result
  result = remover(result)

  # Call Mastodon.py to toot
  mastodon.toot(result)

if __name__ == '__main__':
  main()
