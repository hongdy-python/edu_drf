import os

import django
from celery import Celery

# 主程序

# 创建celery实例对象
app = Celery()

# 把celery和django进行结合，识别并加载django的配置文件
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edu_api.settings.develop')
django.setup()

# 通过创建的实例对象加载配置
app.config_from_object("my_task.config")

# 将添加任务到实例对象中  自动找到该目录下的tasks文件中的任务
# app.autodiscover_tasks(['任务1'，'任务2'])
app.autodiscover_tasks(['my_task.sms','my_task.file'])

# 启动celery  在项目的跟目录下执行启动命令
# celery -A my_task.main worker --loglevel=info -P eventlet