import os
import sys

if getattr(sys, "frozen", False):
    cert = os.path.join(sys._MEIPASS, "progress", "certs", "combined.pem")
    if os.path.isfile(cert):
        os.environ["SSL_CERT_FILE"] = cert
        os.environ["REQUESTS_CA_BUNDLE"] = cert
