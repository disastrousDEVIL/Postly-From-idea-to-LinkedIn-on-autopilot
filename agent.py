import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition
from prompts import MAIN_AGENT_PROMPT, POST_WRITER_PROMPT, IMAGE_CREATOR_PROMPT


def get_options() -> ClaudeAgentOptions:
    """Build agent options with subagent definitions."""
    return ClaudeAgentOptions(
        system_prompt=MAIN_AGENT_PROMPT,
        allowed_tools=["WebSearch", "WebFetch", "Task"],
        agents={
            "post-writer": AgentDefinition(
                description="Write or rewrite a viral LinkedIn post given topic, research, and feedback.",
                prompt=POST_WRITER_PROMPT,
                tools=[],
            ),
            "image-creator": AgentDefinition(
                description="Suggest image prompt ideas for a post, or return an approved prompt for generation.",
                prompt=IMAGE_CREATOR_PROMPT,
                tools=[],
            ),
        },
        permission_mode="bypassPermissions",
    )


async def run_agent(user_message: str, history: list[dict]) -> tuple[str, str | None]:
    """Run the main agent with conversation history.

    Returns:
        tuple of (response_text, approved_prompt_or_None)
        - response_text: the agent's full text response
        - approved_prompt: extracted if agent returned APPROVED_PROMPT:, else None
    """
    options = get_options()
    result_text = ""

    async for message in query(prompt=user_message, options=options):
        # AssistantMessage has .content which is a list of content blocks
        if hasattr(message, "content"):
            for block in message.content:
                if hasattr(block, "text"):
                    result_text = block.text

    # Extract approved prompt if the agent marked one
    approved_prompt = None
    if "APPROVED_PROMPT:" in result_text:
        approved_prompt = result_text.split("APPROVED_PROMPT:")[-1].strip()

    return result_text, approved_prompt
