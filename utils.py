'''renderers, channels and homepage'''

from markdown import markdown

import requests
from flask import make_response, jsonify

def make_html(url, time):
    """
    Return browser readable html that loads url in an iframe and refreshes after time seconds
    """
    time = str(time)
    html = """
    <!doctype html>
    <html>
        <head>
            <title>Kiosk</title>
            <meta name="viewport" content="width=device-width; initial-scale=1.0; maximum-scale=1.0; user-scalable=0;">
            <meta http-equiv="refresh" content="""+time+""">
        </head>
        <body style="margin:0px;padding:0px;overflow:hidden">
            <iframe src= """+url+""" frameborder="0" style="overflow:hidden;overflow-x:hidden;overflow-y:hidden;height:100%;width:100%;position:absolute;top:0px;left:0px;right:0px;bottom:0px" height="100%" width="100%"></iframe>
        </body>
    </html>
    """
    return html

def make_config(name, time, position, pages):
    """
    Return channel config page as browser readable html
    """
    position = str(position)
    pages = str(pages)
    time = str(time)
    html = """
    <!doctype html>
    <html>
        <head>
            <title>Kiosk """+name+""" config</title>
            <meta name="viewport" content="width=device-width; initial-scale=1.0; maximum-scale=1.0; user-scalable=0;">
        </head>
        <body>
        Channel name/time/pages<br>
        <form method="POST">
            <input name="channel-name", value="""+name+""">
            <input name="channel-time", value="""+time+""">
            <input name="channel-pages", size=300, value="""+pages+""">
            <input type="submit">
        </form>
        Channel position<br> """+position+"""<br>
        </body>
    </html>
    """
    return html

def make_new():
    """
    Return channel config page as browser readable html
    """
    html = """
    <!doctype html>
    <html>
        <head>
            <title>Kiosk new page</title>
            <meta name="viewport" content="width=device-width; initial-scale=1.0; maximum-scale=1.0; user-scalable=0;">
        </head>
        <body>
        Channel name<br>
        <form method="POST">
            <input name="channel-name">
            <input type="submit">
        </form>
        </body>
    </html>
    """
    return html

def build_markdown(title, content):
    '''
    Return the content as markdown formatted html with title title
    '''
    content = markdown(content, extensions=['markdown.extensions.extra'])
    fonts = '<link rel="stylesheet" type="text/css" href="//fonts.googleapis.com/css?family=Source+Code+Pro" />'
    head = '<html><head><title>'+title+'</title> '+fonts+' <link rel="stylesheet" href="/static/css/kiosky.css"></head>'

    page = head + '\n\n<body>\n' + content + '\n</body>\n</html>'
    return page

def home(channels):
    '''
    Returns the homepage as html
    '''
    raw = '# Kiosky\n\n'
    if not channels:
        raw = raw + '\n\n' + '> No available channels!' + '\n\n'
        return build_markdown('kiosky', raw)

    raw = raw + '\n'
    raw = raw + '## channels\n'

    for entry in channels:
        name = entry
        time = channels[entry][0]
        position = channels[entry][1]
        pages = channels[entry][2]

        raw = raw + '\n### '+name
        raw = raw + '\n[view](/channels/'+name+') [edit](/config/'+name+')'
        raw = raw + '\n#### Time: '+str(time)+'seconds'
        raw = raw + '\n#### Position: '+str(position)+'/'+str(len(pages)-1)
        for page in pages:
            raw = raw + '\n- '+page+'\n'

    raw = raw + '\n[Add channel](/new)'

    return build_markdown('kiosky', raw)

def channel_page(channel, channels):
    '''
    Returns html for channel
    '''
    channel = channels[channel]
    time = channel[0]
    position = channel[1]
    pages = channel[2]
    page = pages[position]
    return make_html(page, time)

def config_page(channel, channels):
    '''
    Returns html for channel config page
    '''
    name = channel
    channel = channels[channel]
    time = channel[0]
    position = channel[1]
    pages = channel[2]
    pages_string = '|'.join(pages)

    return make_config(name, time, position, pages_string)

# def add_page():
#     '''
#     Returns html for channel config page
#     '''
    # return make_config(name, time, position, pages)

