from http.server import BaseHTTPRequestHandler
import json
import apprise
 
class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(400)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        self.wfile.write('Apprise Vercel is working, use POST method to send notifications.'.encode('utf-8'))
 
    def do_POST(self):
        if 'content-type' not in self.headers or self.headers['content-type'] != 'application/json':
            self.send_response(400)
            self.send_header('Content-type','text/plain')
            self.end_headers()
            self.wfile.write('Currently `content-type` must be `application/json` (which is different from caronc/apprise-api)'.encode('utf-8'))
            return

        # Currently we only support JSON
        length = int(self.headers['content-length'])
        form = json.loads(self.rfile.read(length))
        
        apobj = apprise.Apprise()

        for url in form['urls'].split(","):
            apobj.add(url)
        
        if apobj.notify(
            body=form['body'],
            title=form.get('title', ''),
            notify_type=form.get('type', 'info'),
            body_format=form.get('format', 'text'),
        ):
            self.send_response(200)
            self.send_header('Content-type','text/plain')
            self.end_headers()
            self.wfile.write('OK'.encode('utf-8'))
        else:
            self.send_response(500)
            self.send_header('Content-type','text/plain')
            self.end_headers()
            self.wfile.write('Error sending notifications'.encode('utf-8'))
