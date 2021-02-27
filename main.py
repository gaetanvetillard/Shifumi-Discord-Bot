from asyncio.tasks import wait
from gc import DEBUG_SAVEALL
import discord
import random
import time
import asyncio

from discord.message import convert_emoji_reaction

CHOICE = ["🤚", "👊","✌"]
YES_NO = ["✅", "❌"]
DISCORD_BOT_TOKEN = "YOUR DISCORD BOT TOKEN"

def get_random_choice():
    """This function return a random choice for the bot"""
    choice = random.choice(CHOICE)
    return choice

def check(reaction, user):
    return reaction, user

def how_has_won(host_choice, host_mention, opponent_choice, opponent_mention, game_mode):
    """This function return a string with the result"""

    if game_mode == "vs":
        if host_choice == opponent_choice:
            return "Draw ! Game will restart again soon..."
        elif host_choice == "🤚" and opponent_choice == "👊":
            return f"🎉 {host_mention} has won ! 🎉"
        elif host_choice == "👊" and opponent_choice == "✌":
            return f"🎉 {host_mention} has won ! 🎉"
        elif host_choice == "✌" and opponent_choice == "🤚":
            return f"🎉 {host_mention} has won ! 🎉"
        else:
            return f"🎉 {opponent_mention} has won ! 🎉"
    elif game_mode == "solo":
        if host_choice == opponent_choice:
            return "Draw ! Game will restart again soon..."
        elif host_choice == "🤚" and opponent_choice == "👊":
            return f"🎉 {host_mention} has won ! 🎉"
        elif host_choice == "👊" and opponent_choice == "✌":
            return f"🎉 {host_mention} has won ! 🎉"
        elif host_choice == "✌" and opponent_choice == "🤚":
            return f"🎉^{host_mention} has won ! 🎉"
        else:
            return f"Sorry, I won. Try again :)"


client = discord.Client(activity=discord.Game("$start to start the game"),)



@client.event
async def on_ready():
    print(f'Ready with {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    channel = message.channel
    host = message.author
    host_mention = f"<@!{host.id}>"

    if message.content.startswith('$start vs'):
        try:
            opponent = message.content.split(' ')[2]
            try:
                opponent_id = int(opponent.split("!")[1].split('>')[0])
                opponent_mention = f"<@!{opponent_id}>"
            except IndexError:
                opponent_id = int(opponent.split("@")[1].split('>')[0])
                opponent_mention = f"<@!{opponent_id}>"

        except (IndexError, ValueError):
            embed = discord.Embed(title="Sorry, you need to mention somebody.", description="**Try again.**")
            embed.set_footer(text=f"Host : {host}", icon_url=host.avatar_url)
            bot_msg = await channel.send(embed=embed)

        if "@" not in opponent_mention:
            embed = discord.Embed(title="Sorry, invalid pseudo.", description="**Try again.**")
            embed.set_footer(text=f"Host : {host}", icon_url=host.avatar_url)
            bot_msg = await channel.send(embed=embed)

        elif opponent_mention == host_mention or opponent_mention == f"<@!{client.user.id}>":
            embed = discord.Embed(title="Sorry, you can't play against yourself or me.", description="**Try again.**")
            embed.set_footer(text=f"Host : {host}", icon_url=host.avatar_url)
            bot_msg = await channel.send(embed=embed)

        elif "<@" in opponent:
            timeout = 10
            timer = 0
            embed = discord.Embed(title=f"Shifumi Match Invitation !", description=f"**{opponent}, accept the match with : ✅, decline with : ❌**\nYou still have **{timeout}secs**.")
            embed.set_footer(text=f"Host : {host}", icon_url=host.avatar_url)
            bot_msg = await channel.send(embed=embed)
            for emoji in YES_NO:
                await bot_msg.add_reaction(emoji)

            def check_yes_no_opponent(reaction, user):
                return f"<@!{user.id}>" == opponent_mention and (str(reaction)in YES_NO)

            while timeout != 0:
                try:
                    reaction, user = await client.wait_for("reaction_add", timeout=1, check=check_yes_no_opponent)
                    if reaction != None and user != None:
                        if str(reaction) == YES_NO[0]:
                            game_continue = True
                        else:
                            game_continue = False
                        break
                except asyncio.TimeoutError:
                    if timer == 9:
                        game_continue = False
                    else:
                        timer += 1
                        pass
                timeout -= 1
                if timeout == 0:
                    embed = discord.Embed(title=f"Shifumi Match Invitation !", description="Invitation has expired.")
                    embed.set_footer(text=f"Host : {host}", icon_url=host.avatar_url)
                    await bot_msg.edit(embed=embed)
                    await bot_msg.clear_reactions()
                    return
                else:
                    embed = discord.Embed(title=f"Shifumi Match Invitation !", description=f"**{opponent}, accept the match with : ✅, decline with : ❌**\nYou still have **{timeout}secs**.")
                    embed.set_footer(text=f"Host : {host}", icon_url=host.avatar_url)
                    await bot_msg.edit(embed=embed)

            if game_continue is False:
                await bot_msg.clear_reactions()
                embed = discord.Embed(title=f"Shifumi Match Invitation Refused !")
                embed.set_footer(text=f"Host : {host}", icon_url=host.avatar_url)
                await bot_msg.edit(embed=embed)
                return

            else:
                game_end = False
                while not game_end:
                    await bot_msg.clear_reactions()
                    decount_until_start = 4
                    timer = 0
                    embed = discord.Embed(title=f"Shifumi Match Invitation Accepted !", description=f"**Game will start soon...**")
                    embed.set_footer(text=f"Host : {host}", icon_url=host.avatar_url)
                    await bot_msg.edit(embed=embed)
                    while decount_until_start != 0:
                        time.sleep(1)
                        decount_until_start -= 1
                        if decount_until_start > 1:
                            indications = ":yellow_circle: **WAIT TO REACT...**:yellow_circle:"
                        elif decount_until_start == 1:
                            indications = ":orange_circle: **READY ??** :orange_circle:"
                        elif decount_until_start == 0:
                            indications = ":red_circle: REACT NOW ! :red_circle:"
                        embed = discord.Embed(title=f"Shifumi Match !", description=f"**Choose reaction you want when counter is equal to 0\n🤚 = Paper\n👊 = Rock\n✌ = Scissors\n**")
                        embed.add_field(name=f"Counter : {decount_until_start}", value=f"**{indications}**")
                        embed.set_footer(text=f"Host : {host}", icon_url=host.avatar_url)
                        await bot_msg.edit(embed=embed)

                        if decount_until_start == 1:
                            for emoji in CHOICE:
                                await bot_msg.add_reaction(emoji)

                        elif decount_until_start == 0:
                            def check_test(reaction, user):
                                return str(reaction) in CHOICE and user.id == host.id or user.id == opponent_id

                            first_timer = 0
                            while first_timer <= 5:
                                try:
                                    reaction_1st, user_1st = await client.wait_for('reaction_add', timeout=0.005, check=check_test)
                                    if str(reaction_1st) in CHOICE:
                                        if user_1st.id == host.id:
                                            host_choice = str(reaction_1st)
                                        elif user_1st.id == opponent_id:
                                            opponent_choice = str(reaction_1st)
                                    second_timer = 0
                                    while second_timer <= 2:
                                        try:
                                            reaction_2nd, user_2nd = await client.wait_for('reaction_add', timeout=0.005, check=check_test)
                                            if str(reaction_2nd) in CHOICE:
                                                if user_2nd.id == host.id:
                                                    host_choice = str(reaction_2nd)
                                                elif user_2nd.id == opponent_id:
                                                    opponent_choice = str(reaction_2nd)
                                                
                                                #If Draw : End game    
                                                if str(reaction_1st) != str(reaction_2nd):
                                                    game_end = True
                                            break
                                        except asyncio.TimeoutError:
                                            second_timer =+ 0.005
                                    break
                                except asyncio.TimeoutError:
                                    first_timer += 0.005


                            if first_timer >= 5:
                                await bot_msg.clear_reactions()
                                embed = discord.Embed(title=f"Shifumi Match Has Expired", description=f"Too slow, nobody has won.")
                                embed.set_footer(text=f"Host : {host}", icon_url=host.avatar_url)
                                await bot_msg.edit(embed=embed)
                                return

                            else:
                                await bot_msg.clear_reactions()
                                result = how_has_won(host_choice, host_mention, opponent_choice, opponent_mention, "vs")
                                embed = discord.Embed(title=f"Shifumi Match Result", description=f"{result}\n------------------------------\n{host_mention} : {host_choice}\n{opponent_mention} : {opponent_choice}")
                                embed.set_footer(text=f"Host : {host}", icon_url=host.avatar_url)
                                await bot_msg.edit(embed=embed)
                                if game_end:
                                    return
                                else:
                                    time.sleep(2)
                                
                        

    elif message.content.startswith("$start"):
        timeout = 5
        while timeout >= 0:
            embed = discord.Embed(title=f"Shifumi Match Solo", description=f"{host_mention}, are you ready ?\nGame starts in **{timeout}secs**")
            embed.set_footer(text=f"Player : {host}", icon_url=host.avatar_url)
            if timeout == 0:
                embed = discord.Embed(title=f"Shifumi Match Solo", description=f"{host_mention}, game starts now !")
                embed.set_footer(text=f"Player : {host}", icon_url=host.avatar_url)
            if timeout == 5:
                bot_msg = await channel.send(embed=embed)
            else:
                await bot_msg.edit(embed=embed)
            time.sleep(1)
            timeout -= 1

        game_end = False
        while not game_end:
            decount_until_start = 3
            while decount_until_start != 0:
                time.sleep(1)
                decount_until_start -= 1
                if decount_until_start > 1:
                    indications = ":yellow_circle: **WAIT TO REACT...**:yellow_circle:"
                elif decount_until_start == 1:
                    indications = ":orange_circle: **READY ??** :orange_circle:"
                elif decount_until_start == 0:
                    indications = ":red_circle: REACT NOW ! :red_circle:"
                embed = discord.Embed(title=f"Shifumi Match !",description=f"**Choose reaction you want when counter is equal to 0\n🤚 = Paper\n👊 = Rock\n✌ = Scissors\n**")
                embed.add_field(name=f"Counter : {decount_until_start}", value=f"**{indications}**")
                embed.set_footer(text=f"Player : {host}", icon_url=host.avatar_url)
                await bot_msg.edit(embed=embed)

                if decount_until_start == 1:
                    for emoji in CHOICE:
                        await bot_msg.add_reaction(emoji)

                elif decount_until_start == 0:
                    def check_test(reaction, user):
                        return str(reaction) in CHOICE and user.id == host.id

                    try:
                        host_choice, player = await client.wait_for('reaction_add', timeout=3.0, check=check_test)
                        

                        await bot_msg.clear_reactions()
                        bot_choice = get_random_choice()
                        if "100%winrate" in [role.name for role in player.roles]:
                            if str(host_choice) == "🤚":
                                bot_choice = "👊"
                            elif str(host_choice) == "👊":
                                bot_choice = "✌"
                            elif str(host_choice) == "✌":
                                bot_choice = "🤚"

                        if str(host_choice) != str(bot_choice):
                            game_end = True
                        result = how_has_won(str(host_choice), host_mention, bot_choice, "Bot", "solo")
                        embed = discord.Embed(title=f"Shifumi Match Result", description=f"{result}\n------------------------------\n{host_mention} : {host_choice}\n{client.user.mention} : {bot_choice}")
                        embed.set_footer(text=f"Player : {host}", icon_url=host.avatar_url)
                        await bot_msg.edit(embed=embed)
                        if game_end:
                            return

                    except asyncio.TimeoutError:
                        await bot_msg.clear_reactions()
                        embed = discord.Embed(title=f"Shifumi Match Has Expired",description=f"**You took too much time to react... Try again.**")
                        embed.set_footer(text=f"Player : {host}", icon_url=host.avatar_url)
                        await bot_msg.edit(embed=embed)
                        return
            

client.run(DISCORD_BOT_TOKEN)