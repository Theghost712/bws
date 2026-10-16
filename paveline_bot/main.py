import asyncio
import logging

from . import config

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def main() -> None:
    logger.info("Starting Paveline Bot...")
    # Bot startup wiring happens here as we complete the build.


if __name__ == "__main__":
    asyncio.run(main())
