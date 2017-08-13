# MzQ1NjM2MjY1MzQ3MjUyMjM1.DG-Klg.ewkeS1cwl_REPPewIkT3-Zkwbgs

import discord
import json
from discord.ext import commands
from pathlib import Path

# Put your Settings File path here to avoid typing it in everytime
custom_settings_filepath = 'C:\\Users\\David\\Desktop\\Settings.json'

# ------------------------------------------------
# --- [ Do not edit ANYTHING below this line ] ---
# ------------------------------------------------

default_settings_filepath = 'Settings.json'
settings_filepath = input('Where can we find bot settings? (Push Enter for default)> ')

if settings_filepath == '':
    settings_filepath = default_settings_filepath
    print('Loading default settings filepath...')

my_file = Path(settings_filepath)
if my_file.is_file():
    print('Settings File exists, loading settings now...')
    
    file = open(settings_filepath, 'r')
    settings = json.load(file)
    
    bot_version = settings['bot_version']
    server_id = settings['server_id']
    owner_id = settings['owner_id']
    bot_token = settings['bot_token']
    bot_description = settings['bot_description']
    bot_prefix = settings['bot_prefix']
    authorized_users = settings['authorized_users']
else:
    print('Settings File does not exist, please follow along for setup.')
    server_id = input('What is the Server ID?> ')
    owner_id = input('What is the Owners ID?> ')
    bot_token = input('What is the Bots Token?> ')
    bot_description = input('What is the Bots Description?> ')
    bot_prefix = input('What is the Bots Command Prefix? (Default:~)> ')
    bot_version = '0.1-R1.5'
    if bot_prefix == '':
        bot_prefix = '~'
    

bot = commands.Bot(command_prefix=bot_prefix, description=bot_description + ' - Version: %s' % bot_version)
online_users = []
authorized_admin_roles = ['Admin']
authorized_mod_roles = ['Moderator']
authorized_users = []

def set_globals():
    global bot_owner
    global bot_server
    global debug_toggle_code
    bot_owner = bot.get_server(server_id).get_member(owner_id)
    bot_server = bot.get_server(server_id)
    debug_toggle_code = 0
    
    auth_owner = 0
    for auth_user in authorized_users:
        if auth_user == bot_owner.name:
            auth_owner = 1
    if auth_owner == 0:
        authorized_users.append(bot_owner.name)

def save_settings():
    file = open(settings_filepath, 'w')
    settings = {"bot_version" : bot_version, "server_id" : server_id, "owner_id" : owner_id, "bot_token" : bot_token, "bot_description" : bot_description, "bot_prefix" : bot_prefix, "authorized_users" : authorized_users}
    json.dump(settings, file, indent=4, sort_keys=True)
    file.close()
    print('Settings Saved!')

# Begin loading bot
def debug(message):
    if debug_toggle_code == 1:
        print('[DEBUG] %s' % message)

def refresh_online_users():
    online_users.clear()
    
    for member in bot_server.members:
        if member.status is discord.Status.online:
            online_users.append(member.name)
            debug(member.name)

def check_authorized_user(user):    
    for auth_user in authorized_users:
        if auth_user == user.name:
            return True
    return False
            
def add_authorized_user(user):
    member = bot_server.get_member_named(user)
    if member == None:
        debug('[WARNING]: Member does not exist or is offline')
        return '[WARNING]: Member does not exist or is offline'
    else:
        user_found = 0
        for auth_user in authorized_users:
            if auth_user == member.name:
                user_found = 1
                debug('[WARNING]: %s is already an authorized user' % member.name)
                return '[WARNING]: %s is already an authorized user' % member.name
        if user_found == 0:
            authorized_users.append(member.name)
            return '%s added successfully' % member.name
            debug('%s Added' % member.name)
        user_found = 0

def remove_authorized_user(user):
    member = bot_server.get_member_named(user)
    
    if member == None:
        debug('[WARNING]: Member does not exist or is offline')
        return '[WARNING]: Member does not exist or is offline'
    else:
        user_found = 0
        for auth_user in authorized_users:
            if auth_user == member.name:
                user_found = 1
        if user_found == 1:
            authorized_users.remove(member.name)
            return '%s removed successfully' % member.name
            debug('%s Removed' % member.name)
        user_found = 0
        debug('[WARNING]: %s is not an authorized user.' % member.name)

#------------------------------------------------------------------------------

#            Below is all the commands and events

#------------------------------------------------------------------------------
@bot.event
async def on_ready():
    print(bot.description)
    print('Logged in as:\nUser: %s | ID: %s' % (bot.user.name, bot.user.id))
    set_globals()
    save_settings()

@bot.command(pass_context=True)
async def version(context):
    if check_authorized_user(context.message.author):
        await bot.say('Bot Version: %s' % bot_version)

@bot.command()
async def get_online_users():
    refresh_online_users()
    await bot.say('The users online are: %s' % online_users)

@bot.command(pass_context=True)
async def add_auth_user(context, msg):
    if check_authorized_user(context.message.author):
        await bot.send_message(context.message.author, add_authorized_user(msg))
        debug(authorized_users)

@bot.command(pass_context=True)
async def remove_auth_user(context, msg):
    if check_authorized_user(context.message.author):
        await bot.send_message(context.message.author, remove_authorized_user(msg))
        debug(authorized_users)

@bot.command(pass_context=True)
async def debug_toggle(context):
    if debug_toggle_code == 0:
        debug_toggle_code = 1
        await bot.send_message(context.message.author, 'Debug enabled. Check console for debug messages.')
    else:
        debug_toggle_code = 0
        await bot.send_message(context.message.author, 'Debug disabled.')
    
@bot.command(pass_context=True)
async def logout(context):
    if check_authorized_user(context.message.author):
        await bot.say('Logging out...')
        await bot.logout()
        print('Bot Logged Out.')
  
bot.run(bot_token)