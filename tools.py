import asyncio
import os
import replicate


async def generate_image(prompt: str) -> bytes:
    """Generate an image via Replicate. Returns image bytes.

    Model is read from REPLICATE_MODEL env var so you can
    swap models without touching code.

    The SDK auto-reads REPLICATE_API_TOKEN from the environment.
    Replicate returns FileOutput objects — we use read() to get
    raw bytes, which Telegram can send directly via reply_photo().
    """
    model = os.getenv("REPLICATE_MODEL", "black-forest-labs/flux-schnell")
    output = await asyncio.to_thread(
        replicate.run,
        model,
        input={"prompt": prompt},
    )
    # Replicate returns a list of FileOutput objects — grab the first one
    file_output = output[0]
    # Read bytes from FileOutput (recommended over .url per Replicate docs)
    image_bytes = await asyncio.to_thread(file_output.read)
    return image_bytes
