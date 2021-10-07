import discord
from discord.ext.commands import Bot
import os
from dotenv import load_dotenv
from api_request import get_spell_info, get_spell_list, get_monsters_list, get_list_of

load_dotenv()

version = '1.0.0'
bot = Bot(command_prefix='$')
token = os.getenv("DISCORD_TOKEN")
bmab = 'https://www.buymeacoffee.com/kevinneves'


@bot.event
async def on_ready():
    print(f'Bot Ready. Logged as {bot.user}')
    await bot.change_presence(activity=discord.Game('Minecraft'))


@bot.command(name='list',
            help='Get the list of any of these items using the following words: \n\
                    Classes, Subclasses, Races, Skills, Alignments, Languages, Proficiencies\n\
                    Exmaple: $list Classes')
async def list(context, item):
    print(f'Log: Trying to retrieve a list of {item}')
    info = get_list_of(item)

    # Debug
    if len(info) > 0:
        print(f'Log: Got the list of {item}')
    else:
        print(f'Log: Error. Info not found.')

    #Send the info
    await context.channel.send(info)


@bot.command(name='spells',
             help='Say the level and I give you the info. Example: $spells 5')
async def spells(context, lvl: int):
    print(f'Log: Trying to retrieve a list of spells of level {lvl}')
    info = get_spell_list(lvl)

    # Debug
    if len(info) > 0:
        print(f'Log: Got the info for spells lvl{lvl}')
    else:
        print(f'Log: Error. Info not found.')

    # Send the info
    await context.channel.send(info)


@bot.command(name='spell',
             help='Say the name of the spell and I give you all the info. \
             Examples: $spell Acid arrow')
async def spell(context, *args):
    name = '-'.join([args for args in args])
    print(f'Log: Trying to retrieve {name} info')
    info = get_spell_info(name)

    # Debug
    if len(info) > 0:
        print(f'Log: Got the info for {name}')
    else:
        print(f'Log: Error. Info not found.')

    # Send the info
    if len(info) < 2000:
        await context.channel.send(info)
    else:
        await context.channel.send(info[:1999])
        await context.channel.send(info[2000:])


@bot.command(name='monsters',
             help='Say the Challenge Rate and I give you the list of monsters. \
             Example: $monsters 12')
async def monsters(context, cr: float):
    if cr.is_integer(): cr = int(cr)
    print(f'Log: Trying to retrieve a list of monsters of CR {cr}')
    info = get_monsters_list(cr)

    # Debug
    if len(info) > 0:
        print(f'Log: Got the info for monsters lvl {cr}')
    else:
        print(f'Log: Error. Info not found.')
        await context.channel.send(f'There are no monsters of CR {cr}')

    # Send the info
    await context.channel.send(info)


if __name__ == '__main__':
    bot.run(token)

