import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from email_handler import send_email
from cheroot.wsgi import Server as WSGIServer
from cheroot.ssl.builtin import BuiltinSSLAdapter
import logger

app = Flask(__name__)

logger.configure_logging()

cors_origin = os.environ.get('CORS_ORIGIN', 'http://localhost')
CORS(app, resources={r"/*": {"origins": cors_origin}})

SITE_ROOT = '.'

# Serve the index.html file.
@app.route('/')
def serve_index():
    logger.log_request()
    return send_from_directory(SITE_ROOT, 'index.html')

# Serve files from the root directory.
@app.route('/<path:path>')
def serve_file(path):
    return send_from_directory(SITE_ROOT, path)

# Wrapper for send_email function from email_handler.
@app.route('/send_email', methods=['POST'])
def send_email_wrapper():
    logger.log_request()
    return send_email()

if __name__ == '__main__':
    cert_path = os.environ.get('CERT_PATH')
    key_path = os.environ.get('KEY_PATH')
    
    # Check if the paths are provided
    if cert_path is None or key_path is None:
        raise ValueError("Certificate or private key path is not provided in environment variables.")
    
    # Configure CherryPy server
    server = WSGIServer(bind_addr=('0.0.0.0', 443), wsgi_app=app)
    server.ssl_adapter = BuiltinSSLAdapter(certificate=cert_path, private_key=key_path)
    
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()
    except Exception as e:
        app.logger.error("An error occurred: %s", str(e))
        server.stop()
