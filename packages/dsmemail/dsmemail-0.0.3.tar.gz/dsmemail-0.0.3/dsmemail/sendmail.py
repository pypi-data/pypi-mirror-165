import os
import requests
from .check import check_type, check_env

DSM_EMAIL_APIKEY = os.environ.get('DSM_EMAIL_APIKEY', None)
DSM_EMAIL_URI = os.environ.get('DSM_EMAIL_URI', None)

def sendEmail(subject=None, message=None, emails=None):
    
    check_env()
    
    check_type(variable=subject, variableName="subject", dtype=str)
    check_type(variable=message, variableName="message", dtype=str)
    check_type(variable=emails, variableName="emails", dtype=list, child=str)
    
    r = requests.post(f"{DSM_EMAIL_URI}/email/api/sendMail/",
            headers={
                "Authorization": f"Api-Key {DSM_EMAIL_APIKEY}"
            },
            json={
                "subject": subject,
                "message": message,
                "email": emails
            }
    )
    
    if r.status_code == 201:
        return True, "email send sucess"
    elif r.status_code in [400, 401, 403]:
        return False, r.json()
    else:
        return False, f"{r.content}\nsome thing wrong {r.status_code}"