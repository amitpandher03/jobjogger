# Job Application Email Sender

A Python script that sends formatted job application emails in either English or Italian.

## Features

- Bilingual support (English and Italian)
- Clean, professional email template
- Input validation for emails and URLs
- Optional LinkedIn and GitHub profile links
- Optional PDF attachment
- Secure credential management using environment variables
- User-friendly command-line interface

## Prerequisites

- Python 3.6 or higher
- Gmail account with App Password enabled
- Required Python packages (install using `pip install -r requirements.txt`):
  - python-dotenv
  - secure-smtplib

## Setup

1. Clone the repository:

```bash
git clone https://github.com/amitpandher03/jobjogger.git
```

2. Navigate to the project directory:

```bash
cd jobjogger
```

3. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
```

4. Install the required packages:

```bash
pip install -r requirements.txt
```

5. Create a `.env` file with your Gmail credentials:
   - Copy `.env.example` to `.env`
   - Generate an App Password for your Gmail account:
     1. Go to your Google Account settings
     2. Enable 2-Step Verification
     3. Go to Security > App passwords
     4. Generate a new app password for "Mail"
   - Update `.env` with your Gmail address and the generated App Password

## Usage

1. Run the script:

```bash
python job-to-email.py
```

2. Follow the prompts:
   - Choose language (English or Italian)
   - Enter recipient's email
   - Fill in job application details
   - Add optional professional profile links
   - Optionally attach a PDF file (CV/Resume)

## Email Template

The email includes:
- Professional header with submission timestamp
- Applicant's full name and contact information
- Position applied for
- Years of experience
- Reason for application
- Professional profile links (optional)
- PDF attachment (optional)
- Clean, responsive design

## Security Notes

- Never commit your `.env` file to version control
- Use App Passwords instead of your main Gmail password
- The script uses SMTP over TLS for secure email transmission

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository.
