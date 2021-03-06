import discord
import os
import requests
import json
import yaml
import wikipedia

import warnings
warnings.filterwarnings("ignore")  # This ignores the stupid wikipedia warning no one likes or even cares about that isn't actually from wikipedia but only shows because the wikipedia module doesn't ignore so we need to do it with this two liner that is way too long because of this stupid comment but I am pretty mad at the devs of the wikipedia module for this that's why I am writing so much k thx bye

from wikipedia.exceptions import PageError
from wikipedia.exceptions import DisambiguationError

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

role_msg_id = 795005876112326683

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0] ["q"] + " -" + json_data[0] ["a"]
  return(quote)


@client.event
async def on_reaction_add(reaction, reactor, message):
  # https://discordpy.readthedocs.io/en/latest/api.html#reaction
  message_reacted_on = reaction.message
  message_id = message_reacted_on.id
  reaction_emoji = reaction.emoji
  reacted_by_me = reaction.me
  if reacted_by_me:
    return

  if message_id == role_msg_id:
    print("Die Nachricht mit command wurde erfolgreich erkannt")
    print(message_reacted_on.id)
    print(reaction_emoji)
    print(reactor)


@client.event
async def on_reaction_remove(reaction, reactor):
  message_reacted_on = reaction.message
  reaction_emoji = reaction.emoji
  reacted_by_me = reaction.me
  print("hello")


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
    msg_parts = msg_text.split(" ")
    number_of_options = int(msg_parts[1])

    if number_of_options in [2, 3, 4, 5, 6, 7, 8, 9, 10]:
      await message.add_reaction("1️⃣")
      await message.add_reaction("2️⃣")
      if number_of_options >= 3:
        await message.add_reaction("3️⃣")
      if number_of_options >= 4:
        await message.add_reaction("4️⃣")
      if number_of_options >= 5:
        await message.add_reaction("5️⃣")
      if number_of_options >= 6:
        await message.add_reaction("6️⃣")
      if number_of_options >= 7:
        await message.add_reaction("7️⃣")
      if number_of_options >= 8:
        await message.add_reaction("8️⃣")
      if number_of_options >= 9:
        await message.add_reaction("9️⃣")
      if number_of_options >= 10:
        await message.add_reaction("🔟")
    else:
      await message.channel.send("Du kannst 2-10 Optionen erstellen: `!poll <mengeAnOptionen>`")

      if allow_abstain_vote:
          await message.add_reaction("😶")  # Emoji can be changed, but I thougt the lack of expression on the face fits to abstaining ~kiriDevs

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
    else:
      await message.channel.send("kiron ist live → https://kirimcplay.tv/twitch")

  elif msg_text.startswith("!wannwarderersteweltkrieg?"):
    await message.channel.send("Der erste Weltkrieg ging vom 28. Juli 1914 bis zum 11. November 1918")

  elif msg_text.startswith("!wissen") and (len(msg_text.split(" ")) == 2):
    try:
      search_term = msg_text.split(" ")[1]
      summary = wikipedia.summary(search_term)
      summary_parts = summary.split(". ")

      if len(summary_parts) >= 3:
        summary = f"{summary_parts[0]}.   {summary_parts[1]}. {summary_parts[2]}."
      elif len(summary_parts) == 2:
        summary = f"{summary_parts[0]}. {summary_parts[1]}."
      elif len(summary_parts) == 1:
        summary = f"{summary_parts[0]}."
      else:
        message.channel.send("Tut mir leid, {message.author.mention}, dazu konnte ich keine Zusammenfassung finden")

      if len(summary) > 2000:
        link = f"https://lmgtfy.app/#gsc.tab=0&gsc.q={search_term}"
        await message.channel.send(f"Entschuldige, {message.author.mention}, die ERSTEN DREI SÄTZE der Wikipedia-Zusammenfassung sind schon zu lang für eine Discord-Nachricht.\n{link}")
      else:
        await message.channel.send(
f"""\
\
**\
Hier hast du die Zusammenfassung des Wikipedia-Artikels für \
"{search_term}"!\
\
**\n\n{summary}""")

    except PageError:
      await message.channel.send(f"Tut mir leid, {message.author.mention}, dazu konnte ich keine Wikipedia-Seite finden.")
    except DisambiguationError:
      await message.channel.send(f"Tut mir leid, {message.author.mention}, dazu gibt es zu viele mögliche Einträge. Bitte versuche, dich etwas spezifischer auszudrücken.")

  elif msg_text.startswith("!rollenzuteilung"):
      message_with_command = message
      role_msg_id = message_with_command.id
      await message.channel.send(role_msg_id)

client.run(os.getenv('DISCORD_TOKEN'))
