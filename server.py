'''
server
'''

from flask import Flask, request, jsonify, make_response, send_from_directory, redirect

import utils
from page import Channels

CHANNELS = Channels()
APP = Flask(__name__)

@APP.route('/favicon.ico')
def favicon():
    '''Return favicon.ico'''
    return send_from_directory('/static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@APP.route('/', methods=['GET'])
def index():
    '''root home page'''
    return utils.home(CHANNELS.channels)

@APP.route('/channels/<channel>')
def channels(channel):
    '''channels'''
    if not channel in CHANNELS.channels:
        return f'Unknown channel: {channel}'
    CHANNELS.position_update(channel)
    return utils.channel_page(channel, CHANNELS.channels)

@APP.route('/config/<channel>', methods=['GET', 'POST'])
def config(channel):
    '''config'''
    if request.method == 'GET':
        if not channel in CHANNELS.channels:
            return f'Unable to display config: Unknown channel: {channel}'
        return utils.config_page(channel, CHANNELS.channels)
    elif request.method == 'POST':
        name = request.form['channel-name']
        time = request.form['channel-time']
        pages_string = request.form['channel-pages']
        pages = pages_string.split(',')
        CHANNELS.remove(name)
        CHANNELS.add(name, pages, time)
        return redirect('/')

@APP.route('/new', methods=['GET', 'POST'])
def new():
    '''new channel'''
    if request.method == 'POST':
        channel = request.form['channel-name']
        if channel in CHANNELS.channels:
            return f'Unable to make new channel: name {channel} already exists'
        CHANNELS.add(channel, [], 60)
        return redirect('/')
    elif request.method == 'GET':
        return utils.make_new()

@APP.errorhandler(404)
def not_found(error):
    '''Return a generic 404 message'''
    _path = request.full_path
    _ip = request.remote_addr
    return make_response(jsonify({'error': 'Not found'}), 404)
