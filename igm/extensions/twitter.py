from typing import List
import hikari
import lightbulb
import tweepy
import os

with open("./secrets/twitter") as t:
    _twitter = t.read().splitlines()
    _twitter_api = _twitter[0]
    _twitter_secret_api = _twitter[1]
    _twitter_access = _twitter[2]
    _twitter_access_secret = _twitter[3]

authenticator = tweepy.OAuth1UserHandler(os.environ['TWITTER_API'], os.environ['TWITTER_API_SECRET'])
authenticator.set_access_token(os.environ['TWITTER_ACCESS'], os.environ['TWITTER_ACCESS_SECRET'])

api = tweepy.API(authenticator, wait_on_rate_limit=True)
#client = tweepy.Client(TWITTER_BEARER, wait_on_rate_limit=True)

plugin = lightbulb.Plugin("Twitter")

my_followers = []
streams = []
user_ids = []
tweets = []

class Listener(tweepy.Stream):
    def on_status(self, status):
        tweets.append(status)
        print(status.user.screen_name + ": " + status.text)

#async def get_tweets():
    

@plugin.command
@lightbulb.command("twitter", "Twitter Command Group")
@lightbulb.implements(lightbulb.PrefixCommandGroup, lightbulb.SlashCommandGroup)
async def twitter(ctx: lightbulb.Context) -> None:
    pass

@plugin.command
@lightbulb.command("say", "Twitter Command Group")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def twitter(ctx: lightbulb.Context) -> None:
    await ctx.respond('what?')

@twitter.child
@lightbulb.option('username', 'Twitter Handle', type=str)
@lightbulb.command("bind", "[Work in progress] Streams user's tweets in the channel.")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def bind(ctx: lightbulb.Context) -> None:
    if (ctx.options.username != "Iwus237"):
        streams.append(ctx.options.username)
        stream = Listener(
        os.environ['TWITTER_API'], os.environ['TWITTER_API_SECRET'],
        os.environ['TWITTER_ACCESS'], os.environ['TWITTER_ACCESS_SECRET']
        )
        for user in streams:
            user_ids.append(api.get_user(screen_name = user).id)
        
        await ctx.respond("current users tracked (id): " + str(user_ids))
        await ctx.respond("starting stream")
        stream.filter(follow=user_ids, threaded=True)
        
        while streams:
            for tweet in tweets:
                await ctx.respond(tweet.user.screen_name + " tweeted: " + tweet.text)
                tweets.remove(tweet)
    else:
        ctx.respond("The bot cannot follow itself!")

@twitter.child
@lightbulb.option('username', 'Twitter Handle', type=str)
@lightbulb.command("unbind", "[Work in progress] Stop streaming user tweets")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def unbind(ctx: lightbulb.Context) -> None:
    streams.pop(ctx.options.username)
    user_ids.pop(api.get_user(screen_name=ctx.option.username).id)

@twitter.child
@lightbulb.option('username', 'Twitter Handle', type=str)
@lightbulb.command('follow', 'Follows twitter user as bot')
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def follow(ctx: lightbulb.Context) -> None:
    api.create_friendship(screen_name = ctx.options.username)
    await ctx.respond("followed " + ctx.options.username)
    
@twitter.child
@lightbulb.option('username', 'Twitter Handle', type=str)
@lightbulb.command('unfollow', 'Unfollows twitter user as bot')
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def unfollow(ctx: lightbulb.Context) -> None:
    api.destroy_friendship(screen_name = ctx.options.username)
    await ctx.respond("unfollowed " + ctx.options.username)

@twitter.child
@lightbulb.command('list', 'Lists users the bot is following on Twitter.')
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def list(ctx: lightbulb.Context) -> None:
    for follower in api.get_friends(screen_name = 'Iwus237'):
        my_followers.append(follower.screen_name)
    await ctx.respond("I'm currently following: " + ", ".join(str(e) for e in my_followers))


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(bot.get_slash_command(plugin))
    