# PostPilot

From idea to LinkedIn — on autopilot.

A Telegram bot that researches topics, writes viral LinkedIn posts, generates matching images, and delivers everything ready to copy-paste. Powered by Claude Agent SDK and Replicate.

---

## ⚡ How It Works

```
You send a topic
    → Agent researches it (WebSearch)
        → Post-writer drafts a LinkedIn post
            → You iterate until happy
                → Image-creator suggests visual prompts
                    → You pick one
                        → Replicate generates the image
                            → Post + image delivered in Telegram
```

No auto-posting. You copy-paste to LinkedIn on your own terms.

---

## 🏗 Architecture

```
main.py          Telegram bot + scheduler (entry point)
agent.py         Claude Agent SDK + subagent definitions
prompts.py       System prompts for all three agents
tools.py         Replicate image generation
state.py         Per-user JSON state persistence
```

### Agent Hierarchy

```
Main Agent (Claude)
├── WebSearch / WebFetch    ← research tools
├── post-writer subagent    ← writes LinkedIn posts
└── image-creator subagent  ← suggests image prompts
```

The main agent delegates automatically via the `Task` tool. Subagents are pure text — they have no tool access. Image generation happens in Python, not inside the agent.

---

## 🔄 Workflows

### Workflow 1: On-Demand

Send a topic (text or image) to the bot:

1. Agent researches 3-5 recent facts via WebSearch
2. Post-writer drafts a 150-300 word LinkedIn post
3. You review and give feedback (More Punchy / More Vulnerable / New Angle / Suggest a Change)
4. Loop until you approve
5. Image-creator suggests 3-4 visual prompt ideas
6. You pick one
7. Replicate generates the image
8. Final post + image delivered in Telegram

### Workflow 2: Weekly (Monday 9am)

Runs automatically via APScheduler:

1. Agent searches for 6 trending AI topics from the past week
2. Sends numbered list to your Telegram
3. You pick 3 topics
4. Each topic goes through the full Workflow 1 pipeline
5. All 3 posts delivered when done

---

## 🧱 Stack

| Component | Technology |
|-----------|-----------|
| Agent framework | `claude-agent-sdk` |
| Telegram interface | `python-telegram-bot` |
| Image generation | `replicate` (Flux models) |
| Scheduling | `apscheduler` |
| Config | `python-dotenv` |

---

## 🚀 Setup

### Prerequisites

- Python 3.9+
- Telegram bot token from [@BotFather](https://t.me/botfather)
- [Anthropic API key](https://console.anthropic.com)
- [Replicate API token](https://replicate.com/account/api-tokens)

### Install

```bash
git clone https://github.com/disastrousDEVIL/Postly-From-idea-to-LinkedIn-on-autopilot.git
cd Postly-From-idea-to-LinkedIn-on-autopilot
pip install -r requirements.txt
```

### Configure

```bash
cp .env.example .env
```

Fill in your keys:

```env
TELEGRAM_BOT_TOKEN=your-bot-token
TELEGRAM_CHAT_ID=your-chat-id
ANTHROPIC_API_KEY=your-anthropic-key
REPLICATE_API_TOKEN=your-replicate-token
REPLICATE_MODEL=black-forest-labs/flux-schnell
```

| Variable | Where to get it |
|----------|----------------|
| `TELEGRAM_BOT_TOKEN` | [@BotFather](https://t.me/botfather) on Telegram |
| `TELEGRAM_CHAT_ID` | Message [@userinfobot](https://t.me/userinfobot) on Telegram |
| `ANTHROPIC_API_KEY` | [console.anthropic.com](https://console.anthropic.com) |
| `REPLICATE_API_TOKEN` | [replicate.com/account/api-tokens](https://replicate.com/account/api-tokens) |
| `REPLICATE_MODEL` | Any Replicate image model (default: `flux-schnell`) |

### Run

```bash
python main.py
```

```
PostPilot is running...
Weekly trigger scheduled: every Monday at 9am
```

Open your Telegram bot and send a topic to start.

---

## 🎨 Switching Image Models

Change `REPLICATE_MODEL` in `.env` without touching code:

```env
REPLICATE_MODEL=black-forest-labs/flux-schnell    # fast, cheap
REPLICATE_MODEL=black-forest-labs/flux-dev         # better quality
REPLICATE_MODEL=black-forest-labs/flux-pro         # best quality
```

---

## 📁 Project Structure

```
PostPilot/
├── main.py              # Telegram bot + scheduler
├── agent.py             # Claude SDK + subagents
├── prompts.py           # All system prompts
├── tools.py             # Replicate image generation
├── state.py             # JSON state persistence
├── requirements.txt     # Pinned dependencies
├── .env.example         # Config template
├── .env                 # Your credentials (git-ignored)
├── .gitignore
└── state.json           # Auto-created at runtime (git-ignored)
```

---

## 🪄 License

This project is licensed under the MIT License.
You are free to use, modify, and distribute this software with attribution. See the [LICENSE](LICENSE) file for full details.

## 👤 Author

**Krish Batra**
- Website: [vybecode.in](https://vybecode.in)
- Email: [krishbatra3@gmail.com](mailto:krishbatra3@gmail.com)
- LinkedIn: [krish-batra](https://linkedin.com/in/krish-batra)
