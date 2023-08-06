from distutils.core import setup

setup(
    name="django3-oss-gstorage",  # 设置包名，pip install fakerDemo
    version="0.0.1",  # 版本号
    description="django3-oss-gstorage demo zhien",  # 包的描述信息
    author="zhien",  # 作者
    py_modules=[  # 设置发布的包的文件列表，只要是要发布上线的都要把路径填上
        'django3-oss-gstorage/django_oss_storage/__init__',
        'django3-oss-gstorage/django_oss_storage/backends',
        'django3-oss-gstorage/django_oss_storage/defaults',
    ]
)
