import os

#SENDGRID_API_KEY                                    = os.environ.get('SENDGRID_API_KEY')


#MAILJET_API_KEY                                     = os.environ.get('MAILJET_API_KEY')
#MAILJET_SECRET_KEY                                  = os.environ.get('MAILJET_SECRET_KEY')

FLASK_MAIL_USERNAME                                 = os.environ.get('FLASK_MAIL_USERNAME')
FLASK_MAIL_PASSWORD                                 = os.environ.get('FLASK_MAIL_PASSWORD')
FLASK_MAIL_SERVER                                   = os.environ.get('FLASK_MAIL_SERVER')
FLASK_MAIL_SERVER_PORT                              = os.environ.get('FLASK_MAIL_SERVER_PORT')
FLASK_MAIL_USE_SSL                                  = os.environ.get('FLASK_MAIL_USE_SSL')

DEFAULT_SENDER                                      = os.environ.get('DEFAULT_SENDER')
DEFAULT_RECIPIENT_EMAIL                             = os.environ.get('DEFAULT_RECIPIENT_EMAIL')