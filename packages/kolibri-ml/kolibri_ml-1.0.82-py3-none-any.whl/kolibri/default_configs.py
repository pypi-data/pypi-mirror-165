from kdmt.path import is_writable
import os
import re
import sys
import logging

KOLIBRI_DATA_FOLDER = os.getenv('KOLIBRI_DATA_PATH')

RESOURCES_AUTO_DOWNLOAD = os.getenv('KOLIBRI_RESOURCES_AUTO_DOWNLOAD')


if RESOURCES_AUTO_DOWNLOAD is None:
    RESOURCES_AUTO_DOWNLOAD = "true"
    os.environ['RESOURCES_AUTO_DOWNLOAD'] = RESOURCES_AUTO_DOWNLOAD


######################################################################
# data Path
######################################################################

DATA_PATH = []
"""A list of directories where packages from the Kolibri data are downloaded."""

# User-specified locations:
_paths_from_env = os.environ.get("KOLIBRI_DATA_PATH", "").split(os.pathsep)
DATA_PATH += [d for d in _paths_from_env if d]
if "APPENGINE_RUNTIME" not in os.environ and os.path.expanduser("~/") != "~/":
    DATA_PATH.append(os.path.expanduser("~/.kolibri"))

if sys.platform.startswith("win"):
    # Common locations on Windows:
    DATA_PATH += [
        os.path.join(sys.prefix, ".kolibri"),
        os.path.join(sys.prefix, "share", ".kolibri"),
        os.path.join(sys.prefix, "lib", ".kolibri"),
        os.path.join(os.environ.get("APPDATA", "C:\\"), ".kolibri"),
        r"C:\.kolibri",
        r"D:\.kolibri",
        r"E:\.kolibri",
    ]
else:
    # Common locations on UNIX & OS X:
    DATA_PATH += [
        os.path.join(sys.prefix, ".kolibri"),
        os.path.join(sys.prefix, "share", ".kolibri"),
        os.path.join(sys.prefix, "lib", ".kolibri"),
        "/usr/share/.kolibri",
        "/usr/local/share/.kolibri",
        "/usr/lib/.kolibri",
        "/usr/local/lib/.kolibri",
    ]

if KOLIBRI_DATA_FOLDER is None:

    for kolibridir in DATA_PATH:
        if os.path.exists(kolibridir) and is_writable(kolibridir):
                KOLIBRI_DATA_FOLDER= kolibridir

    # On Windows, use %APPDATA%
    if sys.platform == "win32" and "APPDATA" in os.environ:
        homedir = os.environ["APPDATA"]

    # Otherwise, install in the user's home directory.
    else:
        homedir = os.path.expanduser("~/")
        if homedir == "~/":
            raise ValueError("Could not find a default download directory")

        # append ".kolibri" to the home directory
        KOLIBRI_DATA_FOLDER= os.path.join(homedir, ".kolibri")

    os.environ['KOLIBRI_DATA_PATH'] = KOLIBRI_DATA_FOLDER





LOG_NAME = 'kolibri'
LOG_LEVEL = logging.DEBUG
LOGS_DIR = os.path.join(KOLIBRI_DATA_FOLDER, 'logs')
DO_LOG=True
# if not os.path.exists(LOGS_DIR):
#     try:
#         os.mkdir(LOGS_DIR)
#     except:
#         DO_LOG=False

DEFAULT_NN_MODEL_FILENAME="_model_.h5"

os.environ['Kolibri_DOWNLOAD_URL']="https://raw.githubusercontent.com/mbenhaddou/kolibri-data/main/index.json"
RELATIVE_ERROR = 10000
DEFAULT_SERVER_PORT = 5005
DEFAULT_SEED=4231
EMBEDDING_SIZE = 100
WORD2VEC_WORKERS = 4
MIN_WORD_COUNT = 5
WORD2VEC_CONTEXT = 5
TARGET_RANKING_LENGTH = 10

