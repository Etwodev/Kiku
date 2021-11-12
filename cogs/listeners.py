import discord, asyncio
from discord.ext import commands, tasks
from utils import referencing, startup, definitions, handle
from discord_components import DiscordComponents, Button, Select, SelectOption

class listeners(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.embeds = definitions.embeded()
        self.config = startup.get("config.json")
        self.poll_emojis = ["✅", "♻️", "❌"]

    @tasks.loop(minutes=10)
    async def status_task(self):
        await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"the Info in {len(self.client.guilds)} servers!"))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, err):
        print(f'User "{ctx.author.id}" Triggered Error: "{err}"')

        if isinstance(err, commands.CommandOnCooldown):
            msg = await ctx.reply(embed=self.embeds.CommandOnCooldown(err))
            await msg.delete(delay=3)

        elif isinstance(err, discord.errors.Forbidden):
            await ctx.reply(embed=self.embeds.Forbidden())

        elif isinstance(err, commands.TooManyArguments):
            await ctx.reply(embed=self.embeds.TooManyArguments())

        elif isinstance(err, commands.MaxConcurrencyReached):
            await ctx.reply(embed=self.embeds.MaxConcurrencyReached())

        elif isinstance(err, commands.MissingRequiredArgument):
            await ctx.reply(embed=self.embeds.MissingRequiredArgument(err))

        elif isinstance(err, commands.MessageNotFound):
            await ctx.reply(embed=self.embeds.MessageNotFound())

        elif isinstance(err, commands.ChannelNotFound):
            await ctx.reply(embed=self.embeds.ChannelNotFound())

        elif isinstance(err, commands.NSFWChannelRequired):
            await ctx.reply(embed=self.embeds.NSFWChannelRequired())

        elif isinstance(err, commands.NoPrivateMessage):
            await ctx.reply(embed=self.embeds.NoPrivateMessage())

        elif isinstance(err, commands.CommandNotFound):
            pass

        elif isinstance(err, commands.PartialEmojiConversionFailure):
            pass

        else:
            raise err


    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        try:
            to_send = sorted([chan for chan in guild.channels if chan.permissions_for(guild.me).send_messages and isinstance(chan, discord.TextChannel)], key=lambda x: x.position)[0]
        except IndexError:
            pass
        else:
            await to_send.send(embed=(self.embeds.on_guild_join()))
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.status_task.start() # This is not a bug. vscode just is stupid.
        DiscordComponents(self.client)
        user = await self.client.fetch_user(self.config.owner)
        await user.send(embed=(self.embeds.on_ready(self.client)))

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.content.lower().startswith("k!afk") or ctx.author.bot is True:
            return
        for mention in ctx.mentions:
            x = referencing.fetch_handler(mention)
            if x[3] == 1:
                if mention.id != ctx.author.id:
                    await ctx.reply(embed=self.embeds.on_message(mention, x[4]))
        x = referencing.fetch_handler(ctx.author)
        if x[0] == str(ctx.author.id):
            if x[3] == 1:
                referencing.update_handler(ctx.author, "User is afk.", 0)
                await ctx.reply(embed=discord.Embed(title="Welcome back!", description="I have removed your afk.", color=0xc83737))
                return

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        try:
            if interaction.message.author == self.client.user:
                if interaction.component.label == "Delete":
                    await interaction.message.delete()
                elif interaction.message.mentions[0] == interaction.user and interaction.custom_id == "pollend" and interaction.message.embeds[0].footer.text == "Poll in progress...":
                    raw = referencing.poll_end_handler(interaction)
                    img, name = await handle.poll_handler(raw)
                    await interaction.channel.send(embed=(self.embeds.end_poll(raw, (interaction.message.embeds[0].description), name)), file=img)
                    await interaction.message.delete()
                elif interaction.message.embeds[0].footer.text == "Poll in progress..." and interaction.message.mentions[0] == interaction.user and interaction.custom_id in ["Yes", "No", "Abstain"]:
                    referencing.poll_handler(interaction.user, interaction)
                    await interaction.respond(type=4, content=f"Your vote has been counted!")
            else:
                return
        except IndexError:
            raw = referencing.poll_end_handler(interaction)
            await interaction.message.delete()

def setup(client):
    client.add_cog(listeners(client))