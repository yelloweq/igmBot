import lightbulb
import hikari
import os

from igm import GUILD_ID

with open("./secrets/token") as f:
    _token = f.read().strip()


bot = lightbulb.BotApp(token=_token,
                       prefix='ui.',
                       default_enabled_guilds=GUILD_ID,
                       help_slash_command=True) 


@bot.listen()
async def starting_load_extensions(_: hikari.StartingEvent) -> None:
    """Load extensions when Bot starts."""
    bot.load_extensions_from("./igm/extensions")


@bot.command
@lightbulb.command("ping", "Returns bot's latency")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def ping(ctx: lightbulb.Context) -> None:
   await ctx.respond(f"Pong! Latency: {bot.heartbeat_latency*1000:.2f}ms")


def run() -> None:
    if os.name != "nt":
        import uvloop
        uvloop.install()
    
    bot.run()

