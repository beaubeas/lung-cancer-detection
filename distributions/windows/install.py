import os
import sys
import atexit
import zipfile
import winshell
import requests
from PIL import Image
from pathlib import Path

assert os.name == 'nt'


def at_exit():
    os.system('pause')


atexit.register(at_exit)

PY_EMBED_URL = 'https://www.python.org/ftp/python/3.7.4/python-3.7.4-embed-amd64.zip'
GET_PIP_URL = 'https://bootstrap.pypa.io/get-pip.py'
VC_REDIST_URL = 'https://aka.ms/vs/16/release/vc_redist.x64.exe'

# must be replaced in another script
NAME = '$name'
VERSION = '$version'

assert NAME != '$' + 'name'
assert VERSION != '$' + 'version'

if len(sys.argv) < 2:
    INSTALL_DIR = os.path.join('C:\PROGRA~1', NAME)
else:
    INSTALL_DIR = os.path.join(os.path.abspath(sys.argv[1]), NAME)


def make_dir(d):
    if not os.path.isdir(d):
        os.makedirs(d)


PYTHON_DIR = os.path.join(INSTALL_DIR, 'python')

try:
    make_dir(INSTALL_DIR)
    make_dir(PYTHON_DIR)
except PermissionError as e:
    sys.exit('Please, run the installer as administrator')

PTH_PATH = os.path.join(PYTHON_DIR, 'python37._pth')


def download_file(url):
    filename = url.split('/')[-1]
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return filename


print('installing vc_redist')
vc_redist_filename = download_file(VC_REDIST_URL)
os.system('"{}" /install /quiet /norestart'.format(vc_redist_filename))
os.remove(vc_redist_filename)

print('installing python')
py_embed_filename = download_file(PY_EMBED_URL)
with zipfile.ZipFile(py_embed_filename, 'r') as z:
    z.extractall(PYTHON_DIR)
os.remove(py_embed_filename)

print('fixing imports')

with open(PTH_PATH, 'a') as f:
    f.write('\nimport site')

with open(os.path.join(PYTHON_DIR, 'sitecustomize.py'), 'w') as f:
    f.write('import sys; sys.path.insert(0, "")')

PYTHON_EXE = os.path.join(PYTHON_DIR, 'python.exe')

get_pip_filename = download_file(GET_PIP_URL)
os.system('{} "{}" --no-warn-script-location'.format(PYTHON_EXE, get_pip_filename))
os.remove(get_pip_filename)


os.system('{} -m pip install torch==1.5.0+cpu torchvision==0.6.0+cpu -f https://download.pytorch.org/whl/torch_stable.html --no-warn-script-location'.format(PYTHON_EXE))
if VERSION == '':
    os.system('{} -m pip install mindsdb --no-warn-script-location'.format(PYTHON_EXE))
else:
    os.system('{} -m pip install mindsdb=={} --no-warn-script-location'.format(PYTHON_EXE, VERSION))

print('generating run_server.bat')
with open(os.path.join(INSTALL_DIR, 'run_server.bat'), 'w') as f:
    lines = []
    lines.append('{} -m mindsdb --api=http,mysql,mongodb'.format(PYTHON_EXE))
    f.write('\n'.join(lines))

link_path = str(Path(winshell.desktop()) / '{}.lnk'.format(NAME))

icon_path = os.path.join(INSTALL_DIR, 'mdb-icon.ico')

with open(icon_path, 'wb') as f:
    f.write(
        requests.get('https://mindsdb-installer.s3-us-west-2.amazonaws.com/mdb-icon.png').content
    )

img = Image.open(icon_path)
new_path = icon_path.rstrip('.png') + '.ico'
img.save(new_path, sizes=[(96, 96)])

icon_abspath = os.path.abspath(new_path)

# Create the shortcut on the desktop
with winshell.shortcut(link_path) as link:
    link.path = os.path.join(INSTALL_DIR, 'run_server.bat')
    link.description = NAME
    link.icon_location = (icon_abspath, 0)

print('Success. A desktop shortcut has been created ({})'.format(link_path.rstrip('.lnk')))
