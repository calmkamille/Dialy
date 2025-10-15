import os
import datetime
from github import Github
import discord
from dotenv import load_dotenv

# --- 環境変数読み込み ---
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_NAME = os.getenv("REPO_NAME")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

# --- GitHub 初期化 ---
g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)

# --- Discord Bot 初期化 ---
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)

# --- 起動時ログ ---
@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")

# --- メッセージ受信時処理 ---
@client.event
async def on_message(message):
    # 自分のメッセージや他チャンネルは無視
    if message.author == client.user or message.channel.id != CHANNEL_ID:
        return

    content = message.content.strip()
    if not content:
        return

    # 日付からファイル名作成
    now = datetime.datetime.now()
    year = now.year
    month = f"{now.month:02d}"
    day = now.strftime("%Y-%m-%d")
    path = f"diary/{year}/{month}/{day}.md"

    # 既存ファイルを取得して追記、無ければ新規作成
    try:
        existing = repo.get_contents(path)
        new_content = existing.decoded_content.decode("utf-8") + f"\n\n{content}"
        repo.update_file(path, f"Update diary {day}", new_content, existing.sha)
        print(f"📝 Updated existing diary: {path}")
    except:
        repo.create_file(path, f"Add diary {day}", content)
        print(f"🆕 Created new diary: {path}")

# --- Bot起動 ---
client.run(DISCORD_TOKEN)
