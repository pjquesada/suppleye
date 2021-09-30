import smtplib
from tabulate import tabulate
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def missing_alert(bom_parts, sub, msg):
    _FROM = 'donotreply@example.com'
    _SERVER = 'smtp.example.com'
    _RECIPIENTS = ['RECIPIENT 1', 'RECIPIENT 2', 'RECIPIENT 3', 'RECIPIENT 4']

    text = """
            Hello,

            %s

            {table}
            """ % msg

    html = """
            <html>
            <head>
            <style> 
              table, th, td {{ border: 1px solid black; border-collapse: collapse; }}
              th, td {{ padding: 5px; }}
            </style>
            </head>
            <body><p> Hello, </p>
            <p> %s </p>
            {table}
            </body></html>
            """ % msg

    if bom_parts:
        missing_info_list = [['LINE NUMBER', 'LINE']]
        for i in bom_parts:
            missing_info_list.append(i)

        text = text.format(table=tabulate(missing_info_list, headers="firstrow", tablefmt="github"))
        html = html.format(table=tabulate(missing_info_list, headers="firstrow", tablefmt="html"))

    message = MIMEMultipart(
        "alternative", None, [MIMEText(text), MIMEText(html, 'html')])

    message['Subject'] = "[Automated Alert] %s" % sub
    message['From'] = _FROM
    message['To'] = ', '.join(_RECIPIENTS)
    _SERVER = smtplib.SMTP(_SERVER)
    _SERVER.sendmail(_FROM, _RECIPIENTS, message.as_string())
    _SERVER.quit()


def price_alert(bom_parts, sub, msg):
    _FROM = 'donotreply@example.com'
    _SERVER = 'smtp.example.com'
    _RECIPIENTS = ['RECIPIENT 1', 'RECIPIENT 2', 'RECIPIENT 3', 'RECIPIENT 4']
    text = """
            Hello,

            %s

            {table}

            """ % msg

    html = """
            <html>
            <head>
            <style> 
              table, th, td {{ border: 1px solid black; border-collapse: collapse; }}
              th, td {{ padding: 5px; }}
            </style>
            </head>
            <body><p> Hello, </p>
            <p> %s </p>
            {table}
            </body></html>
            """ % msg

    price_info_list = [['AVPN', 'OCTOID', 'MFR', 'MPN', 'QTY', 'SELLER', 'CURRENT PRICE', 'BASELINE PRICE',
                        'STOCK', 'LEAD TIME (DAYS)', 'PULL DATE']]

    if bom_parts:
        for i in bom_parts:
            price_info_list.append(i)

        text = text.format(table=tabulate(price_info_list, headers="firstrow", tablefmt="github"))
        html = html.format(table=tabulate(price_info_list, headers="firstrow", tablefmt="html"))

    message = MIMEMultipart(
        "alternative", None, [MIMEText(text), MIMEText(html, 'html')])

    message['Subject'] = "[Automated Alert] %s" % sub
    message['From'] = _FROM
    message['To'] = ', '.join(_RECIPIENTS)
    _SERVER = smtplib.SMTP(_SERVER)
    _SERVER.sendmail(_FROM, _RECIPIENTS, message.as_string())
    _SERVER.quit()


def stock_alert(bom_parts, sub, msg):
    _FROM = 'donotreply@example.com'
    _SERVER = 'smtp.example.com'
    _RECIPIENTS = ['RECIPIENT 1', 'RECIPIENT 2', 'RECIPIENT 3', 'RECIPIENT 4']
    text = """
            Hello,

            %s

            {table}

            """ % msg

    html = """
            <html>
            <head>
            <style> 
              table, th, td {{ border: 1px solid black; border-collapse: collapse; }}
              th, td {{ padding: 5px; }}
            </style>
            </head>
            <body><p> Hello, </p>
            <p> %s </p>
            {table}
            </body></html>
            """ % msg
    stock_info_list = [
        ['AVPN', 'OCTOID', 'MFR', 'MPN', 'QTY', 'SELLER', 'AVERAGE PRICE', 'CURRENT STOCK', 'BASELINE STOCK',
         'LEAD TIME (DAYS)', 'PULL DATE']]

    if bom_parts:
        for i in bom_parts:
            stock_info_list.append(i)

        text = text.format(table=tabulate(stock_info_list, headers="firstrow", tablefmt="github"))
        html = html.format(table=tabulate(stock_info_list, headers="firstrow", tablefmt="html"))

    message = MIMEMultipart(
        "alternative", None, [MIMEText(text), MIMEText(html, 'html')])

    message['Subject'] = "[Automated Alert] %s" % sub
    message['From'] = _FROM
    message['To'] = ', '.join(_RECIPIENTS)
    _SERVER = smtplib.SMTP(_SERVER)
    _SERVER.sendmail(_FROM, _RECIPIENTS, message.as_string())
    _SERVER.quit()


def lead_alert(bom_parts, sub, msg):
    _FROM = 'donotreply@example.com'
    _SERVER = 'smtp.example.com'
    _RECIPIENTS = ['RECIPIENT 1', 'RECIPIENT 2', 'RECIPIENT 3', 'RECIPIENT 4']
    text = """
            Hello,

            %s

            {table}

            """ % msg

    html = """
            <html>
            <head>
            <style> 
              table, th, td {{ border: 1px solid black; border-collapse: collapse; }}
              th, td {{ padding: 5px; }}
            </style>
            </head>
            <body><p> Hello, </p>
            <p> %s </p>
            {table}
            </body></html>
            """ % msg
    lead_info_list = [
        ['AVPN', 'OCTOID', 'MFR', 'MPN', 'QTY', 'SELLER', 'AVERAGE PRICE', 'STOCK', 'CURRENT LEAD TIME (DAYS)',
         'BASELINE LEAD TIME (DAYS)', 'PULL DATE']]

    if bom_parts:
        for i in bom_parts:
            lead_info_list.append(i)

        text = text.format(table=tabulate(lead_info_list, headers="firstrow", tablefmt="github"))
        html = html.format(table=tabulate(lead_info_list, headers="firstrow", tablefmt="html"))

    message = MIMEMultipart(
        "alternative", None, [MIMEText(text), MIMEText(html, 'html')])

    message['Subject'] = "[Automated Alert] %s" % sub
    message['From'] = _FROM
    message['To'] = ', '.join(_RECIPIENTS)
    _SERVER = smtplib.SMTP(_SERVER)
    _SERVER.sendmail(_FROM, _RECIPIENTS, message.as_string())
    _SERVER.quit()


def critical_stock_parts(critical_parts, sub, msg):
    _FROM = 'donotreply@example.com'
    _SERVER = 'smtp.example.com'
    _RECIPIENTS = ['RECIPIENT 1', 'RECIPIENT 2', 'RECIPIENT 3', 'RECIPIENT 4']
    text = """
                Hello,

                %s

                {table}

                """ % msg

    html = """
                <html>
                <head>
                <style> 
                  table, th, td {{ border: 1px solid black; border-collapse: collapse; }}
                  th, td {{ padding: 5px; }}
                </style>
                </head>
                <body><p> Hello, </p>
                <p> %s </p>
                {table}
                </body></html>
                """ % msg
    critical_stock_info_list = [['AVPN', 'MPN', 'SELLER', 'MFR', 'AVERAGE PRICE', 'CURRENT STOCK', 'LEAD TIME (DAYS)',
                                 'PULL DATE']]

    if critical_parts:
        for avpn in critical_parts:
            for part in avpn:
                critical_stock_info_list.append(part)

        text = text.format(table=tabulate(critical_stock_info_list, headers="firstrow", tablefmt="github"))
        html = html.format(table=tabulate(critical_stock_info_list, headers="firstrow", tablefmt="html"))

    message = MIMEMultipart("alternative", None, [MIMEText(text), MIMEText(html, 'html')])

    message['Subject'] = "[Automated Alert] %s" % sub
    message['From'] = _FROM
    message['To'] = ', '.join(_RECIPIENTS)
    _SERVER = smtplib.SMTP(_SERVER)
    _SERVER.sendmail(_FROM, _RECIPIENTS, message.as_string())
    _SERVER.quit()


def alert(bom_parts, msg, missing=False, price=False, stock=False, lead=False, critical=False):
    """
    This function creates an email template and table for different types of alerts to be sent out and connects to
    an smtp server to send an email alert. Message and subject fields are passed in the function as well as the
    designated array of parts formatted into sub arrays with each parts information to be tabulated. The type of
    alert is indicated and passed in the function; Missing is to send an alert if there is missing part information
    within the BOM file, price is used to send an alert if the price of a part has increased, stock is used to send
    an alert if the stock level of a part has decreased, and lead is used to send an alert if the lead time of a part
    has increased. The recipients of the email is configurable.
    """

    if missing:
        sub = 'Missing Part Info.'
        missing_alert(bom_parts, sub, msg)
    if price:
        sub = 'Price Increase'
        price_alert(bom_parts, sub, msg)
    if stock:
        sub = 'Stock Decrease'
        stock_alert(bom_parts, sub, msg)
    if lead:
        sub = 'Lead Time Increase'
        lead_alert(bom_parts, sub, msg)
    if critical:
        sub = 'Critical Stock'
        critical_stock_parts(bom_parts, sub, msg)