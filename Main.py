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

@Client.command(
    name="create",
    description="Create a new application.",
    options=[
        interactions.Option(
            name="appname",
            description="The name of the application",
            required=True,
            type=interactions.OptionType.STRING
        ),
        interactions.Option(
            name="field0",
            description="Field of the application",
            required=True,
            type=interactions.OptionType.STRING
        ),
        interactions.Option(
            name="field1",
            description="Field of the application",
            required=True,
            type=interactions.OptionType.STRING
        ),
        interactions.Option(
            name="field2",
            description="Field of the application",
            required=True,
            type=interactions.OptionType.STRING
        ),
        interactions.Option(
            name="field3",
            description="Field of the application",
            required=True,
            type=interactions.OptionType.STRING
        ),
        interactions.Option(
            name="field4",
            description="Field of the application",
            required=True,
            type=interactions.OptionType.STRING
        )
    ]
)
async def CreateApplication(ctx, appname, field0, field1, field2, field3, field4):
    fields = []
    fields = [field0, field1, field2, field3, field4]
    async def confirmCreation(ctx):
        App = Application(guild=0, app_name=appname, app_fields=fields)
        Applications.append(App)

        await ctx.edit(embeds=_SuccessEmbed.embed, components=[])
        return
        
    async def discardCreation(ctx):
        await ctx.edit("Ignoring changes, discarding application.", components=[])
        return

    for field in fields: _ReviewEmbed.add_field(name=f"Question #{fields.index(field)}", value=field, inline=False)
    _ActionRow = ActionRow()
    _ActionRow.add_button(callback=discardCreation, label="Discard ❌", custom_id="discard", style=interactions.ButtonStyle.DANGER)
    _ActionRow.add_button(callback=confirmCreation, label="Confirm ✅", custom_id="accept", style=interactions.ButtonStyle.SUCCESS)
    await ctx.send(embeds=_ReviewEmbed.embed, components=_ActionRow.build_row())

@Client.command(
    name="sendappplication",
    description="Send appplication",
    options=[
        interactions.Option(
            name="appname",
            required=True,
            description="The name of the application.",
            type=interactions.OptionType.STRING
        )
    ]
)
async def SendAppplication(ctx, appname):
    searchApp = None
    for app in Applications:
        if app.app_name == appname:
            searchApp = app
            break

    if searchApp == None: await ctx.send("Bad argument."); return
    await searchApp.sendActionRow(ctx)
    return

Client.start()