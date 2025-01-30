import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from datetime import datetime
import os
import dotenv
import re
from pathlib import Path
import os.path
import json

dotenv.load_dotenv()

def validate_email(email):
    """Validate email format using regex pattern."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_url(url):
    """Basic URL validation."""
    return url.startswith(('http://', 'https://')) if url else True

def send_job_email(sender_email, sender_password, recipient_email, job_details, language='en', pdf_path=None):
    """
    Send job application email with formatted HTML content and optional PDF attachment.
    
    Args:
        sender_email (str): Email address of the sender
        sender_password (str): Password for sender's email
        recipient_email (str): Email address of the recipient
        job_details (dict): Dictionary containing job application details
        language (str): Language code ('en' for English, 'it' for Italian)
        pdf_path (str, optional): Path to PDF file to attach
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    if not all([sender_email, sender_password, recipient_email]):
        raise ValueError("Missing required email credentials")
    
    if not validate_email(recipient_email):
        raise ValueError("Invalid recipient email format")

    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    templates = {
        'en': {
            'submitted_on': "Submitted on",
            'header': "Job Application Details",
            'footer': "This is an automated email from the Job Application System"
        },
        'it': {
            'submitted_on': "Inviato il",
            'header': "Dettagli Candidatura Lavoro",
            'footer': "Questa è un'email automatica dal Sistema di Candidatura Lavoro"
        }
    }
    
    t = templates[language]

    message = MIMEMultipart("alternative")
    message["Subject"] = f"New Job Application - {datetime.now().strftime('%Y-%m-%d')}"
    message["From"] = sender_email
    message["To"] = recipient_email

    html_template = f"""
    <html>
        <head>
            <style>
                body {{
                    font-family: 'Segoe UI', Arial, sans-serif;
                    line-height: 1.6;
                    color: #2c3e50;
                    background-color: #f0f2f5;
                    margin: 0;
                    padding: 20px;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    background: white;
                    border-radius: 8px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    overflow: hidden;
                }}
                .header {{
                    background: #4a90e2;
                    color: white;
                    padding: 20px;
                    text-align: center;
                }}
                .header h2 {{
                    margin: 0;
                    font-size: 24px;
                }}
                .header p {{
                    margin: 10px 0 0;
                    opacity: 0.9;
                }}
                .application-details {{
                    padding: 25px;
                    background: #fff;
                }}
                .application-details p {{
                    margin: 0 0 15px;
                }}
                .application-details strong {{
                    color: #2c3e50;
                }}
                .footer {{
                    background: #f8f9fa;
                    padding: 15px;
                    text-align: center;
                    color: #666;
                    font-size: 14px;
                    border-top: 1px solid #eee;
                }}
                a {{
                    text-decoration: none;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>{t['header']}</h2>
                    <p>{t['submitted_on']}: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
                </div>
                
                <div class="content">
                    {generate_questions_html(job_details, language)}
                </div>

                <div class="footer">
                    <p>{t['footer']}</p>
                </div>
            </div>
        </body>
    </html>
    """

    html_part = MIMEText(html_template, "html")
    message.attach(html_part)

    if pdf_path and os.path.exists(pdf_path):
        with open(pdf_path, "rb") as f:
            pdf_attachment = MIMEApplication(f.read(), _subtype="pdf")
            pdf_filename = os.path.basename(pdf_path)
            pdf_attachment.add_header(
                "Content-Disposition", 
                "attachment", 
                filename=pdf_filename
            )
            message.attach(pdf_attachment)

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)
            print("Email sent successfully!")
        
    except Exception as e:
        print(f"Error sending email: {str(e)}")

def generate_questions_html(job_details, language='en'):
    """
    Generate HTML for job application details in a single, clean box format.
    
    Args:
        job_details (dict): Dictionary containing job application details
        language (str): Language code ('en' for English, 'it' for Italian)
    
    Returns:
        str: Formatted HTML string
    """
    templates = {
        'en': {
            'experience': f"With {job_details['Years of Experience']} years of experience in the field, I believe I would be a valuable addition to your team.",
            'intro': "I am",
            'position_intro': "and I am writing to express my interest in the",
            'position_suffix': "position.",
            'contact': "You can reach me at",
            'why_interested': "Why I'm interested:",
            'profiles': "Professional Profiles:",
            'submitted_on': "Submitted on:",
            'footer': "This is an automated email from the Job Application System",
            'header': "Job Application Details"
        },
        'it': {
            'experience': f"Con {job_details['Years of Experience']} anni di esperienza nel settore, credo che sarei un'aggiunta preziosa al vostro team.",
            'intro': "Sono",
            'position_intro': "e scrivo per esprimere il mio interesse per la posizione di",
            'position_suffix': ".",
            'contact': "Potete contattarmi a",
            'why_interested': "Perché sono interessato/a:",
            'profiles': "Profili Professionali:",
            'submitted_on': "Inviato il:",
            'footer': "Questa è un'email automatica dal Sistema di Candidatura Lavoro",
            'header': "Dettagli Candidatura Lavoro"
        }
    }
    
    t = templates[language]

    return f"""
    <div class="application-details">
        <p>
            {t['intro']} <strong>{job_details.get('Full Name', '')}</strong>, {t['position_intro']} 
            <strong>{job_details.get('Position Applied', '')}</strong>{t['position_suffix']} {t['experience']}
        </p>
        
        <p>{t['contact']} <strong>{job_details.get('Email', '')}</strong>.</p>
        
        <p>
            <strong>{t['why_interested']}</strong><br>
            {job_details.get('Reason for Application', '')}
        </p>
        
        <p>
            <strong>{t['profiles']}</strong><br>
            {f'📎 LinkedIn: <a href="{job_details["LinkedIn URL"]}" style="color: #0077b5;">{job_details["LinkedIn URL"]}</a><br>' if job_details.get("LinkedIn URL") else ''}
            {f'💻 GitHub: <a href="{job_details["GitHub URL"]}" style="color: #333;">{job_details["GitHub URL"]}</a>' if job_details.get("GitHub URL") else ''}
        </p>
    </div>
    """

def save_last_application(job_details, language):
    """Save the last application details to a JSON file."""
    save_path = Path.home() / '.job_application_history.json'
    data = {
        'job_details': job_details,
        'language': language,
        'timestamp': datetime.now().isoformat()
    }
    with open(save_path, 'w') as f:
        json.dump(data, f)

def load_last_application():
    """Load the last application details if available."""
    save_path = Path.home() / '.job_application_history.json'
    if save_path.exists():
        with open(save_path) as f:
            return json.loads(f.read())
    return None

if __name__ == "__main__":
    prompts = {
        'en': {
            'recipient_email': "Enter recipient email",
            'invalid_email': "Invalid email format. Please try again.",
            'fill_details': "\nPlease fill in the following details (press Enter to skip optional fields):",
            'enter': "Enter",
            'optional': "optional",
            'required': "is required. Please provide a value.",
            'invalid_format': "Invalid {} format. Please try again.",
            'missing_credentials': "Error: Missing email credentials in .env file",
            'env_not_found': "Warning: .env file not found"
        },
        'it': {
            'recipient_email': "Inserisci l'email del destinatario",
            'invalid_email': "Formato email non valido. Riprova.",
            'fill_details': "\nCompila i seguenti dettagli (premi Invio per saltare i campi opzionali):",
            'enter': "Inserisci",
            'optional': "opzionale",
            'required': "è obbligatorio. Fornisci un valore.",
            'invalid_format': "Formato {} non valido. Riprova.",
            'missing_credentials': "Errore: Credenziali email mancanti nel file .env",
            'env_not_found': "Attenzione: File .env non trovato"
        }
    }


    pdf_prompts = {
        'en': {
            'attach_pdf': "Would you like to attach a PDF (CV/Resume)? (yes/no): ",
            'enter_path': "Enter the path to your PDF file: ",
            'file_not_found': "File not found. Please enter a valid path.",
            'invalid_file': "Invalid file type. Please select a PDF file.",
            'skip_pdf': "Skipping PDF attachment."
        },
        'it': {
            'attach_pdf': "Vuoi allegare un PDF (CV/Curriculum)? (si/no): ",
            'enter_path': "Inserisci il percorso del file PDF: ",
            'file_not_found': "File non trovato. Inserisci un percorso valido.",
            'invalid_file': "Tipo di file non valido. Seleziona un file PDF.",
            'skip_pdf': "Salto dell'allegato PDF."
        }
    }

    if not dotenv.load_dotenv():
        print(prompts['en']['env_not_found'])  

    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")

    if not all([sender_email, sender_password]):
        print(prompts['en']['missing_credentials']) 
        exit(1)

    last_application = load_last_application()
    
    if last_application:
        reuse_prompts = {
            'en': 'Would you like to use the details from your last application? (yes/no): ',
            'it': 'Vuoi utilizzare i dettagli della tua ultima candidatura? (si/no): '
        }
        
        language = last_application['language']
        use_last = input(reuse_prompts[language]).strip().lower()
        
        if use_last in ['yes', 'y', 'si', 's']:
            job_details = last_application['job_details']
            
            while True:
                recipient_email = input(f"{prompts[language]['recipient_email']}: ").strip()
                if validate_email(recipient_email):
                    break
                print(prompts[language]['invalid_email'])
                
            pdf_path = None
            pdf_p = pdf_prompts[language]
            
            while True:
                attach_pdf = input(pdf_p['attach_pdf']).strip().lower()
                if attach_pdf in ['no', 'n']:
                    print(pdf_p['skip_pdf'])
                    break
                elif attach_pdf in ['yes', 'y', 'si', 's']:
                    while True:
                        pdf_path = input(pdf_p['enter_path']).strip()
                        pdf_path = pdf_path.strip('"\'')
                        if not os.path.exists(pdf_path):
                            print(pdf_p['file_not_found'])
                            continue
                        if not pdf_path.lower().endswith('.pdf'):
                            print(pdf_p['invalid_file'])
                            continue
                        break
                    break
                    
            try:
                send_job_email(
                    sender_email,
                    sender_password,
                    recipient_email,
                    job_details,
                    language,
                    pdf_path
                )
                print("Email sent successfully!")
            except Exception as e:
                print(f"Error: {str(e)}")
                exit(1)
                
            exit(0)

    while True:
        language = input("Choose language (en/it): ").strip().lower()
        if language in ['en', 'it']:
            break
        print("Please choose 'en' for English or 'it' for Italian.")

    p = prompts[language]

    while True:
        recipient_email = input(f"{p['recipient_email']}: ").strip()
        if validate_email(recipient_email):
            break
        print(p['invalid_email'])

    job_details = {}
    required_fields = {
        "Full Name": str,
        "Email": validate_email,
        "Position Applied": str,
        "Years of Experience": str,
        "Reason for Application": str
    }
    
    optional_fields = {
        "LinkedIn URL": validate_url,
        "GitHub URL": validate_url
    }

    print(p['fill_details'])
    
    for field, validator in required_fields.items():
        while True:
            value = input(f"{p['enter']} {field}: ").strip()
            if not value:
                print(f"{field} {p['required']}")
                continue
            if validator == str or validator(value):
                job_details[field] = value
                break
            print(p['invalid_format'].format(field))

    for field, validator in optional_fields.items():
        value = input(f"{p['enter']} {field} ({p['optional']}): ").strip()
        if value and validator(value):
            job_details[field] = value

    pdf_path = None
    pdf_p = pdf_prompts[language]
    
    while True:
        attach_pdf = input(pdf_p['attach_pdf']).strip().lower()
        if attach_pdf in ['no', 'n']:
            print(pdf_p['skip_pdf'])
            break
        elif attach_pdf in ['yes', 'y', 'si', 's']:
            while True:
                pdf_path = input(pdf_p['enter_path']).strip()
                pdf_path = pdf_path.strip('"\'')
                if not os.path.exists(pdf_path):
                    print(pdf_p['file_not_found'])
                    continue
                if not pdf_path.lower().endswith('.pdf'):
                    print(pdf_p['invalid_file'])
                    continue
                break
            break

    save_last_application(job_details, language)

    try:
        send_job_email(
            sender_email,
            sender_password,
            recipient_email,
            job_details,
            language,
            pdf_path
        )
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)
