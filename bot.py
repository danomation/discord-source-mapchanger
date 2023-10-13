import discord
from discord.ext import commands
import os

#declare your variables
discord-token = your discord bot token
discord-channel = your discord channel id
intents = intents = discord.Intents.all()
bot = discord.Bot(intents=intents)
maplist = "/path/to/your/maplist.txt"
mapcycle = "/path/to/your/mapcycle.txt"

#read your files
def read_file(filename):
    with open(filename, "r") as f:
        lines = [line.rstrip() for line in f]
    return lines

class MapSelection(discord.ui.Select):
    def __init__(self, options, current_map, placeholder, line_idx): 
        select_options = [discord.SelectOption(label=option) for option in options]
        discord.ui.Select.__init__(self, placeholder=placeholder, min_values=1, max_values=1, options=select_options)
        self.current_value = current_map
        self.line_idx = line_idx 
    async def callback(self, interaction: discord.Interaction):
        self.current_value = interaction.data['values'][0]
        with open(mapcycle, "r") as f:
            lines = f.readlines()
        lines[self.line_idx] = self.current_value + "\n"
        with open(mapcycle, "w") as f:
            f.writelines(lines)
        await interaction.response.send_message(f"New map selected: {self.current_value}")

#create the slash command
@bot.slash_command(description="select a map")
async def select_map(ctx):
    if ctx.channel.id == discord-channel:
        map_options = read_file(maplist)
        current_mapcycle = read_file(mapcycle)

        view = discord.ui.View()
        counter = 0
        #this looks weird but I had to iterate because there's a max of like 20 options per select and 5 selects per message
        for i, map_name in enumerate(current_mapcycle):
            related_options = [option for option in map_options if map_name[:10] in option]

            if related_options:
                select = MapSelection(options=related_options, placeholder=map_name, current_map=map_name, line_idx=i)
                view.add_item(select)
                counter += 1
                if counter % 5 == 0:
                    await ctx.respond(view=view, ephemeral=True)
                    view.clear_items()
                    counter = 0
        if counter != 0:
            await ctx.respond(view=view, ephemeral=True)

bot.run(discord-token)
