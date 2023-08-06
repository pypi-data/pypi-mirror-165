from setuptools import setup, Extension

VERSION = (1, 0, 0)

setup(
    name="pylzf-c",
    description="liblzf的C扩展，由python-lzf项目修改",
    version=".".join(filter(None, map(str, VERSION))),
    author="GaoFeng",
    author_email="lfxx1994@gmail.com",
    url="http://github.com/teepark/python-lzf",
    license="BSD",
    ext_modules=[Extension(
        'lzf',
        ['lzf_module.c', 'lzf_c.c', 'lzf_d.c'],
        include_dirs=('.',),
        extra_compile_args=['-Wall'])],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: C",
        "Topic :: System :: Archiving :: Compression",
        'Programming Language :: Python :: 3',
    ]
)
