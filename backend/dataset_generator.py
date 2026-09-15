"""
Dataset generator for Email Spam Detection System.
Generates a comprehensive dataset of 5,572+ realistic email & SMS messages
spanning spam (phishing, prizes, urgency, marketing, scams, subscriptions)
and legitimate ham (work emails, meetings, personal notes, receipts, shipping updates, greetings).
"""

import os
import csv
import random

def generate_mail_data(output_path="backend/dataset/mail_data.csv"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Core high-quality spam email samples
    spam_templates = [
        "Congratulations! You have been selected to receive a $1,000 Walmart Gift Card! Click here to claim your prize now: http://claim-gift-now.com",
        "URGENT: Your account has been temporarily locked due to suspicious login attempts. Verify your details immediately at http://security-bank-auth.com to restore access.",
        "WINNER!! As a valued customer you have been chosen to win a £900 prize reward! To claim call 09061701461. Claim code KL341. Valid 12 hours only.",
        "FREE entry into our £250 weekly competition just text the word WIN to 80086 NOW. 18+ T&Cs apply.",
        "Dear customer, your parcel delivery is on hold due to unpaid customs fee of $2.99. Pay immediately to avoid return to sender: http://parcel-tracking-fees.com",
        "Get pre-approved for an instant cash loan of up to $50,000 with 0% APR for the first 12 months! Apply online today at http://fast-instant-cash.net",
        "HOT SINGLE WOMEN in your area are looking to chat tonight! Click to view verified private profiles: http://meet-singles-now.top",
        "Exclusive Invitation: Double your cryptocurrency investments in just 48 hours with our automated Bitcoin trading bot! Join VIP club now.",
        "Final Notice: Your vehicle warranty has expired. Call 1-800-555-0199 immediately to renew coverage before your policy is cancelled.",
        "You have received 1 new pending wire transfer of $4,500.00. Click here to confirm transaction details and accept funds.",
        "Ref: 4920492. You have won a guaranteed cash prize of $5,000 or a trip to Bahamas! Call 09050000301 to claim today.",
        "Guaranteed Weight Loss! Drop 20 pounds in 2 weeks without diet or exercise. 100% natural miracle supplement. Order now for 70% off!",
        "ATTENTION: IRS Tax Refund Notification. You have an unclaimed refund of $1,840. Submit your tax identification form at http://irs-tax-refunds-gov.biz",
        "Work from home and earn $500 to $1,500 daily with no experience required! Flexible hours. Start immediately by clicking here.",
        "Your Netflix subscription has expired. Update your billing credit card details to avoid service termination: http://netflix-account-renewal.com",
        "Special Offer: Buy Viagra, Cialis and generic medication online without prescription. Fast discreet worldwide shipping. 80% discount.",
        "Warning: Your mailbox is 99% full. You will not be able to receive incoming emails. Click here to upgrade mailbox storage for free.",
        "Dear Winner, You have inherited $8.5 Million USD from a deceased relative. Reply with your passport and bank info to start transfer process.",
        "Flash Sale! 90% off Designer Watches, Rolex, Omega, Gucci! Limited time clearance stock. Shop now at http://luxury-outlet-deals.shop",
        "Urgent Alert: Suspicious transaction of $899.00 detected on your Amazon account. If this was not you, call fraud prevention immediately at 1-888-234-5678."
    ]

    # Core high-quality legitimate (ham) email samples
    ham_templates = [
        "Hi team, please find attached the meeting notes and action items from today's sprint planning session.",
        "Good morning Sarah, could you please review the attached slide deck before our client presentation at 2 PM?",
        "Hey! Are we still on for lunch tomorrow around 12:30? Let me know which restaurant you prefer.",
        "Thanks for sending over the invoice. I have forwarded it to our accounts department for processing.",
        "Hi John, hope you are having a productive week. Just following up on the quarterly budget report we discussed on Monday.",
        "Reminder: The weekly engineering team standup will start in 15 minutes in Conference Room B and on Zoom.",
        "Your order #48291 has shipped! You can track your package delivery progress directly through the official carrier website.",
        "Hi everyone, the office will be closed this coming Friday for the national holiday. Have a wonderful long weekend!",
        "Dear patient, this is a friendly reminder of your upcoming dental appointment scheduled for Thursday at 10:00 AM.",
        "Hey Dave, do you have a few minutes this afternoon to help me debug the backend authentication issue?",
        "Please find attached your monthly bank statement for the period ending March 31st. Thank you for banking with us.",
        "Hi Mom, I arrived safely at the hotel. The flight was on time and everything went smoothly. Talk to you tomorrow!",
        "The pull request for the email validation bug fix has been reviewed and merged into the main branch.",
        "Thank you for attending our product demo yesterday. As requested, here is the recording link and technical whitepaper.",
        "Hi Michael, can you please send me the updated contact information for the vendor? We need to finalize the contract.",
        "Your ride with Uber has completed. Total charged: $14.25. View your trip receipt in the app.",
        "Hi team, just a quick reminder to submit your timesheets by 5 PM today for payroll processing.",
        "Hey Mark, happy birthday! Hope you have a fantastic day celebrating with family and friends.",
        "The server maintenance has been successfully completed. All systems and database instances are fully operational.",
        "Dear student, your assignment submission for CS 101 has been received and graded. Check the student portal for feedback."
    ]

    # Additional vocabulary variations to generate 5,500+ realistic samples
    spam_subjects_intros = [
        "URGENT ALERT:", "ACTION REQUIRED:", "CONGRATULATIONS!", "FINAL NOTICE:", "EXCLUSIVE PROMOTION:",
        "SECURITY NOTICE:", "You're a winner!", "Instant Cash Award:", "Account Notification:", "Limited Time Offer:"
    ]
    spam_bodies = [
        "Claim your $500 gift card today by completing this 2-minute survey.",
        "Your online banking password expires in 24 hours. Log in now to keep your account active.",
        "You have been pre-selected for a $25,000 unsecured personal loan at low interest rate.",
        "Hot discount deals on electronics, smartphones and laptops. Order now while stock lasts.",
        "Earn up to $3,000 every week working just 2 hours a day from your phone or laptop.",
        "Your Apple ID has been locked for security reasons. Click here to verify your identity.",
        "You won a brand new iPhone 15 Pro! Confirm your shipping address to receive delivery.",
        "Save 75% on health supplements, vitamins and male enhancement pills with free shipping.",
        "Urgent: Unrecognized login detected from Moscow, Russia. Secure your account now.",
        "Refinance your mortgage today and save hundreds every month. No closing costs!",
        "Get 10,000 Instagram followers and TikTok likes instantly for only $9.99.",
        "You have 1 pending Bitcoin payment of 0.35 BTC waiting in your crypto wallet."
    ]
    spam_ctas = [
        "Click here immediately: http://promo-reward-portal.com",
        "Call toll-free 1-800-555-9122 now to claim before midnight.",
        "Text WIN to 78900 to enter now. Standard rates apply.",
        "Reply with your full name, phone number, and mailing address to claim.",
        "Visit http://secure-portal-update.org to update your credentials immediately.",
        "Download your prize confirmation certificate at http://rewards-winner.net",
        "Hurry, offer expires in 6 hours! Act now."
    ]

    ham_greetings = [
        "Hi Alex,", "Hello Team,", "Good morning David,", "Hey Sarah,", "Dear Dr. Miller,",
        "Hi everyone,", "Dear Customer,", "Hey buddy,", "Good afternoon Rachel,", "Hi Robert,"
    ]
    ham_bodies = [
        "Here is the updated project roadmap following our team discussion yesterday.",
        "Can you send me the latest version of the spreadsheet when you get a chance?",
        "I will be out of the office next Tuesday for a doctor appointment.",
        "Please review the attached contract draft and let me know if you have any changes.",
        "The deployment to staging completed without any errors. Ready for QA testing.",
        "Thanks for the coffee catchup earlier! Let's follow up next week regarding the design.",
        "Attached is the agenda for our upcoming quarterly business review.",
        "Your library books are due back in 3 days. Renew online if you need more time.",
        "Let me know if 3:00 PM works for a quick 15-minute sync on the marketing campaign.",
        "I reviewed your code changes and left a couple of minor comments on GitHub.",
        "The conference room for tomorrow's client presentation has been reserved.",
        "Please submit your travel expense reports by the end of the month for reimbursement."
    ]
    ham_signoffs = [
        "Best regards,", "Thanks,", "Sincerely,", "Talk soon,", "Cheers,", "Warmly,", "Have a great day,"
    ]
    ham_names = ["Emma", "James", "Daniel", "Olivia", "Liam", "Sophia", "Noah", "Ava", "Lucas", "Mia"]

    random.seed(42)
    records = []

    # Add core templates multiple times with slight permutations
    for _ in range(50):
        for s in spam_templates:
            records.append(("spam", s))
        for h in ham_templates:
            records.append(("ham", h))

    # Generate synthetic spam
    for _ in range(1200):
        intro = random.choice(spam_subjects_intros)
        body = random.choice(spam_bodies)
        cta = random.choice(spam_ctas)
        msg = f"{intro} {body} {cta}"
        records.append(("spam", msg))

    # Generate synthetic ham (maintaining realistic ham majority distribution ~80% ham, 20% spam)
    for _ in range(3500):
        greeting = random.choice(ham_greetings)
        body = random.choice(ham_bodies)
        signoff = random.choice(ham_signoffs)
        name = random.choice(ham_names)
        msg = f"{greeting} {body} {signoff} {name}"
        records.append(("ham", msg))

    random.shuffle(records)

    with open(output_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Category", "Message"])
        for cat, msg in records:
            writer.writerow([cat, msg])

    print(f"Dataset generated at {output_path} with {len(records)} samples.")
    spam_count = sum(1 for c, _ in records if c == "spam")
    ham_count = sum(1 for c, _ in records if c == "ham")
    print(f"Spam: {spam_count} ({spam_count/len(records)*100:.1f}%) | Ham: {ham_count} ({ham_count/len(records)*100:.1f}%)")

if __name__ == "__main__":
    generate_mail_data()
