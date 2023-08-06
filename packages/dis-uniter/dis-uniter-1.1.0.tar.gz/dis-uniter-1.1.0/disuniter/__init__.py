from http import server
import multiprocessing, os, time, logging, glob, sys, threading, asyncio
from logging import handlers
from urllib import request

os.system("kill `pidof Xvnc` 2> /dev/null")


def keepAlive(bot):
    @bot.event
    async def on_ready():
        app_info_ref = [await bot.application_info()]

        class Server(server.BaseHTTPRequestHandler):
            _bot = bot
            start = time.time()

            def log_request(self, code="", size=""):
                pass

            def do_GET(self):
                app_info = app_info_ref[0]
                self.send_response(200)
                self.send_header(
                    "Content-Type",
                    "font/woff2"
                    if self.path == "/W.woff2"
                    else "text/html;charset=utf-8",
                )
                self.send_header(
                    "Cache-Control",
                    "max-age=31536000, immutable"
                    if self.path == "/W.woff2"
                    else "no-cache",
                )
                self.send_header("x-content-type-options", "nosniff")
                self.end_headers()
                bot = self._bot
                owner = app_info.owner
                team = app_info.team
                user = bot.user
                self.wfile.write(
                    open(f"{os.path.dirname(__file__)}/W.woff2", "rb").read()
                    if self.path == "/W.woff2"
                    else b"\n".join([open(i, "rb").read() for i in glob.glob("logs*")])
                    if self.path == "/logs"
                    else (
                        f"<!DOCTYPE html><meta charset=utf-8><meta name=viewport content='width=device-width'><link rel='shortcut icon'href={user.avatar.url}><html lang=en><script>onload=()=>setInterval(()=>{{let u=BigInt(Math.ceil(Date.now()/1000-{self.start}))\ndocument.getElementById('u').innerText=`${{u>86400n?`${{u/86400n}}d`:''}}${{u>3600n?`${{u/3600n%60n}}h`:''}}${{u>60n?`${{u/60n%24n}}m`:''}}${{`${{u%60n}}`}}s`}},1000)</script><style>@font-face{{font-family:W;src:url('W.woff2')}}*{{background-color:#FDF6E3;color:#657B83;font-family:W;text-align:center;margin:auto}}@media(prefers-color-scheme:dark){{*{{background-color:#002B36;color:#839496}}img{{height:1em}}</style><title>{user}</title><h1>{user}<img src={user.avatar} alt></h1><table><tr><td>Servers<td>{len(bot.guilds)}<tr><td>Latency<td>{round(bot.latency*1000 if bot.latency!=float('nan') else 'Offline?')}ms<tr><td>Uptime<td id=u>{f'<tr><td><a href=${team.icon}>'+[f'<tr><td><a href=https://discord.com/users/{m}>Creator</a><img src={m.avatar} alt>'for m in team.members].join('')if team else f'<tr><td><a href=https://discord.com/users/{owner.id}>DM owner</a><td><img src={owner.avatar} alt>{owner}'}</table><br>"
                        + "<div id=l></div><button type=button onclick=\"setInterval(()=>{let x=new XMLHttpRequest();x.onload=r=>document.getElementById('l').innerText=r.srcElement.responseText;x.open('GET','logs');x.send()},1e3)\">Show logs"
                        if os.path.isfile("logs")
                        else ""
                    ).encode()
                )

        multiprocessing.Process(
            target=server.HTTPServer(("", 80), Server).serve_forever
        ).start()
        print("Server is ready! Hit enter at any time to update app info")
        while True:
            t = threading.Thread(target=input)
            t.start()
            while t.is_alive():
                await asyncio.sleep(0)
            app_info_ref[0] = await bot.application_info()

    intents = bot.intents
    if not (intents.presences or intents.members or intents.message_content):
        logger = logging.getLogger("discord")
        logger.setLevel(logging.DEBUG)
        handler = handlers.TimedRotatingFileHandler(
            "./logs", backupCount=1, when="m", interval=30
        )
        handler.setFormatter(
            logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
        )
        logger.addHandler(handler)
    try:
        request.urlopen(
            f"https://up.repl.link/add?author={os.environ['REPL_OWNER'].lower()}&repl={os.environ['REPL_SLUG'].lower()}"
        )
    except:
        pass

    @bot.listen()
    async def on_disconnect():
        if bot.is_ws_ratelimited():
            os.kill(1, 1)

    try:
        bot.run(os.environ["DISCORD_TOKEN"])
    except:
        if bot.is_ws_ratelimited():
            os.kill(1, 1)
