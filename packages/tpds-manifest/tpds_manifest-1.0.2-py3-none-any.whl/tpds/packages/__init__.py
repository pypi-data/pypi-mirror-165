import os

def get_package_manifest():
    return os.path.join(os.path.dirname(__file__), 'packages.yaml')
    
__all__ = ['get_package_manifest']
