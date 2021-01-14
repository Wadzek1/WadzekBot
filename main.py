import discord
import os
import requests
import json
import yaml
import wikipedia

client = discord.Client()

MESSAGE_PATH = "messages.yml"
message_file = open(MESSAGE_PATH, "r")
MESSAGES = yaml.safe_load(message_file)
message_file.close()
HELLO_WORLD_STRING = MESSAGES["helloWorld"]

BAD_WORD_PATH = "badWords.yml"
bad_word_file = open(BAD_WORD_PATH, "r")
BAD_WORDS_DATA = yaml.safe_load(bad_word_file)
bad_word_file.close()
BAD_WORDS = BAD_WORDS_DATA["badWords"]


def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0] ["q"] + " -" + json_data[0] ["a"]
  return(quote)


@client.event
async def on_ready():
  wikipedia.set_lang("de")
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
    msg_text.split(" ")
    number_of_options = msg_text[6]
    number_of_options = int(number_of_options)

    if number_of_options == 2:
      await message.add_reaction("1️⃣")
      await message.add_reaction("2️⃣")

    if number_of_options == 3:
      await message.add_reaction("1️⃣")
      await message.add_reaction("2️⃣")
      await message.add_reaction("3️⃣")

    if number_of_options == 4:
      await message.add_reaction("1️⃣")
      await message.add_reaction("2️⃣")
      await message.add_reaction("3️⃣")
      await message.add_reaction("4️⃣")

    if number_of_options == 5:
      await message.add_reaction("1️⃣")
      await message.add_reaction("2️⃣")
      await message.add_reaction("3️⃣")
      await message.add_reaction("4️⃣")
      await message.add_reaction("5️⃣")

  elif any(word in msg_text for word in BAD_WORDS):
    await message.channel.send(MESSAGES["wortwahl"])
  elif msg_text.startswith("!machterfehler?"):
    await message.channel.send("Ich mache keine Fehler, " + message.author.mention)
  elif msg_text.startswith("!quit"):
    if message.author.id in [323196084413267974, 277159146565009408]:
      await message.channel.send(f"Tschüß, {message.author.mention}!")
      await client.close()
      exit(0)
    else:
      await message.channel.send(f"Das darfst du nicht, {message.author.mention}!")
  elif msg_text.startswith("!info"):
    await message.channel.send("Hier sind Informationen über mich, du minderwertiges Stück Kohlenstoff:")
    await message.channel.send("https://wiki.coldmirror.net/wiki/A.R.S.C.H_9000")

  elif msg_text.startswith("!kiri"):
    oauth = os.getenv("TWITCH_OAUTH_TOKEN")
    parameters = { "query": "kirimctwitch" }
    headers = {
      "client-id": os.getenv("TWITCH_CLIENT_ID"),
      "Authorization": f"Bearer {oauth}"
    }

    request = requests.get("https://api.twitch.tv/helix/search/channels", params=parameters, headers=headers)
    top_hit = request.json()["data"][0]
    await message.channel.send(f"""Top Hit on Twitch:
```
{top_hit}
```""")

  elif msg_text.startswith("!istkirilive?"):
    oauth = os.getenv("TWITCH_OAUTH_TOKEN")
    parameters = { "query": "kirimctwitch" }
    headers = {
      "client-id": os.getenv("TWITCH_CLIENT_ID"),
      "Authorization": f"Bearer {oauth}"
    }

    request = requests.get("https://api.twitch.tv/helix/search/channels", params=parameters, headers=headers)
    top_hit = request.json()["data"][0]

    if not top_hit["is_live"]:
      await message.channel.send("kiron ist nicht live")
      await message.channel.send("Wenn Kiron streamt, kannst du ihn hier finden:")
      await message.channel.send("https://twitch.tv/kirimctwitch")
      await message.channel.send(top_hit["thumbnail_url"])
    else:
      await message.channel.send("kiron ist live → https://kirimcplay.tv/twitch")
  elif msg_text.startswith("!wannwarderersteweltkrieg?"):
    await message.channel.send("Der erste Weltkrieg ging vom 28. Juli 1914 bis zum 11. November 1918")
  elif msg_text.startswith("!wissen") and (len(msg_text.split(" ")) == 2):
    search_term = msg_text.split(" ")[1]
    summary = wikipedia.summary(search_term, sentences=2)
    if len(summary) > 2000:
      link = f"https://lmgtfy.app/#gsc.tab=0&gsc.q={search_term}"
      await message.channel.send(f"Entschuldige, {message.author.mention}, die ERSTEN ZWEI SÄTZE der Wikipedia-Zusammenfassung ist schon zu lang für eine Discord-Nachricht.\n{link}")
    else:
      await message.channel.send(
f"""\
\
**\
Hier hast du die ersten zwei Sätze der Zusammenfassung für \
"{search_term}"!\
\
**\n\n{summary}""")


client.run(os.getenv('DISCORD_TOKEN'))
