import os
import sys
import logging
import time
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import google.genai as genai
from google.genai import types
from dotenv import load_dotenv
import pandas as pd
import pdfplumber
import tempfile

# Add src directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from languages import MESSAGES

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configure the client
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

# Define the grounding tool
grounding_tool = types.Tool(
    google_search=types.GoogleSearch()
)

# Configure generation settings with grounding
config = types.GenerateContentConfig(
    tools=[grounding_tool]
)

# Default language
DEFAULT_LANGUAGE = 'en'

# Store user languages and conversation history (in production, use a database)
user_languages = {}
user_conversations = {}
user_document_context = {}
user_batch_context = {}  # For handling multiple files

def get_user_language(user_id):
    """Get user language preference"""
    return user_languages.get(user_id, DEFAULT_LANGUAGE)

def set_user_language(user_id, language):
    """Set user language preference"""
    user_languages[user_id] = language

def get_user_conversation(user_id):
    """Get user conversation history"""
    if user_id not in user_conversations:
        user_conversations[user_id] = []
    return user_conversations[user_id]

def add_to_conversation(user_id, role, message):
    """Add message to user conversation history"""
    conversation = get_user_conversation(user_id)
    conversation.append({"role": role, "parts": [message]})
    # Keep only the last 10 messages to avoid context overflow
    if len(conversation) > 10:
        conversation.pop(0)

def set_user_document_context(user_id, content, file_type):
    """Set user document context"""
    user_document_context[user_id] = {
        "content": content,
        "file_type": file_type,
        "timestamp": time.time()
    }

def get_user_document_context(user_id):
    """Get user document context"""
    # Check if context exists and is not too old (5 minutes)
    if user_id in user_document_context:
        context = user_document_context[user_id]
        if time.time() - context["timestamp"] < 300:  # 5 minutes
            return context
    return None

def clear_user_document_context(user_id):
    """Clear user document context"""
    if user_id in user_document_context:
        del user_document_context[user_id]

def initialize_batch_context(user_id):
    """Initialize batch context for multiple files"""
    user_batch_context[user_id] = {
        "files": [],
        "processing": False,
        "timestamp": time.time()
    }

def add_to_batch_context(user_id, file_name, content, file_type):
    """Add a processed file to batch context"""
    if user_id not in user_batch_context:
        initialize_batch_context(user_id)
    
    user_batch_context[user_id]["files"].append({
        "file_name": file_name,
        "content": content,
        "file_type": file_type
    })

def get_batch_context(user_id):
    """Get batch context for user"""
    if user_id in user_batch_context:
        context = user_batch_context[user_id]
        # Check if batch is not too old (10 minutes for batch processing)
        if time.time() - context["timestamp"] < 600:
            return context
    return None

def clear_batch_context(user_id):
    """Clear batch context"""
    if user_id in user_batch_context:
        del user_batch_context[user_id]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    user_id = update.effective_user.id
    language = get_user_language(user_id)
    welcome_message = MESSAGES[language]['welcome']
    
    # Create custom keyboard menu
    keyboard = [
        [KeyboardButton("/help"), KeyboardButton("/batch")],
        [KeyboardButton("/search"), KeyboardButton("/english")],
        [KeyboardButton("/burmese"), KeyboardButton("/batch_status")],
        [KeyboardButton("/batch_analyze"), KeyboardButton("/batch_clear")]
    ]
    
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /help is issued."""
    user_id = update.effective_user.id
    language = get_user_language(user_id)
    help_text = MESSAGES[language]['help']
    
    # Create custom keyboard menu
    keyboard = [
        [KeyboardButton("/help"), KeyboardButton("/batch")],
        [KeyboardButton("/search"), KeyboardButton("/english")],
        [KeyboardButton("/burmese"), KeyboardButton("/batch_status")],
        [KeyboardButton("/batch_analyze"), KeyboardButton("/batch_clear")]
    ]
    
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    
    await update.message.reply_text(help_text, reply_markup=reply_markup)

async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show the bot menu."""
    user_id = update.effective_user.id
    language = get_user_language(user_id)
    
    # Create custom keyboard menu
    keyboard = [
        [KeyboardButton("/help"), KeyboardButton("/batch")],
        [KeyboardButton("/search"), KeyboardButton("/english")],
        [KeyboardButton("/burmese"), KeyboardButton("/batch_status")],
        [KeyboardButton("/batch_analyze"), KeyboardButton("/batch_clear")]
    ]
    
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    
    await update.message.reply_text("Choose a command from the menu below:", reply_markup=reply_markup)

async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Search the web for current information."""
    try:
        user_id = update.effective_user.id
        language = get_user_language(user_id)
        
        # Get the search query from the message
        query = update.message.text[8:]  # Remove "/search " from the beginning
        
        if not query.strip():
            help_text = "Please provide a search query. Example: /search current exchange rates"
            await update.message.reply_text(help_text)
            return
        
        # Use grounding model to search the web
        prompt = f"{query}"
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=config,
        )
        
        await update.message.reply_text(response.text)
    except Exception as e:
        logger.error(f"Error in search_command: {e}")
        language = get_user_language(user_id)
        await update.message.reply_text(MESSAGES[language]['general_error'])

async def english_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Switch to English language"""
    user_id = update.effective_user.id
    set_user_language(user_id, 'en')
    language = get_user_language(user_id)
    message = MESSAGES[language]['language_changed']
    
    await update.message.reply_text(message)

async def burmese_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Switch to Burmese language"""
    user_id = update.effective_user.id
    set_user_language(user_id, 'my')
    language = get_user_language(user_id)
    message = MESSAGES[language]['language_changed']
    
    await update.message.reply_text(message)

async def process_pdf(file_path: str) -> str:
    """Process PDF file and extract text content with better structure."""
    text_content = []
    try:
        with pdfplumber.open(file_path) as pdf:
            text_content.append(f"PDF Document ({len(pdf.pages)} pages)")
            text_content.append("=" * 30)
            text_content.append("")
            
            for i, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                if page_text:
                    text_content.append(f"--- Page {i+1} ---")
                    text_content.append(page_text)
                    text_content.append("")
                    
        return "\n".join(text_content)
    except Exception as e:
        logger.error(f"Error processing PDF: {e}")
        return None

async def process_excel(file_path: str) -> str:
    """Process Excel file and extract relevant information with proper structure including multiple sheets."""
    try:
        # Read all sheets
        excel_file = pd.ExcelFile(file_path)
        sheet_names = excel_file.sheet_names
        
        excel_data = []
        excel_data.append(f"Excel File Summary:")
        excel_data.append(f"Total Sheets: {len(sheet_names)}")
        excel_data.append("")
        
        # Process each sheet
        for sheet_name in sheet_names:
            excel_data.append(f"Sheet: {sheet_name}")
            excel_data.append("-" * (len(sheet_name) + 7))
            
            # Read specific sheet
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            
            # Add sheet information
            excel_data.append(f"  Rows: {len(df)}")
            excel_data.append(f"  Columns: {len(df.columns)}")
            excel_data.append("")
            
            # Add column information
            excel_data.append("  Columns:")
            for i, col in enumerate(df.columns):
                excel_data.append(f"    {i+1}. {col}")
            excel_data.append("")
            
            # For small datasets, include all data
            # For larger datasets, show first 20 rows and last 5 rows to give better context
            if len(df) > 0:
                if len(df) <= 30:
                    # For smaller datasets, show all data
                    excel_data.append("  All Data:")
                    excel_data.append("  ```")
                    
                    # Create a formatted table representation
                    # Header
                    header = " | ".join([str(col) for col in df.columns])
                    excel_data.append(f"  {header}")
                    excel_data.append("  " + "-" * len(header))
                    
                    # All data rows
                    for index, row in df.iterrows():
                        row_data = " | ".join([str(val) if pd.notna(val) else "" for val in row])
                        excel_data.append(f"  {row_data}")
                    
                    excel_data.append("  ```")
                else:
                    # For larger datasets, show first 20 rows and last 5 rows
                    excel_data.append(f"  Data (First 20 rows and last 5 rows of {len(df)} total rows):")
                    excel_data.append("  ```")
                    
                    # Create a formatted table representation
                    # Header
                    header = " | ".join([str(col) for col in df.columns])
                    excel_data.append(f"  {header}")
                    excel_data.append("  " + "-" * len(header))
                    
                    # First 20 data rows
                    for index, row in df.head(20).iterrows():
                        row_data = " | ".join([str(val) if pd.notna(val) else "" for val in row])
                        excel_data.append(f"  {row_data}")
                    
                    # Separator
                    excel_data.append("  ...")
                    excel_data.append("  (middle rows omitted for brevity)")
                    excel_data.append("  ...")
                    
                    # Last 5 data rows
                    for index, row in df.tail(5).iterrows():
                        row_data = " | ".join([str(val) if pd.notna(val) else "" for val in row])
                        excel_data.append(f"  {row_data}")
                    
                    excel_data.append("  ```")
            else:
                excel_data.append("  No data in this sheet")
            
            excel_data.append("")
            excel_data.append("  Column Data Types:")
            for col in df.columns:
                excel_data.append(f"    {col}: {df[col].dtype}")
            
            excel_data.append("")
            excel_data.append("=" * 50)
            excel_data.append("")
        
        return "\n".join(excel_data)
    except Exception as e:
        logger.error(f"Error processing Excel: {e}")
        return None

async def chat_with_gemini(message: str, user_id: int) -> str:
    """Chat with Gemini AI for general conversations with context tracking and web grounding"""
    try:
        language = get_user_language(user_id)
        lang_name = "English" if language == "en" else "Burmese"
        
        # Add user message to conversation history
        add_to_conversation(user_id, "user", message)
        
        # Get conversation history
        conversation = get_user_conversation(user_id)
        
        # Create prompt with context
        prompt = f"""You are a helpful financial assistant. Please respond to the user's message appropriately.
        Keep your responses concise and helpful.
        
        IMPORTANT: 
        1. Respond in {lang_name} language.
        2. Focus on financial topics when relevant
        3. Be helpful with general questions about finance, accounting, or document processing
        4. For current information, use web search to get up-to-date data
        
Conversation history:
{'\n'.join([f"{msg['role']}: {msg['parts'][0]}" for msg in conversation])}
        
User's latest message: {message}
        
Please provide a helpful and concise response with proper markdown formatting where appropriate."""
        
        # Use grounding model for general conversations to access current information
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=config,
        )
        
        # Add AI response to conversation history
        if response.text:
            add_to_conversation(user_id, "model", response.text)
        
        return response.text
    except Exception as e:
        logger.error(f"Error chatting with Gemini AI: {e}")
        return "Sorry, I encountered an error while processing your message."

async def batch_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start batch document processing mode."""
    try:
        user_id = update.effective_user.id
        language = get_user_language(user_id)
        
        # Initialize batch context
        initialize_batch_context(user_id)
        
        batch_msg = ("📁 Batch Processing Mode Activated!\n\n"
                     "Please upload multiple PDF and/or Excel files. I'll process them all and then you can ask me to compare them or analyze them together.\n\n"
                     "Commands:\n"
                     "- /batch_analyze - Analyze all uploaded files together\n"
                     "- /batch_clear - Clear the current batch\n"
                     "- /batch_status - Check the status of your batch")
        
        await update.message.reply_text(batch_msg)
    except Exception as e:
        logger.error(f"Error in batch_command: {e}")
        language = get_user_language(user_id)
        # Use plain text for error messages
        await update.message.reply_text(MESSAGES[language]['general_error'])

async def batch_analyze_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Analyze all files in the current batch."""
    try:
        user_id = update.effective_user.id
        language = get_user_language(user_id)
        
        batch_context = get_batch_context(user_id)
        if not batch_context or len(batch_context["files"]) == 0:
            await update.message.reply_text("❌ No files in batch. Please upload files first or use /batch to start.")
            return
        
        # Mark batch as processing
        user_batch_context[user_id]["processing"] = True
        
        # Create combined context for analysis
        combined_content = []
        combined_content.append(f"Batch Analysis ({len(batch_context['files'])} files)")
        combined_content.append("=" * 40)
        combined_content.append("")
        
        for i, file_info in enumerate(batch_context["files"], 1):
            combined_content.append(f"File {i}: {file_info['file_name']} ({file_info['file_type']})")
            combined_content.append("-" * 30)
            combined_content.append(file_info["content"])
            combined_content.append("")
            combined_content.append("=" * 40)
            combined_content.append("")
        
        combined_text = "\n".join(combined_content)
        
        # Store combined context for questions
        set_user_document_context(user_id, combined_text, "Batch")
        
        confirmation_msg = (f"✅ Batch of {len(batch_context['files'])} files processed successfully! "
                           "You can now ask me questions about all these documents together.")
        await update.message.reply_text(confirmation_msg)
    except Exception as e:
        logger.error(f"Error in batch_analyze_command: {e}")
        language = get_user_language(user_id)
        # Use plain text for error messages
        await update.message.reply_text(MESSAGES[language]['general_error'])

async def batch_clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Clear the current batch."""
    try:
        user_id = update.effective_user.id
        language = get_user_language(user_id)
        
        clear_batch_context(user_id)
        await update.message.reply_text("✅ Batch cleared successfully!")
    except Exception as e:
        logger.error(f"Error in batch_clear_command: {e}")
        language = get_user_language(user_id)
        # Use plain text for error messages
        await update.message.reply_text(MESSAGES[language]['general_error'])

async def batch_status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Check the status of the current batch."""
    try:
        user_id = update.effective_user.id
        language = get_user_language(user_id)
        
        batch_context = get_batch_context(user_id)
        if not batch_context:
            await update.message.reply_text("❌ No active batch. Use /batch to start.")
            return
        
        # Build status message
        status_msg = "📁 Batch Status\n\n"
        status_msg += f"Files processed: {len(batch_context['files'])}\n\n"
        
        if batch_context['files']:
            status_msg += "Files in batch:\n"
            for i, file_info in enumerate(batch_context['files'], 1):
                status_msg += f"{i}. {file_info['file_name']} ({file_info['file_type']})\n"
        
        status_msg += "\nUse /batch_analyze to analyze all files together."
        
        await update.message.reply_text(status_msg)
    except Exception as e:
        logger.error(f"Error in batch_status_command: {e}")
        language = get_user_language(user_id)
        # Use plain text for error messages
        await update.message.reply_text(MESSAGES[language]['general_error'])

async def answer_document_question(question: str, user_id: int) -> str:
    """Answer user questions about processed documents with grounding for current info."""
    try:
        language = get_user_language(user_id)
        lang_name = "English" if language == "en" else "Burmese"
        
        # Get document context
        doc_context = get_user_document_context(user_id)
        if not doc_context:
            return "Please upload a document first before asking questions about it."
        
        prompt = f"""You are a financial document assistant. Please answer the user's question about the financial document they uploaded.
        
User's question: {question}
        
Document content: {doc_context['content'][:15000]}  # Increased limit for better context
        
Document type: {doc_context['file_type']}
        
IMPORTANT: 
1. The document content is provided in a structured format to help you understand the data
2. For Excel files, you'll see column names and sample data in a table format
3. For PDF files, you'll see text organized by pages
4. Respond in {lang_name} language.
5. Provide specific, accurate answers based on the document content
6. If the question cannot be answered with the provided data, say so clearly
7. If the question asks about current/recent financial data, use web search to get up-to-date information
        
Please provide a focused and helpful response to the user's question."""
        
        # Use grounding model for all document questions to access current information
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=config,
        )
            
        return response.text
    except Exception as e:
        logger.error(f"Error answering document question: {e}")
        return "Sorry, I encountered an error while processing your question."

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming documents."""
    try:
        user_id = update.effective_user.id
        language = get_user_language(user_id)
        
        # Check if this is part of a batch upload
        batch_context = get_batch_context(user_id)
        
        # Get file details
        file = await update.message.document.get_file()
        file_name = update.message.document.file_name.lower()
        
        # Send acknowledgment
        if not batch_context or not batch_context.get("processing", False):
            await update.message.reply_text(MESSAGES[language]['processing'])
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            await file.download_to_drive(temp_file.name)
            
            # Process based on file type
            if file_name.endswith('.pdf'):
                content = await process_pdf(temp_file.name)
                file_type = "PDF"
            elif file_name.endswith(('.xls', '.xlsx')):
                content = await process_excel(temp_file.name)
                file_type = "Excel"
            else:
                await update.message.reply_text(MESSAGES[language]['unsupported_format'], parse_mode='Markdown')
                return
            
            # Remove temporary file
            os.unlink(temp_file.name)
            
            if content:
                # Add to batch context if processing multiple files
                if batch_context:
                    add_to_batch_context(user_id, file_name, content, file_type)
                    # Check if user wants to analyze the batch
                    if batch_context.get("processing", False):
                        # User has indicated they want to analyze the batch
                        batch_info = f"✅ Added {file_type} file: {file_name} to batch. {len(batch_context['files'])} files processed so far."
                        await update.message.reply_text(batch_info)
                else:
                    # Single file processing
                    set_user_document_context(user_id, content, file_type)
                    
                    # Send confirmation that document is ready for questions
                    confirmation_msg = f"✅ {file_type} file processed successfully! You can now ask me questions about this document."
                    await update.message.reply_text(confirmation_msg)
            else:
                await update.message.reply_text(MESSAGES[language]['processing_error'])
                
    except Exception as e:
        logger.error(f"Error handling document: {e}")
        user_id = update.effective_user.id
        language = get_user_language(user_id)
        await update.message.reply_text(MESSAGES[language]['general_error'])

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text messages."""
    user_id = update.effective_user.id
    language = get_user_language(user_id)
    user_message = update.message.text
    
    if user_message.lower() in ['hi', 'hello', 'hey']:
        await update.message.reply_text(MESSAGES[language]['greeting'])
    else:
        # Check if user has a document context to ask questions about
        doc_context = get_user_document_context(user_id)
        if doc_context:
            # User is asking a question about their document
            response = await answer_document_question(user_message, user_id)
            try:
                await update.message.reply_text(response)
            except:
                # If markdown fails, send as plain text
                await update.message.reply_text(response)
        else:
            # General chat when no document is processed
            response = await chat_with_gemini(user_message, user_id)
            try:
                await update.message.reply_text(response)
            except:
                # If markdown fails, send as plain text
                await update.message.reply_text(response)

def main():
    """Start the bot."""
    # Create application and pass bot token
    application = Application.builder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("english", english_command))
    application.add_handler(CommandHandler("burmese", burmese_command))
    application.add_handler(CommandHandler("batch", batch_command))
    application.add_handler(CommandHandler("batch_analyze", batch_analyze_command))
    application.add_handler(CommandHandler("batch_clear", batch_clear_command))
    application.add_handler(CommandHandler("batch_status", batch_status_command))
    application.add_handler(CommandHandler("search", search_command))
    application.add_handler(CommandHandler("menu", menu_command))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()