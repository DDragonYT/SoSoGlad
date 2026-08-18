import discord

def gen_error(text):
    embed = discord.Embed(
        title = text,
        color=discord.Colour.red()
    )
    return embed

def target_from_message(self, message):
    command = str(message.content).split(" ")
    target = None
    if len(command) > 1:
        target = command[1]
        if "<" in target:
            user_id = int(target.strip("<>@"))
            target = self.get_user(user_id)
        else:
            target = message.author
    else:
        target = message.author
    return target