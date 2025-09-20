"""
Configuration file for the Research-to-Startup AI Agent Swarm.
"""

import os

# Gemini API Configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'demo-key-placeholder')
GEMINI_MODE = os.getenv('GEMINI_MODE', 'demo')  # 'demo' or 'production'

# Tavily API Configuration
TAVILY_API_KEY = os.getenv('TAVILY_API_KEY', 'demo-key-placeholder')
TAVILY_MODE = os.getenv('TAVILY_MODE', 'demo')  # 'demo' or 'production'

# Application Settings
APP_TITLE = "Research-to-Startup AI Agent Swarm"
APP_ICON = "🚀"
APP_LAYOUT = "wide"

# Agent Settings
AGENT_PROCESSING_DELAY = 1  # seconds between agent processing steps
MAX_TEXT_LENGTH = 10000  # maximum text length for processing

# PDF Settings
MAX_PDF_PAGES = 50  # maximum pages to process from PDF

# Output Settings
DEFAULT_OUTPUT_DIR = "output"
PITCH_DECK_FILENAME = "pitch_deck.pdf"
