import openai
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Set up OpenAI API key
openai.api_key = 'your_openai_api_key'  # Replace with your actual OpenAI API key

# Load leads data from CSV file
leads_data = pd.read_csv('/workspaces/AI-Automated-Lead-Generation-System/Data/leads_data.csv')  # Update with your actual CSV file path

# Generate personalized emails
def generate_email(company_name, description, keywords):
    prompt = (
        f"Write a personalized email to the company {company_name}. "
        f"Highlight the benefits of our AI-driven marketing solutions. "
        f"Make sure to reference their business focus as described: '{description}'. "
        f"Include keywords such as {keywords} to align with their needs. "
        "Keep the tone friendly and professional."
    )
    response = openai.Completion.create(
        engine="text-davinci-003",  # Choose the appropriate model
        prompt=prompt,
        max_tokens=200
    )
    return response.choices[0].text.strip()

# SMTP email setup (Example with Gmail)
def send_email(to_address, subject, body, from_address='your_email@gmail.com', smtp_server='smtp.gmail.com', smtp_port=587):
    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = from_address
    message['To'] = to_address
    message['Subject'] = subject

    # Add body to email
    message.attach(MIMEText(body, 'plain'))

    # Use credentials to log in to the SMTP server
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(from_address, 'your_email_password')  # Use app-specific password if using Gmail
        text = message.as_string()
        server.sendmail(from_address, to_address, text)

# Iterate through your classified leads data and generate/send emails
for index, row in leads_data.iterrows():
    company_name = row['Company Name for Emails']
    description = row['Short Description']
    keywords = row.get('Keywords', 'No specific keywords listed')  # Handle missing keywords gracefully
    email = row['Email']  # Assuming your CSV includes an 'Email' column
    subject = 'Discover How AI Can Transform Your Business'
    personalized_email = generate_email(company_name, description, keywords)
    
    # Send the personalized email
    send_email(to_address=email, subject=subject, body=personalized_email)

    print(f"Email sent to {company_name} ({email})")
