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
bot_version = '0.1-R1.25'
online_users = []
authorized_admin_roles = ['Admin']
authorized_mod_roles = ['Moderator']
authorized_users = []

if settings_filepath == '':
    settings_filepath = default_settings_filepath
    print('Loading default settings filepath...')

my_file = Path(settings_filepath)
if my_file.is_file():
    print('Settings File exists, loading settings now...')
    
    file = open(settings_filepath, 'r')
    settings = json.load(file)
    
    if settings['bot_version'] is bot_version:
        bot_version = settings['bot_version']
    server_id = settings['server_id']
    owner_id = settings['owner_id']
    bot_token = settings['bot_token']
    bot_description = settings['bot_description']
    bot_prefix = settings['bot_prefix']
    authorized_users = settings['authorized_users']
    authorized_admin_roles.clear()
    authorized_mod_roles.clear()
    authorized_admin_roles = settings['authorized_admin_roles']
    authorized_mod_roles = settings['authorized_mod_roles']
    
else:
    print('Settings File does not exist, please follow along for setup.')
    server_id = input('What is the Server ID?> ')
    owner_id = input('What is the Owners ID?> ')
    bot_token = input('What is the Bots Token?> ')
    bot_description = input('What is the Bots Description?> ')
    bot_prefix = input('What is the Bots Command Prefix? (Default:~)> ')
    if bot_prefix == '':
        bot_prefix = '~'
    

bot = commands.Bot(command_prefix=bot_prefix, description=bot_description + ' - Version: %s' % bot_version)

def set_globals():
    global bot_owner
    global bot_server
    bot_owner = bot.get_server(server_id).get_member(owner_id)
    bot_server = bot.get_server(server_id)
    
    auth_owner = 0
    for auth_user in authorized_users:
        if auth_user == bot_owner.name:
            auth_owner = 1
    if auth_owner == 0:
        authorized_users.append(bot_owner.name)

def save_settings():
    file = open(settings_filepath, 'w')
    settings = {"bot_version" : bot_version, "server_id" : server_id, "owner_id" : owner_id, "bot_token" : bot_token, "bot_description" : bot_description, "bot_prefix" : bot_prefix, "authorized_users" : authorized_users, "authorized_admin_roles" : authorized_admin_roles, "authorized_mod_roles" : authorized_mod_roles}
    json.dump(settings, file, indent=4, sort_keys=True)
    file.close()
    print('Settings Saved!')

# Begin loading bot
def debug(message):
    print('')

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
        return '[WARNING]: Member does not exist or is offline'
    else:
        user_found = 0
        for auth_user in authorized_users:
            if auth_user == member.name:
                user_found = 1
        if user_found == 1:
            authorized_users.remove(member.name)
            return '%s removed successfully' % member.name
        user_found = 0

def add_admins_role(role):
    role_found = 0
    if role is not None:
        for admin_role in authorized_admin_roles:
            if admin_role == role:
                role_found = 1
                return '%s is already an admin role.' % role
    if role_found == 0:
        authorized_admin_roles.append(role)
        return '%s added to admin roles successfully' % role
    role_found = 0
            
def remove_admins_role(role):
    role_found = 0
    if role is not None:
        for admin_role in authorized_admin_roles:
            if admin_role == role:
                role_found = 1
    if role_found == 1:
        authorized_admin_roles.remove(role)
        return '%s removed from admin roles successfully' % role
    return '%s is not an authorzied admin role.' % role
    role_found = 0

def add_mods_role(role):
    role_found = 0
    if role is not None:
        for mod_role in authorized_mod_roles:
            if mod_role == role:
                role_found = 1
                return '%s is already a mod role.' % role
    if role_found == 0:
        authorized_mod_roles.append(role)
        return '%s added to mod roles successfully' % role
    role_found = 0
    
def remove_mods_role(role):
    role_found = 0
    if role is not None:
        for mod_role in authorized_mod_roles:
            if mod_role == role:
                role_found = 1
    if role_found == 1:
        authorized_mod_roles.remove(role)
        return '%s removed from mod roles successfully' % role
    return '%s is not an authorized mod role.' % role
    role_found = 0

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

@bot.command(pass_context=True)
async def remove_auth_user(context, msg):
    if check_authorized_user(context.message.author):
        await bot.send_message(context.message.author, remove_authorized_user(msg))

@bot.command(pass_context=True)
async def add_admin_role(context, msg):
    if check_authorized_user(context.message.author):
        await bot.send_message(context.message.author, add_admins_role(msg))

@bot.command(pass_context=True)
async def remove_admin_role(context, msg):
    if check_authorized_user(context.message.author):
        await bot.send_message(context.message.author, remove_admins_role(msg))
    
@bot.command(pass_context=True)
async def add_mod_role(context, msg):
    if check_authorized_user(context.message.author):
        await bot.send_message(context.message.author, add_mods_role(msg))

@bot.command(pass_context=True)
async def remove_mod_role(context, msg):
    if check_authorized_user(context.message.author):
        await bot.send_message(context.message.author, remove_mods_role(msg))

@bot.command(pass_context=True)
async def test(context):
    for role in bot_server.get_member_named(context.message.author.name).roles:
        print(role.name)
    
@bot.command(pass_context=True)
async def logout(context):
    if check_authorized_user(context.message.author):
        await bot.say('Saving and logging out...')
        save_settings()
        await bot.logout()
        print('Bot Logged Out.')
  
bot.run(bot_token)