# zoho_checkbot

A Telegram bot that helps you process and analyze financial documents like PDFs and Excel files, with built-in web search capabilities for current financial information.

## Features

- Process and analyze PDF documents
- Process and analyze Excel files (including multiple sheets)
- Ask questions about your documents
- Batch processing of multiple files
- Built-in web search for current financial information
- Multilingual support (English and Burmese)

## Web Search Capabilities

The bot uses the `gemini-pro` model which has built-in web search capabilities. This means it can automatically access current financial information from the web when needed to provide more accurate and up-to-date responses.

Examples of when web search is used:
- Current exchange rates
- Latest financial news
- Recent stock prices
- Current interest rates
- Recent economic data

## Requirements

- Python 3.8+
- Telegram Bot Token
- Google Gemini API Key

## Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your credentials:
   ```
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token
   GEMINI_API_KEY=your_google_gemini_api_key
   ```
4. Run the bot:
   ```
   python src/bot.py
   ```

## Usage

1. Start a conversation with the bot on Telegram
2. Upload a PDF or Excel file
3. Ask questions about the document
4. Or use `/batch` to process multiple files together
5. Use `/search <query>` to search for specific current information

## Commands

- `/start` - Start the bot
- `/help` - Show help message
- `/batch` - Process multiple files together
- `/batch_analyze` - Analyze all uploaded files together
- `/batch_clear` - Clear the current batch
- `/batch_status` - Check the status of your batch
- `/search <query>` - Search the web for current information
- `/english` - Switch to English
- `/burmese` - Switch to Burmese

## Supported File Types

- PDF (.pdf)
- Excel (.xls, .xlsx)

## Examples of Questions

- "What is the total revenue?"
- "List all transactions over $1000"
- "Show me all expense categories"
- "What was the highest expense?"
- "Compare the revenue in these files"
- "Find duplicate entries between documents"
- "What is the current USD to EUR exchange rate?"
- "What are the latest interest rates?"

## Note

The bot automatically searches the web for current financial information when needed to provide more accurate and up-to-date responses.