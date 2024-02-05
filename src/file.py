import json

with open("src/sit_data/chars.json", "r", encoding="utf-8") as f:
        json_data = f.read()
    
chars = json.loads(json_data)
bots = [entry["bot"] for entry in chars]

bot = "전영중"
bot_data = next((entry for entry in chars if entry["bot"] == bot), None)
print(bot_data)