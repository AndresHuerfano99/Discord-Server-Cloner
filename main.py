#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import time

# Third-party imports
try:
    import platform
    import discord
    import inquirer
    import psutil
    from art import text2art
    from helpmodule import Clone
    from colorama import Fore, Style
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import Progress
    from rich.table import Table
    import traceback
    import asyncio
except Exception as e:
    print(e)


def loading(seconds: int) -> None:
    """
    Display a progress bar for the specified number of seconds.
    """
    with Progress() as progress:
        task = progress.add_task("Loading...", total=seconds)
        while not progress.finished:
            progress.update(task, advance=1)
            time.sleep(1)


def get_user_preferences() -> dict:
    """
    Show default cloning preferences and allow the user to reconfigure them.

    Returns:
        dict: A dictionary with cloning preferences.
    """
    # Default preferences
    default_preferences = {
        'guild_edit': True,
        'channels_delete': True,
        'roles_create': True,
        'categories_create': True,
        'channels_create': True,
        'emojis_create': False
    }

    def map_boolean_to_string(value: bool) -> str:
        return "Yes" if value else "No"

    # Prepare a panel content displaying current settings
    panel_content = "\n".join([
        f"- Change server name and icon: {map_boolean_to_string(default_preferences['guild_edit'])}",
        f"- Delete destination server channels: {map_boolean_to_string(default_preferences['channels_delete'])}",
        f"- Clone roles: {map_boolean_to_string(default_preferences['roles_create'])}",
        f"- Clone categories: {map_boolean_to_string(default_preferences['categories_create'])}",
        f"- Clone channels: {map_boolean_to_string(default_preferences['channels_create'])}",
        f"- Clone emojis: {map_boolean_to_string(default_preferences['emojis_create'])}"
    ])

    Console().print(
        Panel(panel_content, title="Config BETA", style="bold blue", width=70)
    )

    # Ask if the user wants to reconfigure the default settings
    questions = [
        inquirer.List(
            'reconfigure',
            message='Do you want to reconfigure the default settings?',
            choices=['Yes', 'No'],
            default='No'
        )
    ]
    answers = inquirer.prompt(questions)

    if answers and answers.get('reconfigure') == 'Yes':
        config_questions = [
            inquirer.Confirm('guild_edit', message='Edit the server icon and name?', default=False),
            inquirer.Confirm('channels_delete', message='Delete the channels?', default=False),
            inquirer.Confirm('roles_create', message='Clone roles? (NOT RECOMMENDED TO DISABLE)', default=False),
            inquirer.Confirm('categories_create', message='Clone categories?', default=False),
            inquirer.Confirm('channels_create', message='Clone channels?', default=False),
            inquirer.Confirm('emojis_create', message='Clone emojis? (Recommended for solo cloning)', default=False)
        ]
        updated_preferences = inquirer.prompt(config_questions)
        if updated_preferences:
            default_preferences.update(updated_preferences)

    # Clear the screen before returning preferences
    os.system('cls' if os.name == 'nt' else 'clear')
    return default_preferences


def restart() -> None:
    """
    Restart the current Python script.
    """
    python_executable = sys.executable
    os.execv(python_executable, [python_executable] + sys.argv)


async def main():
    """
    Main function for handling user input, authentication, and cloning operations.
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    client = discord.Client()

    # Collect user input for token and server IDs
    while True:
        token = input(f"{Style.BRIGHT}{Fore.MAGENTA}Insert your token to proceed:{Style.RESET_ALL}\n > ")
        guild_source = input(f"{Style.BRIGHT}{Fore.MAGENTA}Source server ID:{Style.RESET_ALL}\n > ")
        guild_dest = input(f"{Style.BRIGHT}{Fore.MAGENTA}Destination server ID:{Style.RESET_ALL}\n > ")
        os.system('cls' if os.name == 'nt' else 'clear')

        print(f"{Style.BRIGHT}{Fore.GREEN}The values you inserted are:")
        print(f"Token: {Fore.YELLOW}{'*' * len(token)}{Style.RESET_ALL}")
        print(f"Source Server ID: {Fore.YELLOW}{guild_source}{Style.RESET_ALL}")
        print(f"Destination Server ID: {Fore.YELLOW}{guild_dest}{Style.RESET_ALL}")

        confirm = input(f"{Style.BRIGHT}{Fore.MAGENTA}Are these values correct? (Y/N):{Style.RESET_ALL}\n > ")

        if confirm.upper() == 'Y' and guild_source.isnumeric() and guild_dest.isnumeric():
            break
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"{Style.BRIGHT}{Fore.RED}Invalid input. Please re-enter values.{Style.RESET_ALL}")

    preferences = get_user_preferences()

    @client.event
    async def on_ready():
        """
        Called when the Discord client is ready.
        Executes the cloning operations based on user preferences.
        """
        try:
            start_time = time.time()
            Console().print(Panel("Authentication successful", style="bold green", width=50))
            loading(5)
            os.system('cls' if os.name == 'nt' else 'clear')

            # Retrieve guild objects from the provided IDs
            guild_from = client.get_guild(int(guild_source))
            guild_to = client.get_guild(int(guild_dest))

            # Perform cloning operations based on preferences
            if preferences.get('guild_edit'):
                await Clone.guild_edit(guild_to, guild_from)
            if preferences.get('channels_delete'):
                await Clone.channels_delete(guild_to)
            if preferences.get('roles_create'):
                await Clone.roles_create(guild_to, guild_from)
            if preferences.get('categories_create'):
                await Clone.categories_create(guild_to, guild_from)
            if preferences.get('channels_create'):
                await Clone.channels_create(guild_to, guild_from)
            if preferences.get('emojis_create'):
                await Clone.emojis_create(guild_to, guild_from)

            elapsed_time = time.time() - start_time
            print(f"{Style.BRIGHT}{Fore.BLUE}Cloning completed in {elapsed_time:.2f} seconds.{Style.RESET_ALL}")
            await client.close()
        except Exception as e:
            print(f"{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")
            traceback.print_exc()
            restart()

    try:
        await client.start(token)
    except discord.LoginFailure:
        print(f"{Fore.RED}Invalid token.{Style.RESET_ALL}")
        restart()


if __name__ == "__main__":
    # Install requirements.
    if not os.getenv('requirements'):
        subprocess.Popen(['start', 'start.bat'], shell=True)
        sys.exit()

    os.system('cls' if os.name == 'nt' else 'clear')
    asyncio.run(main())

#start
