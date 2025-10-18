import requests
import datetime

# Permanent Meta Access Token
ACCESS_TOKEN = "EAAWkjh4z25EBPvJVvQyaJObqjkjhnk5pnul433cZAk0xBwilQyQu0dsVXBsa40nUMBxhrn54LXiYIgC6oT4NP4bGeS1NnZA5G4j5v37Rjko5mlPr72q3F39YAGnahoa1DKzrhANoXtsRtcLSB025ocAgghiXRlpcaB2FZCpRcH3EH1ZCE6ELElblzTu7ZC3W0LyZA8hau1n2cB1tffy0mLRffZC90RPBZAQVFVg45KKo"

PHONE_NUMBER_ID = "886911787831711"

# WhatsApp Numbers to Send (comma separated)
RECIPIENTS = ["919666766656", "919032958626"]  # Replace with yours and your partner's

def send_whatsapp_message():
    today = datetime.date.today()
    summary_message = f"""👋 Hello Hari!

Your Timerio WhatsApp Alert System is LIVE!

📊 Yesterday’s summary ({today - datetime.timedelta(days=1)}):
Sales: ₹1,50,000
Transactions: 230
Avg Ticket Size: ₹652

This is an automated message from Timerio AI Analytics."""
    
    url = f"https://graph.facebook.com/v21.0/{PHONE_NUMBER_ID}/messages"
    
    for number in RECIPIENTS:
        payload = {
            "messaging_product": "whatsapp",
            "to": number,
            "type": "text",
            "text": {"body": summary_message}
        }
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        response = requests.post(url, json=payload, headers=headers)
        print(number, response.status_code, response.text)

if __name__ == "__main__":
    send_whatsapp_message()
