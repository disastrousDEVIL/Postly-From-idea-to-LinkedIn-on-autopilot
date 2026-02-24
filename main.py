import os
from io import BytesIO
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from agent import run_agent
from tools import generate_image
from state import load, save

load_dotenv()


async def handle_message(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    """Handle every incoming Telegram message (text, photo, or command)."""
    chat_id = update.effective_chat.id
    state = load(chat_id)
    history = state.get("history", [])

    # Build the user message — handle photos with captions
    user_msg = update.message.text or ""
    if update.message.photo:
        file = await update.message.photo[-1].get_file()
        user_msg = f"[IMAGE ATTACHED: {file.file_path}] {update.message.caption or ''}"

    # Show typing indicator while agent works
    await update.message.chat.send_action("typing")

    # Run the main agent
    response, approved_prompt = await run_agent(user_msg, history)

    # If agent returned an approved prompt → generate image via Replicate
    if approved_prompt:
        await update.message.reply_text("🎨 Generating your image...")
        image_bytes = await generate_image(approved_prompt)

        # Send image as photo in Telegram
        await update.message.reply_photo(
            photo=BytesIO(image_bytes),
            caption="Here's your image! If you're happy with it, the post is ready to copy-paste above.",
        )

        # Save the approved post for reference
        state["approved_post"] = response.split("APPROVED_PROMPT:")[0].strip()

    # Update conversation history (keep last 20 messages)
    history.append({"role": "user", "content": user_msg})
    history.append({"role": "assistant", "content": response})
    state["history"] = history[-20:]
    save(chat_id, state)

    # Send response — split long messages (Telegram 4096 char limit)
    # Strip the APPROVED_PROMPT marker from what the user sees
    display_text = response.split("APPROVED_PROMPT:")[0].strip() if approved_prompt else response
    for i in range(0, len(display_text), 4096):
        await update.message.reply_text(display_text[i : i + 4096])


async def weekly_trigger(app):
    """Workflow 2 — fires every Monday 9am. Sends trending AI topics to user."""
    chat_id = int(os.getenv("TELEGRAM_CHAT_ID", "0"))
    if not chat_id:
        print("⚠️ TELEGRAM_CHAT_ID not set — skipping weekly trigger.")
        return

    state = load(chat_id)
    history = state.get("history", [])

    response, _ = await run_agent(
        "Run Workflow 2: find 6 trending AI topics from the past 7 days.",
        history,
    )

    # Send response — split long messages
    for i in range(0, len(response), 4096):
        await app.bot.send_message(chat_id=chat_id, text=response[i : i + 4096])

    # Save to history
    history.append({"role": "user", "content": "Run Workflow 2"})
    history.append({"role": "assistant", "content": response})
    state["history"] = history[-20:]
    save(chat_id, state)


def main():
    """Start the Telegram bot with weekly scheduler."""
    app = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
    app.add_handler(MessageHandler(filters.ALL, handle_message))

    # Schedule Workflow 2: every Monday at 9am
    scheduler = AsyncIOScheduler()
    scheduler.add_job(weekly_trigger, "cron", day_of_week="mon", hour=9, args=[app])
    scheduler.start()
    print("🤖 PostPilot is running...")
    print("📅 Weekly trigger scheduled: every Monday at 9am")

    app.run_polling()


if __name__ == "__main__":
    main()
