# Nerdtendo
The original Super Mario Maker Discord bot, now supporting SMM2!

---

## Setup

### Requirements
- Python 3.8+
- (optional) [pm2](https://pm2.keymetrics.io/), to manage the bot's process

### Installation
1. Clone the source to your computer.
```
git clone https://github.com/burritosoftware/Nerdtendo.git
cd Nerdtendo
```

2. Install the necessary requirements.
```
python3.8 -m pip install -r requirements.txt
python3.8 -m pip install git+https://github.com/neonjonn/lightbulb-ext-neon.git
```

3. Create an `.env` file, and paste your Discord bot token inside.
```
cp .env-example .env
nano .env
```

4. Start the bot.
```
python3.8 bot.py
(or if using pm2)
pm2 start --interpreter=python3.8 bot.py
```