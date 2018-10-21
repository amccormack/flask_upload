'''
Copyright 2018 Alex McCormack

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''


from __future__ import print_function

import argparse
from functools import wraps
import os
import tempfile
from flask import Flask, request, redirect, url_for, Response
from werkzeug.utils import secure_filename

app = Flask(__name__)

def check_creds(username, password):
    return username == app.config['USERNAME'] and password == app.config['PASSWORD']

def auth401():
    return Response('Login Required', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_authentication(f):
    @wraps(f)
    def dec(*args, **kwargs):
        if not app.config['REQUIRE_AUTH']:
            return f(*args, **kwargs)
        auth = request.authorization
        if not auth or not check_creds(auth.username, auth.password):
            return auth401()
        return f(*args, **kwargs)
    return dec

@app.route('/', methods=['GET', 'POST'])
@requires_authentication
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        print('Wrote file to {0}'.format(filepath))
        file.save(filepath)
        return '''
            <!doctype html>
            <title>File Saved</title>
            <h1>File {0} has been saved</h1>
            <h1>Upload new File</h1>
            <form method=post enctype=multipart/form-data>
              <p><input type=file name=file>
                 <input type=submit value=Upload>
            </form>
        '''.format(file.filename)
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--upload-folder', help='The path to store the files. (default temp dir)')
    creds = parser.add_argument_group('credentials', 'No authentication is performed by default, but you may specify a username and password')
    creds.add_argument('-u', '--username', help='Username. Required if password is specified')
    creds.add_argument('-p', '--password', help='Password. Required if username is specified')

    parser.add_argument('--host', default='0.0.0.0')
    parser.add_argument('--port', default=5000, type=int)

    args = parser.parse_args()
    if any([args.username, args.password]) and not all([args.username, args.password]):
        parser.print_help()
        parser.error('Both username or password must be specified, or neither should be specified')

    app.config['REQUIRE_AUTH'] = all([args.username, args.password])
    app.config['USERNAME'] = args.username
    app.config['PASSWORD'] = args.password

    folder = args.upload_folder or tempfile.mkdtemp()
    if not os.path.isdir(folder):
        raise ValueError('Folder {0} does not exist'.format(folder))
    app.config['UPLOAD_FOLDER'] = folder

    app.run(args.host, args.port, load_dotenv=False)
