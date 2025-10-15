import os
import datetime
import discord
from github import Github

# 環境変数からトークン取得
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
REPO_NAME = "calmkamille/diary"  # ここは自分のリポジトリに書き換え

# GitHubに接続
g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)

# Discordクライアント
intents = discord.Intents.default()
intents.message_content = True  # メッセージ内容を取得可能にする
client = discord.Client(intents=intents)

def post_diary(content: str):
    """GitHub に日記を作成または更新する関数"""
    day = datetime.datetime.now().strftime("%Y-%m-%d")
    path = f"diary/{day}.txt"

    try:
        # ファイルが存在するか確認
        existing_file = repo.get_contents(path)
        # 存在する場合は更新
        repo.update_file(
            path=path,
            message=f"Update diary {day}",
            content=content,
            sha=existing_file.sha
        )
        print(f"✅ Updated diary: {path}")

    except Exception as e:
        # 存在しない場合は新規作成
        repo.create_file(
            path=path,
            message=f"Add diary {day}",
            content=content
        )
        print(f"✅ Created new diary: {path}")

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")

@client.event
async def on_message(message):
    # Bot 自身のメッセージは無視
    if message.author == client.user:
        return

    # 受信したメッセージを GitHub に保存
    try:
        post_diary(message.content)
        await message.channel.send("日記を GitHub に保存しました！")
    except Exception as e:
        print(f"❌ Error: {e}")
        await message.channel.send("日記の保存に失敗しました。")

# Bot 起動
client.run(DISCORD_TOKEN)
