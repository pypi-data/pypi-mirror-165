'''
Created on 5 Jun 2020

@author: jacklok
'''


from mailjet_rest import Client
from six import string_types
import logging
from trexmail import conf

api_key         = None#conf.MAILJET_API_KEY
api_secret      = None#conf.MAILJET_SECRET_KEY

def send_email(sender=None, to_address=None, cc_address=None, bcc_address=None, subject=None, 
               body=None, html=None, batch_id=None, app=None):
    
    logging.info('sender=%s', sender)
    logging.info('to_address=%s', to_address)
    logging.info('subject=%s', subject)
    
    logging.info('api_key=%s', api_key)
    logging.info('api_secret=%s', api_secret)
    
    
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    
    to_address_list = None
    
    if isinstance(to_address, string_types):
        to_address_list = [{"Email": to_address}]
    elif isinstance(to_address, (tuple, list)):
        to_address_list = []
        for t in to_address:
            to_address_list.append({"Email": t})
    
    cc_address_list = None
    if isinstance(cc_address, string_types):
        cc_address_list = [{"Email": cc_address}]
    elif isinstance(cc_address, (tuple, list)):
        cc_address_list = []
        for t in cc_address:
            cc_address_list.append({"Email": t})        
            
    bcc_address_list = None
    if isinstance(bcc_address, string_types):
        bcc_address_list = [{"Email": bcc_address}]
    elif isinstance(bcc_address, (tuple, list)):
        bcc_address_list = []
        for t in bcc_address:
            bcc_address_list.append({"Email": t})        
    
    data = {
      'Messages': [
        {
          "From": {
            "Email": sender,
            #"Name": ""
          },
          "To": to_address_list,
          "Bcc": bcc_address_list,
          "Cc": cc_address_list,
          "Subject"     : subject,
          "TextPart"    : body,
          "HTMLPart"    : html,
          "CustomID"    : batch_id
        }
      ]
    }
    result = mailjet.send.create(data=data)
    result_in_json = result.json()
    
    logging.debug('result_in_json=%s', result_in_json)
    logging.debug('result_in_json.Messages=%s', result_in_json.get('Messages'))
    
    response_status = {}
    
    for a in result_in_json.get('Messages')[0].get('To'):
        response_status[a.get('Email')] = {
                                            'message_id'    : a.get('MessageID'),
                                            'message_uuid'  : a.get('MessageUUID'),
                                            }
        
    
    #logging.debug('Status=%s', result.status)
    logging.debug('Result=%s', result_in_json)
    
    return result_in_json.get('Messages')[0].get('Status')=='success'
    


