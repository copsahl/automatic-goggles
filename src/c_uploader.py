import base64
from os.path import exists
from http.server import HTTPServer, SimpleHTTPRequestHandler

DIRECTORY = "uploads"
PORT = 8080

class Error(Exception):
    pass

class UploadFileNotFound(Error):
    pass

class HTTPRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def log_message(self, format, *args):
        """Surpress HTTP logs"""
        return


class Uploader:

    """Class to create shell/powershell commands for file upload"""

    @staticmethod
    def linux_script_upload(local_file, new_filename):
        if not exists(f"uploads/{local_file}"):
            raise UploadFileNotFound
        
        with open(f"uploads/{local_file}", "r") as fObj:
            data = fObj.read()

        b64_str = base64.b64encode(data.encode()).decode()
        return f"echo '{b64_str}' | base64 -d > /tmp/{new_filename} && chmod 0700 /tmp/{new_filename}"
    
    @staticmethod
    def windows_script_upload(local_file, new_filename):
        pass

    @staticmethod
    def web_host_upload():
        # TODO: Make better
        # NOTE: Require's 'admin' or 'root' permissions
        try:
            serv = HTTPServer(("0.0.0.0", PORT), HTTPRequestHandler)
            serv.serve_forever()
        except PermissionError as e:
            print(f"Ope: {e}: Cannot start HTTP server!")
            return