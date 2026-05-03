# #from agentic.chunkings.chunker import chunk_text
# #from agentic.logger import logging

# from agentic.logger.logging import get_logger , setup_logging
# from agentic.exception import Agentic_Exception
# import sys

# #from agentic.logger import logger

# setup_logging()
# logger = get_logger("agentic")

# def main():

#     text = "Example document"

#     #chunks = chunk_text(text)

#     logger.info(f"Chunks created: {len(text)}")

#     try :
#         c = 10/0
#         print(c)
#     except Exception as e :
#         raise Agentic_Exception(e, sys) from e


# if __name__ == "__main__":
#     main()

from agentic.chunkings.chunking import build_chunks
from agentic.data_loader import DataLoader
from agentic.data_loader import load, load_from_config

laws_df = load(filename="laws_de.csv", nrows=1000)

chunks = build_chunks(laws_df)
print(chunks[500:501])