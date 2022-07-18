from click import option
from Utility import *
import interactions

# Command Structure
# Command(Name="lowercasename", Desc="description", Admin=True/False, CallBack=Function)
# Command.add_option(Name="lowercasename", Desc="description", Required=True/False, Option_Type=interactions.OptionType.STRING)

# Action Row Structure
# ActionRow()
# ActionRow.add_button(label="What", custom_id="uniqueid", callback=Function, style=interactions.ButtonStyle.PRIMARY)

# Modal Structure
# Modal(title="Title", Callback=Function)
# Modal.add_textinput(label="None", custom_id="None")

# Embed Structure
# Embed(title="Title", description="Description", color=hexadecimalcolor)
# Embed.add_field(name="None", value="None", inline=True/False)
# Embed.embed


# Temp Var
Applications = []

# Create Command
_SuccessEmbed = Embed(title="Application Created Correctly ✅", 
                    description="Your application was create correctly, you can now send an embed to fill it with /sendApplication",
                    color=colors.green)
_ReviewEmbed = Embed(title="Application Review 🔋", 
                    description="Please review the application and the fields that you provided. Make sure that it all fits your needs and then press the Green button, otherwhise just press the red button and try again.",
                    color=colors.magenta)

async def CreateApplication(ctx, options):
    appname = options['appname']
    app_name = appname
    fields = [options['field0'], options['field1'], options['field2'], options['field3'], options['field4']]
    async def confirmCreation(ctx):
        App = Application(guild=ctx.get_guild().id, app_name=app_name, app_fields=fields)
        Applications.append(App)

        await ctx.send(embeds=_SuccessEmbed.embed)
        return
        
    async def discardCreation(ctx):
        await ctx.send("Ignoring changes, discarding application.")
        return

    _ActionRow = ActionRow()
    _ActionRow.add_button(callback=discardCreation, label="Discard ❌", custom_id="discard" + ctx.get_guild().id, style=interactions.ButtonStyle.DANGER)
    _ActionRow.add_button(callback=confirmCreation, label="Confirm ✅", custom_id="accept" + ctx.get_guild().id, style=interactions.ButtonStyle.DANGER)
    await ctx.send(embeds=_ReviewEmbed.embed, components=_ActionRow)


CreateCommand = Command(Name="create", Desc="Create a new application.", Admin=True, CallBack=CreateApplication)
CreateCommand.add_option(Name="appname", Desc="Name of the application.", Required=True)
for i in range(5): CreateCommand.add_option(Name=f"field{i}", Desc=f"Field of the Application. {i}" , Required=True)
CreateCommand.build_command()

Client.start()