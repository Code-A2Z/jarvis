import smtplib
from email.mime.text import MIMEText

import streamlit as st


def EMail():
  st.markdown("#### Welcome to E-mail Automation")
  senderEmail = st.text_input("Enter your E-mail Address")
  passWord = st.text_input("Enter your Password", type="password")

  receiverEmails = st.text_area("Enter the Recipient's E-mail Addresses (separated by commas)").split(",")
  message = MIMEText(st.text_area("Enter the body of the mail"))
  message["From"] = senderEmail
  message["To"] = ", ".join(receiverEmails)
  message["Subject"] = st.text_input("Enter the Subject of the mail", value="Automated Email")

  if st.button("Send Mail"):
    if senderEmail != "" and passWord != "" and receiverEmails != [] and message != "":
      receiverEmail = receiverEmails.strip()
      server = smtplib.SMTP("smtp.gmail.com", 587)
      server.ehlo()
      server.starttls()
      server.login(senderEmail, passWord)
      server.sendmail(senderEmail, receiverEmail, message.as_string())
      server.close()
      st.success("E-mail has sent successfully!", icon="✅")
    else:
      st.error("Please provide all the details.", icon="🚨")
  st.info(
    """Switch on the 'Less secure app access' of sender's mail by using this [link](https://myaccount.google.com/lesssecureapps?pli=1&rapt=AEjHL4MWL7anq0zxK7rt3arv3YBLKrAswWmAWqOkIUCd0qKKHlpQyezvEt2ruMNK2BaXddqMJlydydf-quRjLpwabeoLI_tZ3Q).""",
    icon="ℹ️",
  )
