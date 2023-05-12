#! python3
# random_chore.py — An exercise in using python to automate email.
# For more information, see project_details.txt.

import os
import logging
import random
import smtplib
from email.message import EmailMessage


logging.basicConfig(
    level=logging.DEBUG,
    filename="logging.txt",
    format="%(asctime)s -  %(levelname)s -  %(message)s",
)
# logging.disable(logging.CRITICAL)  # Note out to enable logging.

EMAIL_HOST = os.environ.get("ICLD_SMTP")
EMAIL_ADDRESS = os.environ.get("ICLD_USER")
EMAIL_PASSWORD = os.environ.get("ICLD_PASS")
FRST_ADDY = os.environ.get("TOTA_USER")
SCND_ADDY = os.environ.get("AUTO_USER")

recipients_list = [
    FRST_ADDY,
    SCND_ADDY,
    EMAIL_ADDRESS,
]

chores_list = ["wash dishes", "clean bathroom", "vaccum house"]

chore_assignments = {}


def choose_chore():
    random_chore = random.choice(chores_list)
    return random_chore


def remove_chore(chore):
    chores_list.remove(chore)
    return chores_list


for recipient in recipients_list:
    chore_assignment = choose_chore()
    remove_chore(chore_assignment)
    chore_assignments[recipient] = [chore_assignment]

logging.info(chore_assignments)

for key, value in chore_assignments.items():
    msg = EmailMessage()
    msg["Subject"] = "You chore for the week."
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = key
    msg.set_content(f"Your chore for the week is: {value}")

    with smtplib.SMTP("smtp.mail.me.com", 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
