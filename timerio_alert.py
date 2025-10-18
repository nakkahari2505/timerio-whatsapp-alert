import pandas as pd
from datetime import datetime, timedelta
import requests
import os

# === WhatsApp API Setup ===
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
RECIPIENT_PHONE = os.getenv("RECIPIENT_NUMBER")

# === Read data ===
df = pd.read_excel("Sale_Oct.xlsx")

# Clean Sale column (remove commas, ensure numeric)
df["Sale"] = df["Sale"].astype(str).str.replace(",", "").astype(float)

# Convert Date column to datetime
df["Date"] = pd.to_datetime(df["Date"], errors="coerce", format="%m/%d/%Y")

# === Filter Dates ===
today = datetime.now().date()
yesterday = today - timedelta(days=1)
last_week_same_day = yesterday - timedelta(days=7)

# Yesterday data
df_yest = df[df["Date"].dt.date == yesterday]

# Last week same weekday data
df_last_week = df[df["Date"].dt.date == last_week_same_day]

# === Company-level summary ===
total_sales = df_yest["Sale"].sum()
txn_count = df_yest["Txn_No"].nunique()
ticket_size = round(total_sales / txn_count, 2) if txn_count > 0 else 0

last_week_sales = df_last_week["Sale"].sum()
growth = ((total_sales - last_week_sales) / last_week_sales * 100) if last_week_sales > 0 else 0

# === Branch-level summary ===
branch_summary = []
for branch, sub in df_yest.groupby("Branch"):
    branch_sales = sub["Sale"].sum()
    branch_txns = sub["Txn_No"].nunique()
    branch_ticket = round(branch_sales / branch_txns, 2) if branch_txns > 0 else 0

    last_week_branch_sales = df_last_week[df_last_week["Branch"] == branch]["Sale"].sum()
    branch_growth = ((branch_sales - last_week_branch_sales) / last_week_branch_sales * 100) if last_week_branch_sales > 0 else 0

    branch_summary.append(f"🏢 *{branch}* → ₹{branch_sales:.0f} | {branch_txns} Txns | ₹{branch_ticket:.0f}/Txn | {branch_growth:+.1f}%")

# === Format message ===
message = (
    f"📊 *Timerio Daily Diagnostic Summary* ({yesterday.strftime('%d-%b-%Y')})\n\n"
    f"🏬 *Overall* → ₹{total_sales:.0f} | {txn_count} Txns | ₹{ticket_size:.0f}/Txn | {growth:+.1f}% vs LYD\n\n"
    + "\n".join(branch_summary)
    + "\n\n#TimerioAutoAlert"
)

# === Send WhatsApp message ===
url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}
payload = {
    "messaging_product": "whatsapp",
    "to": RECIPIENT_PHONE,
    "type": "text",
    "text": {"body": message}
}

response = requests.post(url, headers=headers, json=payload)
print(response.status_code, response.text)
