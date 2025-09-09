MESSAGES = {
    "en": {
        "welcome": "*👋 Welcome to the Financial Document Assistant Bot!*\n\nI'm a specialized financial assistant that can help you process and analyze PDF and Excel documents.\n\n*How to use me:*\n1. Upload a PDF or Excel file and ask questions about it\n2. *Or* use `/batch` to process multiple files and analyze them together\n\n*Commands:*\n`/start` - Start the bot\n`/help` - Show this help message\n`/batch` - Process multiple files together\n`/english` - Switch to English\n`/burmese` - မြန်မာဘာသာဖြင့် ဆက်လက်ဆောင်ရွက်ရန်",
        "help": "*🤖 Financial Document Assistant Bot Help*\n\n*Commands:*\n`/start` - Start the bot\n`/help` - Show this help message\n`/batch` - Process multiple files together\n`/batch_analyze` - Analyze all uploaded files together\n`/batch_clear` - Clear the current batch\n`/batch_status` - Check the status of your batch\n`/search <query>` - Search the web for current information\n`/english` - Switch to English\n`/burmese` - Switch to Burmese\n\n*How to use:*\n1. Upload a PDF or Excel file and ask questions about it\n2. *Or* use `/batch` to process multiple files:\n   - Type `/batch` to start batch mode\n   - Upload multiple files\n   - Type `/batch_analyze` to analyze them together\n\n*Supported file types:*\n• PDF (.pdf)\n• Excel (.xls, .xlsx)\n\n*Examples of questions you can ask:*\n• \"What is the total revenue?\"\n• \"List all transactions over $1000\"\n• \"Show me all expense categories\"\n• \"What was the highest expense?\"\n• \"Compare the revenue in these files\"\n• \"Find duplicate entries between documents\"\n\nJust upload your document(s) and ask me anything!\n\n*Note: I automatically search the web for current financial information when needed.*",
        "processing": "*📥 Processing your document...* Please wait.",
        "analyzing": "*✅ {} file processed successfully!* You can now ask me questions about this document.",
        "unsupported_format": "*❌ Unsupported file format.* Please send PDF or Excel files only.",
        "processing_error": "*❌ Error processing the file.* Please try again.",
        "general_error": "*❌ Sorry, something went wrong.* Please try again later.",
        "greeting": "*👋 Hi!* I'm your Financial Document Assistant. Upload a PDF or Excel file, then ask me questions about it!",
        "send_document": "Please upload a PDF or Excel file, then ask me questions about it!",
        "language_changed": "*🇺🇸 Language changed to English!*"
    },
    "my": {
        "welcome": "*👋 မင်္ဂလာပါ Financial Document Assistant Bot မှ ကြိုဆိုပါတယ်!*\n\nကျွန်တော်သည် PDF နှင့် Excel ဖိုင်များကို စိစစ်ပေးနိုင်သော ငွေကြေးဆိုင်ရာ ကူညီသူ အထူးလုပ်ဖော်ပါ။\n\n*အသုံးပြုနည်း:*\n၁။ PDF သို့မဟုတ် Excel ဖိုင်ကို ပို့ပြီး သင့်ဖိုင်အကြောင်း မေးပါ\n၂။ *သို့မဟုတ်* ဖိုင်များစုစည်း၍ စိစစ်ရန် `/batch` ကို အသုံးပြုပါ\n\n*Commands:*\n`/start` - Bot ကို စတင်အသုံးပြုရန်\n`/help` - အကူအညီကြည့်ရန်\n`/batch` - ဖိုင်များစုစည်း၍ စိစစ်ရန်\n`/english` - Switch to English\n`/burmese` - မြန်မာဘာသာဖြင့် ဆက်လက်ရန်",
        "help": "*🤖 အကူအညီ*\n\n*Commands များ:*\n`/start` - Bot ကို စတင်အသုံးပြုရန်\n`/help` - အကူအညီကြည့်ရန်\n`/batch` - ဖိုင်များစုစည်း၍ စိစစ်ရန်\n`/batch_analyze` - ဖိုင်အားလုံးကို စုစည်း၍ စိစစ်ရန်\n`/batch_clear` - လက်ရှိဖိုင်စုကို ရှင်းလင်းရန်\n`/batch_status` - ဖိုင်စု၏ အခြေအနေကို ကြည့်ရန်\n`/search <query>` - အင်တာနက်တွင် အချက်အလက်များကို ရှာဖွေရန်\n`/english` - အင်္ဂလိပ်ဘာသာသို့ ပြောင်းရန်\n`/burmese` - မြန်မာဘာသာသို့ ပြောင်းရန်\n\n*အသုံးပြုနည်း:*\n၁။ PDF သို့မဟုတ် Excel ဖိုင်ကို ပို့ပြီး သင့်ဖိုင်အကြောင်း မေးပါ\n၂။ *သို့မဟုတ်* ဖိုင်များစုစည်း၍ စိစစ်ရန်:\n   - ပထမ `/batch` ကို ရိုက်ပါ\n   - ဖိုင်များကို ပို့ပါ\n   - နောက် `/batch_analyze` ကို ရိုက်၍ စုစည်းစိစစ်ပါ\n\n*လက်ခံသော ဖိုင်အမျိုးအစားများ:*\n• PDF (.pdf)\n• Excel (.xls, .xlsx)\n\n*မေးနိုင်သော မေးခွန်းများ ဥပမာများ:*\n• \"စုစုပေါင်းဝင်ငွေက ဘာလဲ?\"\n• \"၁၀၀၀ ဒေါ်လာထက်ပိုသော ငွေသွင်းအားလုံးကို ပြပါ\"\n• \"အသုံးစရိတ်အမျိုးအစားအားလုံးကို ပြပါ\"\n• \"အမြင့်ဆုံးအသုံးစရိတ်က ဘာလဲ?\"\n• \"ဤဖိုင်များတွင် ဝင်ငွေကို နှိုင်းယှဉ်ပါ\"\n• \"ဖိုင်များကြား ထပ်တူအင်အားလုံးကို ရှာပါ\"\n\nသင့်ဖိုင်(များ)ကို ပို့ပြီး မေးခွန်းများမေးပါ!\n\n*Note: လိုအပ်သလို ငွေကြေးဆိုင်ရာ အချက်အလက်များအတွက် အင်တာနက်ကို အလိုအလျောက်ရှာဖွေပေးပါမည်။*",
        "processing": "*📥 စာရွက်စာတမ်းကို စစ်ဆေးနေပါသည်...* ခဏစောင့်ပါ။",
        "analyzing": "*✅ {} ဖိုင်ကို အောင်မြင်စွာ ဖတ်ရှုပြီးပါပြီ!* ယခု သင့်ဖိုင်အကြောင်း မေးခွန်းများမေးနိုင်ပါပြီ။",
        "unsupported_format": "*❌ PDF သို့မဟုတ် Excel ဖိုင်များကိုသာ ပို့ပေးပါ။*",
        "processing_error": "*❌ ဖိုင်စစ်ဆေးရာတွင် အမှားရှိနေပါသည်။* ထပ်မံကြိုးစားကြည့်ပါ။",
        "general_error": "*❌ တစ်ခုခုမှားယွင်းနေပါသည်။* နောက်မှ ထပ်စမ်းကြည့်ပါ။",
        "greeting": "*👋 မင်္ဂလာပါ!* ကျွန်တော်က Financial Document Assistant ပါ။ PDF သို့မဟုတ် Excel ဖိုင်ပို့ပြီး သင့်ဖိုင်အကြောင်း မေးပါ!",
        "send_document": "ကျေးဇူးပြု၍ PDF သို့မဟုတ် Excel ဖိုင်ပို့ပြီး သင့်ဖိုင်အကြောင်း မေးပါ!",
        "language_changed": "*🇲🇲 မြန်မာဘာသာသို့ ပြောင်းလဲပြီးပါပြီ!*"
    }
}