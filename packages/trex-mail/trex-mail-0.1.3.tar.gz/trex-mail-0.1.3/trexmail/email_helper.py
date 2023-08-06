'''
Created on 15 Jul 2022

@author: jacklok
'''
from trexlib.utils.google.cloud_tasks_util import create_task
import logging
from trexmail.flask_mail import send_email
from flask import current_app
from trexlib.conf import SEND_EMAIL_TASK_URL
from trexlib.conf import DEPLOYMENT_MODE, LOCAL_MODE, SYSTEM_TASK_SERVICE_CREDENTIAL_PATH, SYSTEM_TASK_GCLOUD_PROJECT_ID, SYSTEM_TASK_GCLOUD_LOCATION, SYSTEM_TASK_SERVICE_ACCOUNT_EMAIL 
from trexmail.conf import DEFAULT_SENDER

logger = logging.getLogger('helper')

def trigger_send_email(sender_address=DEFAULT_SENDER, recipient_address=None, subject=None, message=None, cc_address=None):
    if DEPLOYMENT_MODE == LOCAL_MODE:
        send_email(sender           = sender_address, 
                   to_address   = [recipient_address], 
                   subject      = subject, 
                   body         = message,
                   app          = current_app
                   )
    
    else:
        queue_name      = 'send-email' 
        payload         = {
                                'sender_address'    : sender_address,
                                'recipient_address' : recipient_address,
                                'subject'           : subject,
                                'message'           : message,
                                'cc_address'        : cc_address,
                            }
                        
        create_task(SEND_EMAIL_TASK_URL, queue_name, payload=payload, 
                        in_seconds      = 1, 
                        http_method     = 'POST',
                        credential_path = SYSTEM_TASK_SERVICE_CREDENTIAL_PATH, 
                        project_id      = SYSTEM_TASK_GCLOUD_PROJECT_ID,
                        location        = SYSTEM_TASK_GCLOUD_LOCATION,
                        service_email   = SYSTEM_TASK_SERVICE_ACCOUNT_EMAIL
                        )
    
    return True
