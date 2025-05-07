# routes/auth/__init__.py

from .login import auth_bp
from .oauth import *  # 导入oauth模块中的所有内容
# oauth routes already imported via login.py


