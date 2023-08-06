'''
Created on 4 Jun 2020

@author: jacklok
'''

from flask_mail import Mail, Message 
import logging

def send_email(sender=None, to_address=None, cc_address=None, bcc_address=None, subject=None, 
               body=None, html=None, batch_id=None, is_html=False, app=None):
        
    msg = Message(subject, sender=sender, recipients=to_address, cc=cc_address, bcc=bcc_address)
    if is_html:
        msg.html = html
    else:
        msg.body = body
    
    mail = Mail(app=app)
    
    logging.debug('mail.username=%s', mail.username)
    logging.debug('mail.password=%s', mail.password)
        
    mail.send(msg)
    
    return True