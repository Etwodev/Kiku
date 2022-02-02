import discord, asyncio, ast
from discord import message
from discord.ext import commands, tasks
from discord.ext.commands import context
import utils.config, utils.embeds.errors, utils.embeds.listeners, utils.referencing, utils.threading, utils.api
from discord_components import DiscordComponents, Button, Select, SelectOption

class listeners(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.referencing = utils.referencing
        self.errors_embeds = utils.embeds.errors
        self.listeners_embeds = utils.embeds.listeners
        self.threading = utils.threading
        self.api = utils.api
        self.config = utils.config.get("config.json")

    @tasks.loop(minutes=5)
    async def status_task(self):
        await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"the Info in {len(self.client.guilds)} servers!"))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, err):
        print(f'User "{ctx.author.id}" Triggered Error: "{err}"')
        embed = self.errors_embeds.ErrorsEmbed(ctx=ctx, err=err)

        if isinstance(err, commands.UserInputError):
            embed.UserInputError()

        elif isinstance(err, commands.CommandOnCooldown):
            embed.CommandOnCooldown()

        elif isinstance(err, discord.errors.Forbidden):
            embed.Forbidden()

        elif isinstance(err, commands.TooManyArguments):
            embed.TooManyArguments()

        elif isinstance(err, commands.MaxConcurrencyReached):
            embed.MaxConcurrencyReached()

        elif isinstance(err, commands.MissingRequiredArgument):
            embed.MissingRequiredArgument()

        elif isinstance(err, commands.MessageNotFound):
            embed.MessageNotFound()

        elif isinstance(err, commands.ChannelNotFound):
            embed.ChannelNotFound()

        elif isinstance(err, commands.NSFWChannelRequired):
            embed.NSFWChannelRequired()

        elif isinstance(err, commands.NoPrivateMessage):
            embed.NoPrivateMessage()
        
        elif isinstance(err, commands.errors.BadArgument):
            embed.BadArgument()

        elif isinstance(err, commands.MissingPermissions):
            embed.MissingPermissions()

        else:
            embed.UnknownDiscordError()
            raise err

        await ctx.reply(embed=embed.embed)


    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        try:
            to_send = sorted([chan for chan in guild.channels if chan.permissions_for(guild.me).send_messages and isinstance(chan, discord.TextChannel)], key=lambda x: x.position)[0]
        except IndexError:
            pass
        else:
            embed = self.listeners_embeds.ListenersEmbed()
            embed.OnGuildEmbed(self.client, guild)
            await to_send.send(embed=embed.embed)
    
    @commands.Cog.listener()
    async def on_ready(self):
        if not self.status_task.is_running():
            self.status_task.start()
        DiscordComponents(self.client)
        embed = self.listeners_embeds.ListenersEmbed()
        embed.OnReadyEmbed(client=self.client)
        for owner in self.config.owners:       
            user = await self.client.fetch_user(owner)
            await user.send(embed=embed.embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        fields = {}
        if message.content.lower().startswith(self.config.prefix[0] + "afk") or message.author.bot is True:
            return
        elif message.mentions:
            for i, mention in enumerate(message.mentions):
                if i > 5:
                    break
                else:
                    profile = self.referencing.ProfileHeader(mention)
                    if profile.is_afk():
                        if mention.id != message.author.id:
                            fields[mention.name] = profile.afk_message
        profile = self.referencing.ProfileHeader(message.author)
        if profile.is_afk():
            profile.remove_afk()
            fields[message.author.name] = "Welcome back, I removed your afk."
        if fields.keys():
            embed = self.listeners_embeds.ListenersEmbed()
            embed.MessageAFKEmbed(message=message, fields=fields)
            await message.reply(embed=embed.embed)
        else:
            return

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        if interaction.message.author != self.client.user:
            return
        elif not interaction.message.embeds:
            await interaction.message.delete()
            await interaction.respond(type=4, content="The embed was removed, deleting now.")
        elif interaction.component.label == "I do" and interaction.user.id == list(ast.literal_eval(interaction.custom_id).values())[0]:
            profile = self.referencing.ProfileHeader(interaction.user)
            married = self.referencing.ProfileHeader(interaction.message.mentions[0])
            if profile.set_marriage(married):
                embed = self.listeners_embeds.ListenersEmbed()
                embed.ButtonMarriageYesEmbed(url=await self.api.tenor("anime+marriage", 8), user_a=profile.user, user_b=married.user)
                await interaction.channel.send(embed=embed.embed)
                await interaction.message.delete()
            else:
                await interaction.message.delete()
                raise commands.UserInputError("One user is already married! I mean, you tried...")
        elif interaction.component.label == "Denied" and interaction.user.id == list(ast.literal_eval(interaction.custom_id).values())[0]:
            embed = self.listeners_embeds.ListenersEmbed()
            embed.ButtonMarriageNoEmbed(url=await self.api.tenor("anime+sad", 8), user=interaction.message.mentions[0])
            await interaction.channel.send(embed=embed.embed)
            await interaction.message.delete()
              
        elif interaction.component.label == "Accept" and interaction.user.id == list(ast.literal_eval(interaction.custom_id).values())[0]:
            profile = self.referencing.HaremHeader(interaction.user)
            owner = self.referencing.HaremHeader(interaction.message.mentions[0])
            if owner.add(profile):
                embed = self.listeners_embeds.ListenersEmbed()
                embed.ButtonHaremYesEmbed(url=await self.api.tenor("anime+marriage", 8), user_a=profile.user, user_b=owner.user)
                await interaction.channel.send(embed=embed.embed)
                await interaction.message.delete()
            else:
                await interaction.message.delete()
                raise commands.UserInputError("User is already in a harem or the harem has reached the max users!")
        elif interaction.component.label == "Reject" and interaction.user.id == list(ast.literal_eval(interaction.custom_id).values())[0]:
            embed = self.listeners_embeds.ListenersEmbed()
            embed.ButtonHaremNoEmbed(url=await self.api.tenor("anime+sad", 8), user=interaction.message.mentions[0])
            await interaction.channel.send(embed=embed.embed)
            await interaction.message.delete()
        elif interaction.component.label == "Delete":
            await interaction.message.delete()
            await interaction.respond(type=4, content="Deleted!")
        elif interaction.message.mentions[0] == interaction.user and interaction.component.label == "End":
            raw = self.referencing.poll_handler_end(interaction=interaction)
            file, file_name = await self.threading.poll_handler(raw)
            embed = self.listeners_embeds.ListenersEmbed()
            embed.ButtonPollEmbed(message=interaction.message.embeds[0].description, file_name=file_name, results=raw)
            await interaction.channel.send(embed=embed.embed, file=file)
            await interaction.message.delete()
            await interaction.respond(type=4, content="Poll ended.")
        elif interaction.component.label in ["Yes", "No", "Abstain"]:
            self.referencing.poll_handler(user=interaction.user, interaction=interaction)
            await interaction.respond(type=4, content="Your vote has been counted!")


def setup(client):
    client.add_cog(listeners(client))