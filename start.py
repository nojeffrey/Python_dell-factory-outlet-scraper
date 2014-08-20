#!/usr/bin/env python

import smtplib
from email.mime.text import MIMEText
import requests
from lxml import etree, html

SMTP_SERVER = '<ip here>'
FROM = 'dell_notifications@mydomain.com'
TO = ['you@yourdomain.com']
SUBJECT = 'New server on Dell Factory Outlet'


ua = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36'}
response = requests.get("http://www1.ap.dell.com/content/topics/segtopic.aspx/products/quickship/au/en/poweredge?c=au&l=en&s=dfo", headers=ua)
#response = requests.get("http://localhost/dell.html", headers=ua)
tree = html.fromstring(response.text)

xpath_servers = tree.xpath(".//td[@class='gridCellAlt' or @class='gridCell']/text()")
final_list = []
sublist = []
for item in xpath_servers:
    if item.startswith('DFO'):
        if sublist:
            final_list.append(sublist)
        sublist = []
    sublist.append(item)
final_list.append(sublist)

with open('serials.txt', 'a+') as f:
    serials = f.read()
    for dell_server in final_list:
        for server_serial in dell_server:
            if server_serial.startswith('DFO'):
                print server_serial
                if server_serial in serials:
                    print 'Server already in list'
                else:
                    f.write(server_serial + '\n') #eg DFO-2757963SV \n
                    message = "Subject: %s\n\n%s\n\n%s" % (SUBJECT, '\n'.join(dell_server), "http://www1.ap.dell.com/content/topics/segtopic.aspx/products/quickship/au/en/poweredge?c=au&l=en&s=dfo")
                    server = smtplib.SMTP(SMTP_SERVER)
                    server.sendmail(FROM, TO, message)
                    server.quit()
                    print dell_server
                    #print 'else'
