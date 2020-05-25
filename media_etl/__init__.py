import sys
import os
BASE_DIR, SCRIPT_NAME = os.path.split(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
print(sys.path)
__all__ = ['postgres_etl']