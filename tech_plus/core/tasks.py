from tech_plus.celery import app
from .utils.excel import Excel
import base64
from django.conf import settings
from django.core.files.storage import default_storage

@app.task
def fill(base64_json_string):
    file_bytes_base64 = base64_json_string.encode('utf-8')
    file_url = base64.b64decode(file_bytes_base64).decode()
    file_name = file_url.split()[1][1:-2]
    file = str(settings.BASE_DIR) + file_name
    Excel.fill_excel(file=file)
    default_storage.delete(file)
     
