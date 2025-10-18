import requests
import datetime

# Permanent Meta Access Token
ACCESS_TOKEN = "EAAWkjh4z25EBPqj5wA15sQmjbL7WdamyKsGDCEn3Mvt69IIZBYdHumVljxPAaitn3P2Ygg8jNo71HYr7i0KvwhcN1EHKrPpYJOFdUPZAXIv8oNGJjvRSCEwmV2mzgMEYAKsq9KOFomNsxnNQgScWfYMH5OqGtj2wX2kPaqZBkIycXlQKs5qt2Clh9gpt6W77gZDZD"

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
