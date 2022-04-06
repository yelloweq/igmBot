import lightbulb
import hikari
import os

bot = lightbulb.BotApp(token=os.environ['BOT_TOKEN'],
                       prefix='gm.',
                       help_slash_command=True,
                       default_enabled_guilds=os.environ['DEFAULT_GUILD_ID']) 


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

