from setuptools import setup, find_packages

setup(
    name="molint",
    version="1.0.4",
    description="扫描py文件",
    author="mzg",
    packages=find_packages(),
    package_data={'': ['.pylintrc']},
    install_requires=['pylint==2.9.5'],
    entry_points={
            'console_scripts': [ # key值为console_scripts
                'molint = molint.scan:main' # 格式为'命令名 = 模块名:函数名'
            ]
        },
)
