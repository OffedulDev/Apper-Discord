# Utility Module
import interactions
from bot_token import Bot_Token

Client = interactions.Client(token=Bot_Token, intents=interactions.Intents.GUILD_MESSAGE_CONTENT | interactions.Intents.GUILDS)

## Discord Utilities

class colors:
    default = 0
    teal = 0x1abc9c
    dark_teal = 0x11806a
    green = 0x2ecc71
    dark_green = 0x1f8b4c
    blue = 0x3498db
    dark_blue = 0x206694
    purple = 0x9b59b6
    dark_purple = 0x71368a
    magenta = 0xe91e63
    dark_magenta = 0xad1457
    gold = 0xf1c40f
    dark_gold = 0xc27c0e
    orange = 0xe67e22
    dark_orange = 0xa84300
    red = 0xe74c3c
    dark_red = 0x992d22
    lighter_grey = 0x95a5a6
    dark_grey = 0x607d8b
    light_grey = 0x979c9f
    darker_grey = 0x546e7a
    blurple = 0x7289da
    greyple = 0x99aab5
async def get_channel(id: int):
    try:
        return interactions.Channel(**await Client._http.get_channel(id), _client=Client._http)
    except:
        print("Error getting channel")
        return None

## Discord (sub)Classes

class Embed:
    def __init__(self, title="None", description="None", color=0x336EFF):
        self.title = title
        self.description = description
        self.color = color
        self.embed = interactions.Embed(title=self.title, description=self.description, color=self.color)

    def add_field(self, name="None", value="None", inline=True):
        self.embed.add_field(name=name, value=value, inline=inline)

class Modal:
    def __init__(self, title, custom_id):
        self.title = title
        self.custom_id = custom_id
        self.components = []

    def add_textinput(self, style=interactions.TextStyleType.SHORT, label="None", custom_id="None", min_length=0, max_length=100):
        self.components.append(interactions.TextInput(
                style=style,
                label=label,
                custom_id=custom_id,
                min_length=min_length,
                max_length=max_length,
            )
        )       

    def build_modal(self):

        return interactions.Modal(
            title=self.title,
            custom_id=self.custom_id,
            components=self.components
        )

class ActionRow:
    def __init__(self):
        self.actions = []

    def add_button(self, callback, label="None", custom_id="", style=interactions.ButtonStyle.PRIMARY):
        self.actions.append(interactions.Button(
                style=style,
                label=label,
                custom_id=custom_id
            )
        )
        @Client.component(custom_id)
        async def execute(ctx):
            await callback(ctx)

    def build_row(self):
        return interactions.ActionRow(components=self.actions)

## Bot Classes 
class Application:
    def __init__(self, guild, app_name, app_fields):
        self.app_name = app_name
        self.app_fields = app_fields
        self.guild = guild
        
        @Client.modal(self.app_name)
        async def ModalCallback(ctx, field1, field2, field3, field4, field5):
            _ResEmbed = Embed(title="Application Recived from " + ctx.author.username + "🎭", description="Recived application, review the parameters.", color=colors.dark_gold)

            fields = [field1, field2, field3, field4, field5]
            for field in fields:
                _ResEmbed.add_field(name="Question #" + str(fields.index(field)), value=field, inline=False)

        AppModal = Modal(title=self.app_name, custom_id=self.app_name.lower())
        for field in app_fields: AppModal.add_textinput(label=field, custom_id=str(app_fields.index(field)))
        self.AppModal = AppModal.build_modal()

    async def sendActionRow(self, ctx):
        StartEmbed = Embed(title="Starting Application ✅", 
                           description="You should be prompted with your application in a moment. Thanks for choosing Apper!", 
                           color=colors.green)
        
        ActionRowEmbed = Embed(title=self.app_name + " Application", 
                               description="Press the button below to start this application, under here you can find every question asked in the application.", 
                               color=colors.teal)

        for Field in self.app_fields: ActionRowEmbed.add_field(name="Question #" + str(self.app_fields.index(Field)), value=Field, inline=False)

        async def startApplication(ctx):
            await ctx.popup(self.AppModal)
            await ctx.send(embeds=StartEmbed.embed)

        _ActionRow = ActionRow()
        _ActionRow.add_button(callback=startApplication, 
                              label="Start Application (" + self.app_name + ")", 
                              custom_id=self.app_name.lower())

        await ctx.send(embeds=ActionRowEmbed.embed, components=_ActionRow.build_row())
        


                    