from dotenv import load_dotenv
load_dotenv()

from src.fetch_deals import get_recent_deals_grouped_by_owner
from src.engagements import fetch_engagements_for_deal
from src.analyze_deals import analyze_deals
from src.emailer import send_email_with_csv
import time

def safe_send_email(email, deals, role, metrics=None):
    try:
        send_email_with_csv(email, deals, role, metrics=metrics)
        print(f"✅ Email sent to {email}")
    except Exception as e:
        print(f"❌ First attempt failed to send email to {email}: {e}")
        print("🔁 Retrying in 5 seconds...")
        time.sleep(5)
        try:
            send_email_with_csv(email, deals, role, metrics=metrics)
            print(f"✅ Email sent to {email} on retry")
        except Exception as e2:
            print(f"❌ Retry also failed for {email}: {e2}")

def run():
    print("🚀 Fetching deals...")
    deals_by_owner = get_recent_deals_grouped_by_owner()

    if not deals_by_owner:
        print("⚠️ No deals found. Exiting.")
        return

    print("📩 Fetching engagements...")
    all_deals = []
    for owner_email, deals in deals_by_owner.items():
        for deal in deals:
            timestamps, last_note = fetch_engagements_for_deal(deal["id"], deal["name"])
            deal["engagements"] = timestamps
            deal["last_note"] = last_note
            all_deals.append(deal)

    print(f"🧠 Analyzing {len(all_deals)} deals...")
    alert_map, metrics_by_owner = analyze_deals(all_deals)

    for deal in all_deals:
        deal["alerts"] = alert_map.get(deal["id"], [])
        deal["metrics"] = metrics_by_owner.get(deal.get("owner_email", "").lower(), {})

    alerts_by_owner = {}
    for deal in all_deals:
        if not deal.get("alerts"):
            continue
        owner_email = deal.get("owner_email", "").lower()
        if owner_email:
            alerts_by_owner.setdefault(owner_email, []).append(deal)

    print("\n📬 Will send to Deal Owners:")
    for email, deals in alerts_by_owner.items():
        print(f"   - {email} ({len(deals)} deal(s))")

    specific_owners = {
        "noyal.saharan@prozo.com",
        "shaikh.quamar@prozo.com",
        "nikhil.patle@prozo.com",
        "vishal.labh1@prozo.com",
        "kuldeep.thakran@prozo.com",
        "sushma.chauhan@prozo.com",
        "divij.wadhwa@prozo.com"
    }

    print("\n📧 Sending Deal Owner emails to selected owners only...")
    for email, deals in alerts_by_owner.items():
        if email in specific_owners:
            safe_send_email(email, deals, role="OWNER", metrics=metrics_by_owner.get(email.lower(), {}))

    print("\n📧 Sending summary email to Kuldeep...")
    all_alerted_deals = [deal for deal in all_deals if deal.get("alerts")]
    safe_send_email("kuldeep.thakran@prozo.com", all_alerted_deals, role="SUMMARY")

    print("✅ Process complete. Exiting.")


# Only run locally if executed directly
if __name__ == "__main__":
    run()
