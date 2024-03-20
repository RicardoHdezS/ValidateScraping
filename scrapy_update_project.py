import shutil, os
from dotenv import load_dotenv

load_dotenv()

home_path = r'./FastBot/FastBot/features/templates/ds_scrapy_file.tmpl'
tmp_path = fr'{os.getenv("TMP_PATH")}'

shutil.copy(home_path, tmp_path)