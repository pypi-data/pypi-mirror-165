# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['disuniter']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dis-uniter',
    'version': '1.1.0',
    'description': 'Keep your discord bot alive on replit',
    'long_description': "This creates a simple website to go with your discord.py bot on https://replit.com so it can be kept alive.\n# Usage\nStore your bot token in a secret called `DISCORD_TOKEN`. Secrets are accessed through the lock icon on the left on desktop, and commands tab at the bottom > secrets on mobile.\n```py\nfrom discord.ext import commands\nfrom disuniter import keepAlive\nimport discord\n# Include members intent here if you want to show your discord tag and profile picture, but that will disable the logging to protect users' privacy\nbot = commands.Bot()\n# Needed to show DM owner link if you don't have members intent, but can be omitted if you don't want to show your DM link anyways\nbot.owner_id = your_discord_user_id_here\n# normal bot code here...\nkeepAlive(bot)\n```\nWait, where's the `bot.run`?? The `keepAlive` function does that for you\n1) To enforce using a secret to store your token so you don't expose it (NEVER expose it even if you are to remove it instantly, because people can check your repl's history)\n2) To restart your bot automatically when there's a rate limit. Rate limits are caused by too many requests from the same IP that is shared across multiple repls, and are responsible for downtimes on replit-hosted bots.\n\n# Why this?\n- No dependencies, unlike the typical Flask keep-alive\n- No spammy output, unlike Flask and the keep-alive I usually recommended on the replit discord\n- It shows:\n\t- Uptime\n\t- Number of servers\n\t- Latency (ping)\n\t- Logs, unless you have any of the following privacy-violating intents:\n\t\t- `message_content`\n\t\t- `presences`\n\t\t- `members`\n- It automatically adds your repl to https://up.repl.link, a pinger, if it isn't already there\n- It uses [Solarized](https://ethanschoonover.com/solarized/#features), which is objectively the best colour palette ever.\n# Why is it called dis-uniter?\nI am keeping Discord bots alive. Discord = disagreement. I am dis-uniting by keeping disagreements alive.",
    'author': 'Umar Sharief',
    'author_email': 'umar.sharief04@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
