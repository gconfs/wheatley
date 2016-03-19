from sopel import module
from redmine import Redmine, ResourceNotFoundError
import re
from os import environ

# Redmine
envkey = environ.get('REDMINE_API_KEY')

if envkey:  # Found Redmine API key in environment variables
    apiKey = envkey
else:       # Nothing in env vars, let's try key.txt file
    try:
        apiKey = open("key.txt", 'r').readline().rstrip('\n')
    except:
        raise Exception("can't find any Redmine API key, neither in env nor in key.txt")

url     = "https://redmine.gconfs.fr"
version = "3.2.0.stable"
redmine = None

redmine = Redmine(url, key=apiKey, version=version)

@module.rule('(.*#[0-9]+.*)')
def hi(bot, trigger):
    msg = trigger.group(1) # Kinda dirty, fix it
    match = re.findall("#[0-9]+", msg)
    for matched in match:
      issuenb = int(matched[1:]) # Remove leading '#'
      try:
        issue = redmine.issue.get(issuenb)
        bot.say("[" + issue.tracker.name
                + " #" + str(issue.id)
                + " on " + issue.project.name + "] "
                + issue.subject + " : "
                + url + "/issues/" + str(issue.id))
      except ResourceNotFoundError:
        bot.say("Sorry, can't find issue #" + str(issuenb))

@module.commands('echo', 'repeat')
def echo(bot, trigger):
        bot.reply(trigger.group(2))
