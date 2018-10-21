# About

Its easy to share files from a computer in python3 using

```
python3 -m http.server #or python2 -m SimpleHTTPServer
```

But receiving files has no easy one liner.

Using flask_upload you can set up a web server to receive incoming files with:

```
docker run -p 5000:5000 -v $PWD:/tmp/output -it amccormack/flask_upload
```

or

```
python flask_upload.py
```

`flask_upload.py` has been tested on Python 2.7.9 and Python 3.6


# Usage of flask_upload.py

```
$ python flask_upload.py -h
usage: flask_upload.py [-h] [-f UPLOAD_FOLDER] [-u USERNAME] [-p PASSWORD]
                       [--host HOST] [--port PORT]

optional arguments:
  -h, --help            show this help message and exit
  -f UPLOAD_FOLDER, --upload-folder UPLOAD_FOLDER
                        The path to store the files. (default temp dir)
  --host HOST
  --port PORT

credentials:
  No authentication is performed by default, but you may specify a username
  and password

  -u USERNAME, --username USERNAME
                        Username. Required if password is specified
  -p PASSWORD, --password PASSWORD
                        Password. Required if username is specified

```
