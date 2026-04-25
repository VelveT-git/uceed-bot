from questions import questions
import random 

print("RUNNING MAIN.PY")

import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True 
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def uceed(ctx, qtype=None, category=None, number: int = 1):

    filtered = questions

    # filter by type
    if qtype:
        filtered = [q for q in filtered if q["type"] == qtype.upper()]

    # filter by category
    if category:
        filtered = [q for q in filtered if q["category"] == category.capitalize()]

    if len(filtered) == 0:
        await ctx.send("No questions found for this filter.")
        return

    selected = random.sample(filtered, min(number, len(filtered)))

    for q in selected:
        await ctx.send(f"**{q['question']}**")

        if "image" in q:
            await ctx.send(file=discord.File(q["image"]))

        if "options" in q:
            await ctx.send("\n".join(q["options"]))

        await ctx.send("✍️ Reply with your answer (30 seconds)")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            msg = await bot.wait_for("message", timeout=30.0, check=check)

            user_answer = msg.content.strip().upper()
            correct = q["answer"]

            if isinstance(correct, list):
                if sorted(user_answer.split()) == sorted(correct):
                    await ctx.send("✅ Correct!")
                else:
                    await ctx.send(f"❌ Wrong! Correct answer: {correct}")
            else:
                if user_answer == str(correct).upper():
                    await ctx.send("✅ Correct!")
                else:
                    await ctx.send(f"❌ Wrong! Correct answer: {correct}")

        except:
            await ctx.send(f"⏰ Time up! Correct answer: {q['answer']}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    print("Message seen:", message.content)

    await bot.process_commands(message)

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

import os
TOKEN = os.getenv("TOKEN")
bot.run(TOKEN)