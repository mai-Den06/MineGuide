import os

# guide
API_KEY = os.getenv("API_KEY")
ENDPOINT = os.getenv("ENDPOINT")
API_VERSION = '2024-02-01'
MODEL = "gpt-4o"

# object detection
MODEL_PATH = './weights/ore_v2.pt'

# window capture
WINDOW_NAME = 'Minecraft*'

# database
DB_PATH = "./data/ore.db"

# overlay
IMAGE_SAMPLE_PATH = './data/sample_images'
