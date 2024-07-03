def get_excluded_files():
    return ['main.py', 'replit.nix', 'keep_alive.py', 'add.py', 'host.py', 'edit_files.py', 'fork.py', "runner", 'home', 'bin', 'boot', 'dev', 'etc', 'inject', 'mnt', 'io', 'lib', 'lib32', 'bin', 'SelfHost']

import discord
from discord.ext import commands
import subprocess
import os
import shutil
from discord.ext import commands
import subprocess
import shutil
import tempfile
import pexpect
import importlib
import threading
import asyncio
import io
from contextlib import redirect_stdout
from keep_alive import keep_alive
keep_alive()

import os
import io



intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

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

        def run_file_thread(ctx, path):
            # Capture output
            output = io.StringIO()
            with redirect_stdout(output):
                try:
                    exec(open(path).read())
                except Exception as e:
                    output.write(str(e))

            # Send the output line by line
            lines = output.getvalue().splitlines()
            for line in lines:
                asyncio.run_coroutine_threadsafe(ctx.send(line), bot.loop)

        # Start the file execution in a separate thread
        thread = threading.Thread(target=run_file_thread, args=(ctx, path))
        thread.start()

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



bot = commands.Bot(command_prefix='!', intents=intents)

async def edit_file(ctx, filename, content):
        """
        Edits a file.

        Args:
            ctx: Context di Discord.
            filename: Nome del file Python da modificare.
            content: Nuovo contenuto Python (come stringa).
        """

        file_path = f"{filename}"  # Modifica il percorso in base alle tue esigenze

        # Tentare di caricare il contenuto del file esistente (se presente)
        try:
            with open(file_path, "r") as f:
                existing_content = f.read()
        except FileNotFoundError:
            existing_content = ""

        # Aggiornare il contenuto con le modifiche richieste
        new_content = content.strip()  # Rimuovere gli spazi bianchi all'inizio e alla fine

        # Usare un diff tool temporaneo per generare le modifiche
        diff_process = subprocess.Popen(
            ["diff", "-u", "0", existing_content, new_content],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        diff_output, _ = diff_process.communicate()
        diff_text = diff_output.decode("utf-8")

        # Inviare un messaggio di anteprima con le modifiche
        if diff_text:
            await ctx.send(f"`diff\n{diff_text}`")
            await ctx.send("Confirm? (y/n)")

            response = await ctx.bot.wait_for("message", check=lambda m: m.author == ctx.author and m.content.lower() in ["y", "n"])

            if response.content.lower() == "n":
                await ctx.send("Canceled.")
                return

        # Salvare il file Python aggiornato
        with open(file_path, "w") as f:
            f.write(new_content)

        # Inviare un messaggio di conferma
        await ctx.send(f"File {filename} updated!")

@bot.command()
async def edit(ctx, filename, *, content):
        """Comando alias per edit_file."""
        await edit_file(ctx, filename, content)

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
        await ctx.send("Il file deve essere un file Python.")
        return

    output = await run_file(ctx, path)
    await ctx.send(output)


@bot.command(name="view")
async def view_code(ctx, filename):
    """
    Views a file

    Args:
        ctx: Context
        filename: Name of the file to view
    """

    # Recupera il percorso del file
    file_path = f"{filename}"

    # Controlla se il file esiste
    if os.path.exists(file_path):
        try:
            # Leggi il contenuto del file
            with open(file_path, "r") as f:
                file_content = f.read()

            # Formatta il codice per la visualizzazione
            code_block = f"**{file_content}**"

            # Invia il codice come embed message
            embed = discord.Embed(title=f"Code: {filename}", description=code_block)
            await ctx.send(embed=embed)
        except Exception as e:
            # Gestisci gli errori di lettura del file
            await ctx.send(f"Error while reading the file: {e}")
    else:
        # Il file non esiste
        await ctx.send(f"Error: File {filename} not found.")

my_secret = os.environ['TOKEN']

bot.run(my_secret)
import tempfile
import pexpect
import importlib
from keep_alive import keep_alive
keep_alive()

intents = discord.Intents.default()
intents.message_content = True
