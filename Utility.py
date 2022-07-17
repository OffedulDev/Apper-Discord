from msilib.schema import AdminExecuteSequence
from time import sleep
from types import NoneType
import interactions
from bot_token import Bot_Token

Client = interactions.Client(token=Bot_Token, intents=interactions.Intents.ALL)

async def get_channel(id: int):
    try:
        return interactions.Channel(**await Client._http.get_channel(id), _client=Client._http)
    except:
        print("Error getting channel")
        return None

class Embed:
    def __init__(self, title="None", description="None", color=0x336EFF):
        self.title = title
        self.description = description
        self.color = color
        self.embed = interactions.Embed(title=self.title, description=self.description, color=self.color)

    def add_field(self, name="None", value="None", inline=True):
        self.embed.add_field(name=name, value=value, inline=inline)

class Modal:
    def __init__(self, title, custom_id, callback=None):
        self.title = title
        self.custom_id = custom_id
        self.components = []
        self.callback = callback

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
        @Client.modal(self.custom_id)
        async def _answer(ctx, *answers):
            await self.callback(ctx, answers)

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

class Command:
    def __init__(self, CallBack, Name="", Desc="", Admin=False):
        self.name = Name
        self.desc = Desc
        self.options = []
        self.callback = CallBack
        self.admin = Admin

    def add_option(self, Name, Desc, Required, Option_Type):
        self.options.append(interactions.Option(
                name=Name,
                description=Desc,
                type=Option_Type,
                requried=Required
            )
        )

    def build_command(self):
        callback = self.callback
        @Client.command(
            name=self.name,
            description=self.desc,
            options=self.options,
            default_member_permissions=interactions.Permissions.ADMINISTRATOR if self.admin else interactions.Permissions.SPEAK
        )
        async def execute(ctx, **options):
            await callback(ctx, options)
