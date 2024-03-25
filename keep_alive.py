from flask import Flask,render_template
from threading import Thread
from main import bot

app = Flask(__name__)

@app.route('/')
def index():
    return """
<html>
<head><meta http-equiv="refresh" content="1; URL=/dash" /></head>
<body><p>Alive</p></body
</html

"""

@app.route('/invite')
def invite():
   return render_template("dashboard/invite/index.html")

@app.route('/discord')
def discord_():
   return render_template("dashboard/discord/index.html")

@app.route('/premium')
def premium():
   return render_template("dashboard/premium/index.html")

@app.route('/dash')
def dash():
   guilds = bot.guilds
   guild_amount = 0
   member_count = 0
   for i in guilds:
      guild_amount += 1
      member_count += i.member_count
   file = open("amount-cmds.txt")
   command_count = file.readline(-1)
   return render_template("dashboard/index.html", guilds=guilds, member_count=member_count, command_count=command_count, guild_amount=guild_amount)

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():  
    t = Thread(target=run)
    t.start()
