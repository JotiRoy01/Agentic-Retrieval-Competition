#from agentic.chunkings.chunker import chunk_text
#from agentic.logger import logging

from agentic.logger.logging import get_logger , setup_logging
#from agentic.logger import logger

setup_logging()
logger = get_logger("agentic")

def main():

    text = "Example document"

    #chunks = chunk_text(text)

    logger.info(f"Chunks created: {len(text)}")


if __name__ == "__main__":
    main()