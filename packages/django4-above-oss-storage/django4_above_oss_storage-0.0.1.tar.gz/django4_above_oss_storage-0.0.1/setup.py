from distutils.core import setup

setup(
    name="django4_above_oss_storage",  # 设置包名，pip install fakerDemo
    version="0.0.1",    # 版本号
    description="修复django4.0以后文本转换格式BUG报错", # 包的描述信息
    author="ss",     # 作者
    py_modules = [        # 设置发布的包的文件列表，只要是要发布上线的都要把路径填上
        'django4_above_oss_storage.backends',
        'django4_above_oss_storage.defaults',
    ]
)