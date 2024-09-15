import discord
from discord import app_commands
from discord.ext import commands, tasks
from itertools import cycle

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())

# Action au démarrage du bot
@bot.event
async def on_ready():
    print("Connected !")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="(∪｡∪)｡｡｡zzZ"))
    try:
        synced_commands = await bot.tree.sync()
        print(f"Synced {len(synced_commands)} commands.")
    except Exception as e:
        print("An error with syncing application commands has occured: ", e)

# Commandes
@bot.tree.command(name="ping", description="Play a game of ping-pong against the bot.")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"{interaction.user.mention} Pong! 🏓")

# -----------------------------------------------------------------------------------------

@bot.tree.command(name="announcement", description="Make a announcement.")
@app_commands.describe(mention="The role to mention", announcement="The text of the announcement.")
async def announcement(interaction: discord.Interaction, mention: discord.Role, announcement: str):
    if interaction.user.guild_permissions.administrator:
        announcement_message = f"{mention.mention}|\n \n {announcement}"

        await interaction.response.send_message(announcement_message)
    else:
        await interaction.response.send_message("You doesn't have the permission to make announcements", ephemeral=True)

# -----------------------------------------------------------------------------------------

@bot.tree.command(name="partnership", description="Make a partnership with another Discord server.")
@app_commands.describe(mention="The role to mention", responsible="The responsible of the partnership", representative="The representative of the other server", message="The message of the partnership")
async def partnership(interaction: discord.Interaction, mention: discord.Role, responsible: discord.Member, representative: discord.Member, message: str):
    if interaction.user.guild_permissions.administrator:
        embed_message = discord.Embed(
            title="__**Partenariat**__",
            color=discord.Color.dark_gray()
        )
        
        embed_message.add_field(name="**Représentant:**", value=f"{representative.mention}", inline=False)
        embed_message.add_field(name="**Responsable:**", value=f"{responsible.mention}", inline=False)
        
        await interaction.response.send_message(
            content=f"{mention.mention} |\n\n{message}",
            embed=embed_message
        )
    else:
        await interaction.response.send_message(
            "You don't have permission to make announcements.",
            ephemeral=True
        )

# Récupération du token
with open("Chillr-token.txt") as file:
    token = file.read()

# Démarrage du bot
bot.run(token)