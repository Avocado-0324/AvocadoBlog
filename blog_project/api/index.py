import sys
import os

# 添加项目根目录到 Python 路径
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if path not in sys.path:
    sys.path.append(path)

from blog_project.wsgi import application
app = application