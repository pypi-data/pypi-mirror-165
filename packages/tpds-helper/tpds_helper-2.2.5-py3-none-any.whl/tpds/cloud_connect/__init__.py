"""
    Trust Platform core package - cloud_connect module
"""
try:
    from .aws_connect import *
    from .azure_connect import *
    from .gcp_connect import *
except ModuleNotFoundError as e:
    pass

from .cloud_connect import *
