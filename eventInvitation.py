#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf8  
'''
@author: sats
'''
import smtplib

from email.utils import formatdate
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase

from email import Encoders
import os, datetime

config = fileutil.social

def send_invite(param):
    CRLF = "\r\n"
    attendees = param['to']
    attendees = ""
    try:
        for att in param['to']:
            attendees += "ATTENDEE;CUTYPE=INDIVIDUAL;ROLE=REQ-PARTICIPANT;PARTSTAT=NEEDS-ACTION;RSVP=TRUE;CN="+att+";X-NUM-GUESTS=0:mailto:"+att+CRLF
    except Exception as e:
        print e
    fro = "Satish <noreply@abc.com>"
    
    msg = MIMEMultipart('mixed')
    msg['Reply-To']=fro
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = 'Satish:Meeting invitation from Satihs'
    msg['From'] = fro
    msg['To'] = attendees

    __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
    f= os.path.join(__location__, 'invite.ics')   
    ics_content = open(f).read()
    try:
        replaced_contents = ics_content.replace('startDate', param['startDate'])
        replaced_contents = replaced_contents.replace('endDate', param['endDate'])
        replaced_contents = replaced_contents.replace('telephonic', param['location'])
        replaced_contents = replaced_contents.replace('now', datetime.datetime.now().strftime("%Y%m%dT%H%M%SZ"))
    except Exception as e:
        log.warn(e)
    if param.get('describe') is not None:
        replaced_contents = replaced_contents.replace('describe', param.get('describe'))
    else:
        replaced_contents = replaced_contents.replace('describe', '')
    replaced_contents = replaced_contents.replace('attend',  msg['To'])
    replaced_contents = replaced_contents.replace('subject',  param['subject'])
    part_email = MIMEText(replaced_contents,'calendar;method=REQUEST')

    
    msgAlternative = MIMEMultipart('alternative')
   
    
    ical_atch = MIMEBase('text/calendar',' ;name="%s"'%"invitation.ics")
    ical_atch.set_payload(replaced_contents)
    Encoders.encode_base64(ical_atch)
    ical_atch.add_header('Content-Disposition', 'attachment; filename="%s"'%f)
    

    
    msgAlternative.attach(part_email)
    msgAlternative.attach(ical_atch)
    msg.attach(msgAlternative)
    mailServer = smtplib.SMTP('smtp.mandrillapp.com', 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login('smtp-username', 'smtp-password')
    mailServer.sendmail(fro, param['to'], msg.as_string())
    mailServer.close()