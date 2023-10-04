def get_excluded_files():
    return ['main.py', 'replit.nix', 'keep_alive.py']

import discord
from discord.ext import commands
import subprocess
import shutil
import tempfile
import pexpect
import importlib
import os
import io

async def edit_file(ctx, path):
    """Modifica un file.

    Args:
        ctx: Il contesto del comando.
        path: Il percorso del file da modificare.

    Returns:
        Nessuno.
    """

    if not os.path.exists(path):
        await ctx.send("the file dosen't exist.")
        return

    with open(path, "r") as f:
        content = f.read()

    edit = await ctx.prompt("Inserisci il nuovo contenuto del file:")

    with open(path, "w") as f:
        f.write(edit_content)

async def run_file(ctx, path):
    """Esegue un file.

    Args:
        ctx: Il contesto del comando.
        path: Il percorso del file da eseguire.

    Returns:
        L'output del comando.
    """

    output = subprocess.check_output(["python", path])
    return output.decode()



intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command(name='mkdir')
async def mkdir(ctx, directory):
    # Esegue il comando mkdir e ottiene l'output del comando come oggetto stringa.
    result = subprocess.check_output(['mkdir', directory]).decode("utf-8")

    # Invia il messaggio al canale Discord.
    await ctx.send(f'`folder created`')


@bot.command(name='terminal')
async def any(ctx, command):
    # Esegue il comando specificato e ottiene l'output del comando come oggetto Popen.
    process = subprocess.Popen([command], stdout=subprocess.PIPE)

    # Legge l'output del comando riga per riga.
    for line in process.stdout:
        # Invia il messaggio al canale Discord.
        await ctx.send(f'`{line.decode("utf-8")}`')

@bot.command(name='rm')
async def rm(ctx, file):
    # Ottieni la lista di file da escludere.
    excluded_files = get_excluded_files()

    # Controlla se il file è nella lista di file da escludere.
    if file in excluded_files:
        # Invia un messaggio di errore.
        await ctx.send(f'`Error: you cant delete the code of the bot: {file}`')
    else:
        # Elimina il file.
        os.remove(file)

@bot.command(name='rmdir')
async def rmdir(ctx, directory):
    # Elimina la cartella specificata.
    try:
        shutil.rmtree(directory)
    except OSError:
        await ctx.send(f'`Folder not found: {directory}`')
    else:
        await ctx.send(f'`Folder deleted: {directory}`')

@bot.command(name='cd')
async def cd(ctx, directory):
    # Cambia la directory corrente.
    try:
        os.chdir(directory)
    except OSError:
        await ctx.send(f'`Error: folder not found: {directory}`')
    else:
        await ctx.send(f'`current directory: {os.getcwd()}`')
      
@bot.command(name='touch')
async def touch(ctx, file):
    # Crea il file specificato.
    try:
        open(file, 'w').close()
    except FileExistsError:
        await ctx.send(f'`Error: file already exists: {file}`')
    else:
        await ctx.send(f'`File created: {file}`')

@bot.command(name='echo')
async def echo(ctx, *args):
    # Stampa il testo specificato.
    await ctx.send(' '.join(args))

@bot.command(name='apt')
async def apt(ctx, *args):
    # Esegue il comando `apt` con gli argomenti specificati.
    try:
        output = subprocess.check_output(['apt', *args])
    except subprocess.CalledProcessError as e:
        # Invia un messaggio di errore se il comando `apt` fallisce.
        await ctx.send(e.output.decode())
        return

    # Invia il risultato del comando `apt` al messaggio.
    await ctx.send(output.decode())

@bot.command(name="start")
async def run_file_command(ctx, path):
    """Esegue un file.

    Args:
        ctx: Il contesto del comando.
        path: Il percorso del file da eseguire.

    Returns:
        Nessuno.
    """

    if not path.endswith(".py"):
        await ctx.send("the file must be in python")
        return

    output = await run_file(ctx, path)
    await ctx.send(output)

@bot.command(name="edit")
async def edit_file_command(ctx, path):
    """Modifica un file.

    Args:
        ctx: Il contesto del comando.
        path: Il percorso del file da modificare.

    Returns:
        Nessuno.
    """

    await edit_command(ctx, path)
    await ctx.send("Il file è stato modificato.")

my_secret = os.environ['TOKEN']

bot.run(my_secret)
