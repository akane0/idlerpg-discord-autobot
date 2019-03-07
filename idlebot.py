import discord
import asyncio
import random
from discord.ext import commands

client = commands.Bot(command_prefix="-")
token = "hehe xd"


@client.event
async def on_ready():
    print("-------")
    print("Logged in as:")
    print("User: " + client.user.name + "#" + client.user.discriminator)
    print("ID: " + client.user.id)
    print("idle-rpg full bot")
    print("-------")
    client.gambling = "off"
    client.autoquest = "off"

@client.command(pass_context=True)
async def s(ctx, *, args):

    await client.say(args)

@client.command(pass_context=True)
async def p(ctx, amount):

    if int(amount) <= 0:
        await client.send_message(ctx.message.channel, "Amount too low.")
    else:
        await client.send_message(ctx.message.channel, "$give {} {}".format(amount, ctx.message.author.mention))


@client.command(pass_context=True)
async def b(ctx):

    await client.send_message(ctx.message.channel, "$e")

@client.command(pass_context=True)
async def startquest(ctx, questnumber="1", repetition=1):

    timers = {
    '1': 1800,
    '2': 3600,
    '3': 7200,
    '4': 10800,
    '5': 14400,
    '6': 18000,
    '7': 21600,
    '8': 25200,
    '9': 28800,
    '10': 32400,
    '11': 36000,
    '12': 39600,
    '13': 43200,
    '14': 46800,
    '15': 50400,
    '16': 54000,
    '17': 57600,
    '18': 61200,
    '19': 64800,
    '20': 68400,
    }

    if questnumber not in timers.keys():
        await client.send_message(ctx.message.channel, "Not a valid dungeon number")
        return

    print("Starting auto-quest... looping {} times...".format(repetition))

    time = timers[questnumber]

    loop = 0
    timing = 0

    await client.send_message(ctx.message.channel, "Starting quest [{}]. Repeating [{}] times.".format(questnumber, repetition))

    client.autoquest = "on"

    while loop < repetition:
        await client.send_message(ctx.message.channel, "$a {}".format(questnumber))
        print("Sleeping for {} seconds".format(time))

        while timing <= time and client.autoquest == "on":
            await asyncio.sleep(1)
            timing += 1

        if client.autoquest == "off":
            print("Autoquest has been stopped manually...")
            return

        await client.send_message(ctx.message.channel, "$status")
        await asyncio.sleep(2)
        loop += 1

    print("Autoquest has been stopped...")


@client.command(pass_context=True)
async def startgamble(ctx):

    print("Starting gambling script...")

    await client.say("$e")

    print("Waiting for response...")

    msg = await client.wait_for_message(timeout=None)
    msgc = msg.content

    client.gambling = "on"
    print(msgc)

    filter_1 = msgc[msgc.find("$")+1:]
    filter_2 = filter_1[:filter_1.find("*")]

    bankroll = filter_2

    print("Found bankroll {}...".format(bankroll))

    while client.gambling == "on":

        await asyncio.sleep(1)

        bet = int(bankroll) * .25

        if bet <= 0:
            print("Force betting $1...")
            bet = 1

        print("Betting {}...".format(bet))

        await asyncio.sleep(5)

        await client.say("$flip {} {}".format(random.choice(["heads", "tails"]), int(bet)))

        await asyncio.sleep(0.01)

        result = await client.wait_for_message(timeout=None)

        print("Waiting for response...")
        
        # hehe xd bad coding practices down here

        if "lost" in result.content:
            bankroll = int(bankroll) - bet
            print("Lost..")
            print("Bankroll: ", bankroll)
        elif "won" in result.content:
            bankroll = int(bankroll) + bet
            print("Won..")
            print("Bankroll: ", bankroll)
        else:
            if "$flip" in result.content:
                print("Read flip instead of IdleRPG, attempting to read log...")

                await asyncio.sleep(5)

                async for message in client.logs_from(ctx.message.channel, limit=1):
                    if "lost" in message.content:
                        bankroll = int(bankroll) - bet
                        print("Lost..")
                        print("Bankroll: ", bankroll)
                    elif "won" in message.content:
                        bankroll = int(bankroll) + bet
                        print("Won..")
                        print("Bankroll: ", bankroll)
                    elif message.author == client.user:
                        print("Read own message, bot may be offline, trying to read message again...")

                        await asyncio.sleep(5)

                        async for message in client.logs_from(ctx.message.channel, limit=1):
                            if "lost" in message.content:
                                bankroll = int(bankroll) - bet
                                print("Lost..")
                                print("Bankroll: ", bankroll)
                            elif "won" in message.content:
                                bankroll = int(bankroll) + bet
                                print("Won..")
                                print("Bankroll: ", bankroll)
                            else:
                                print("Could not recognize text... shutting down")
                                print("Text: {}".format(result.content))
                                print("Bankroll: ", bankroll)
                                client.gambling = "off"

    await asyncio.sleep(1)
    print("Gambling has stopped...")


@client.command(pass_context=True)
async def stopgamble(ctx):

    client.gambling = "off"
    print("Attempting to stop gambling...")


@client.command(pass_context=True)
async def stopautoquest(ctx):

    client.autoquest = "off"
    print("Attempting to stop autoquest...")


# @client.command(pass_context=True)
# async def autosteal(ctx):
#     pass

client.run(token, bot=False)
