from typing import Any, Dict, Optional
import yaml
import os


try:
    from yaml import (
        CSafeLoader as SafeLoader
    )
except ImportError:
    from yaml import ( 
        SafeLoader
    )
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def get_project_root(kwargs):
    return os.getcwd() if not kwargs.get('project_dir') else os.path.abspath(kwargs['project_dir'])

def safe_load(content) -> Optional[Dict[str, Any]]:
    return yaml.load(content, Loader=SafeLoader)
    
def get_project_root(kwargs):
    return os.getcwd() if not kwargs.get('project_dir') else os.path.abspath(kwargs['project_dir'])