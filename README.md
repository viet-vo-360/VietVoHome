
---

# Installation Instructions

## 1. Install Python
https://www.python.org/downloads/

<ins>Notes</ins>: Use version <= [3.8.6](https://www.python.org/downloads/release/python-386/) for windows 7.


## 2. Python Required Commands

To set up the necessary dependencies for this project, execute the following commands:

```
pip install Flask
pip install Flask-CORS
pip install Flask Flask-CORS
pip install Flask requests
```

Install CherryPy server:
```
pip install CherryPy
```
## 4. Setup Environment Variables
```
## Google SMTP server
FROM_EMAIL      # sending email
TO_EMAIL        # receiving email
SMTP_SERVER     # smtp.gmail.com
SMTP_USERNAME   # sending email
SMTP_PASSWORD   # from Google application's password
SMTP_PORT       # 587

## Google Recaptcha
RECAPTCHA_SECRET_KEY

## https from ZeroSSL
CERT_PATH       # certificate.crt
KEY_PATH        # private.key

## Flask
FLASK_ENV       # production

## Site
CORS_ORIGIN     # vohoangviet.id.vn
```

## 5. Run website

Execute the following command:

```
python app.py
```