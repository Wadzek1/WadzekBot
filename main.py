import discord
import os
import requests
import json
import yaml

client = discord.Client()

MESSAGE_PATH = "messages.yml"
message_file = open(MESSAGE_PATH, "r")
messages = yaml.safe_load(message_file)
message_file.close()
HELLO_WORLD_STRING = messages["helloWorld"]

BAD_WORD_PATH = "badWords.yml"
bad_word_file = open(BAD_WORD_PATH, "r")
bad_words_data = yaml.safe_load(bad_word_file)
bad_word_file.close()
BAD_WORDS = bad_words_data["badWords"]

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0] ["q"] + " -" + json_data[0] ["a"]
  return(quote)

@client.event
async def on_ready():
  print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
  msg_text = message.content.lower()

  if message.author == client.user:
    return

  if msg_text.startswith('!hello'):
    await message.channel.send(HELLO_WORLD_STRING)
  elif msg_text.startswith("!inspiration"):
    quote = get_quote()
    await message.channel.send(quote)
  elif msg_text.startswith("!poll"):
    await message.add_reaction("1️⃣")
    await message.add_reaction("2️⃣")
  elif any(word in msg_text for word in BAD_WORDS):
    await message.channel.send(messages["wortwahl"])
  elif msg_text.startswith("!machterfehler?"):
    await message.channel.send("WadzekBot macht keine Fehler, " + message.author.mention)
  elif msg_text.startswith("!quit"):
    if message.author.id in [323196084413267974, 277159146565009408]:
      await message.channel.send(f"Tschüß, {message.author.mention}!")
      await client.close()
    else:
      await message.channel.send(f"Das darfst du nicht, {message.author.mention}!")
client.run(os.getenv('DISCORD_TOKEN'))
