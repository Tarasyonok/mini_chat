import random
import re
import sys
import threading
import time
from flask import Flask, render_template
from turbo_flask import Turbo

app = Flask(__name__)
turbo = Turbo(app)

messages = ['test', 'Hello, World!', '123']

@app.context_processor
def inject_load():
    return {'messages': messages}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/page2')
def page2():
    return render_template('page2.html')


def update_load():
    with app.app_context():
        while True:
            time.sleep(1)
            messages.append(f'test{len(messages)}')
            turbo.push(turbo.replace(render_template('loadavg.html'), 'load'))


th = threading.Thread(target=update_load)
th.daemon = True
th.start()

app.run()
