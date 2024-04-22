import os
import sys

parent_dir = os.path.abspath(os.path.join(os.getcwd(), '.'))
sys.path.append(parent_dir)


from models.user import User
from database import session
