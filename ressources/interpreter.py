# import discord
# from discord.ext import commands

# ICommands: list = ["test", "lol", "eheh"]


# class IContext:

#     def __init__(self, bot, message: discord.Message):
#         self.bot = bot
#         self.message = message
#         self.channel = message.channel
#         self.author = message.author
#         self.guild = message.guild
#         self.content = message.content


# class ICommand:

#     def __init__(self, component: str):
#         self.full_component: str = component
#         self.components: list = component.split(" ")
#         self.arguments: list = self.components[1:]
#         self.validation_result: dict = self.check_validity()

#     def check_validity(self):
#         if not self.components[0].startswith("/"):
#             return {"error": "Une commande doit commencer par '/'."}
#         command = self.components[0][1:]
#         if command not in ICommands:
#             return {"error": f"La commande {command} n'est pas reconnue."}

#         return None

#     def is_valid(self):
#         return self.validation_result is None

#     def get_error(self):
#         return self.validation_result


# class Interpreter(commands.Cog):

#     def __init__(self, bot):
#         self.bot = bot
#         self.salon_id = 1280127733157855357

#     @commands.Cog.listener()
#     async def on_message(self, message):
#         await self.bot.wait_until_ready()
#         if message.author == self.bot.user:
#             return
#         if message.channel.id == self.salon_id:
#             context = IContext(self.bot, message)
#             await self.interprete(context, message.content)

#     async def interprete(self, ctx: IContext, component: str):
#         command = ICommand(component)
#         channel = self.bot.get_channel(self.salon_id)
#         if command.is_valid():
#             command_name = command.components[0][1:]
#             method_name = f"ICommand_{command_name}"
#             method = getattr(self, method_name, None)
#             if method:
#                 await method(ctx, command.arguments)
#             else:
#                 await channel.send(
#                     f"La commande {command_name} n'a pas de méthode associée.")
#         else:
#             error_message = command.get_error()
#             await channel.send(f"Erreur: {error_message['error']}")

#     # Enregistrement des commandes
#     async def ICommand_test(self, ctx: IContext, arguments: list):
#         await ctx.channel.send(f"TEST {arguments}")

#     async def ICommand_lol(self, ctx: IContext, arguments: list):
#         await ctx.channel.send(f"LOL : {arguments}")


# async def setup(bot):
#     await bot.add_cog(Interpreter(bot))
