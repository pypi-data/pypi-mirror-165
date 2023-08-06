import ast
import importlib
import io
import json
import numbers
import sys
import discord
from discord.ext import commands

if len(sys.argv) < 3:
    sys.exit("usage: python -m clidpy [-i module...] your_token prefix cmd expr [cmd expr...]")
args = sys.argv[1:]

imports = {"discord": discord, "io": io, "json": json, "File": discord.File, "Embed": discord.Embed}
while args and args[0] == "-i":
    flag, name, *args = args
    imports[name] = importlib.import_module(name)

builtins = set(globals()) | set(dir(__builtins__)) | set(imports)
token, prefix, *other = args
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=prefix, intents=intents)

async def convert(ctx, result):
    # Convert to string or kwargs:
    if isinstance(result, numbers.Number):
        result = str(result)
    elif isinstance(result, discord.Embed):
        result = {"embed": result}
    elif isinstance(result, discord.File):
        result = {"file": result}

    # Dispatch:
    if isinstance(result, str):
        await ctx.send(result)
    elif isinstance(result, dict):
        await ctx.send(**result)
    elif type(result).__name__ == 'Image' and type(result).__module__ == 'PIL.Image':
        with io.BytesIO() as output:
            result.save(output, format="PNG")
            with io.BytesIO(output.getvalue()) as png:
                await ctx.send(file=discord.File(png, filename="image.png"))
        return
    else:
        print("Unknown response type", type(result))

cmds = {}
while other:
    name, expr, *other = other
    root = ast.parse(expr)
    # print(ast.dump(root))
    seen = set()
    stored = set()
    params = []
    for node in ast.walk(root):
        if isinstance(node, ast.Name):
            if node.id not in seen and node.id not in builtins:
                seen.add(node.id)
                params.append(node.id)
            if isinstance(node.ctx, ast.Store):
                stored.add(node.id)
        if isinstance(node, ast.Lambda):
            for arg in node.args.args:
                stored.add(arg.arg)

    params = [p for p in params if p not in stored]
    print(name, params)
    exec(f"""\
@bot.hybrid_command(name=name)
async def f(ctx{''.join(', ' + p  for p in params)}):
    result = {expr}
    await convert(ctx, result)""", globals() | imports)

@bot.command()
async def sync_commands(ctx):
    print("Syncing commands")
    bot.tree.copy_global_to(guild=ctx.guild)
    await bot.tree.sync()

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"{error}\nUsage: {ctx.command.name} " + " ".join(f"<{p}>" for p in ctx.command.params))
    else:
        raise error

bot.run(token)
