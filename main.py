import os

from turn_enum import turn_enum
from process_turn import process_turn_rec

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

process_turn_rec((), turn_enum.USER, None)
