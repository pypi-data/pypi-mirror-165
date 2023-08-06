from setuptools import setup,find_packages

with open("README.md","r",encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='tktk',
      version='0.4.1',
      description='tkinter的增强控件,将tkinter的基础控件进行封装,给予更强大的控件功能,所有控件继承于LabelFrame进行封装,使用方法和普通控件没什么区别;',
      long_description=long_description,
      long_description_content_type='text/markdown',
      classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
      url='https://gitee.com/w-8/tktk',
      author='bili:凿寂',
      author_email='mdzzdyxc@163.com',
      license='MIT',
      packages=find_packages(),
      zip_safe=True
     )
#python3 setup.py sdist bdist_wheel
#python3 -m twine upload dist/*