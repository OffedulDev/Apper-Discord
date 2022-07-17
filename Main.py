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



# Setup Command


Client.start()