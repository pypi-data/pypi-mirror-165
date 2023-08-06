from distutils.core import setup

setup(
    name="django4-oss-storage",                # 设置包名，pip install fakerDemo
    version="1.0.0",                           # 版本号
    description='resolved the "force_text" issue in django4.0 version not supported by aliyun oss module',  # 包的描述信息
    author="wj",                               # 作者
    py_modules=[                               # 设置发布的包的文件列表，只要是要发布上线的都要把路径填上
        'django4_oss_storage.backends',
        'django4_oss_storage.defaults',
    ]
)
