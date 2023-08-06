from distutils.core import setup
from setuptools import find_packages

setup(
    name='kioblog',
    packages=find_packages(exclude=('kioblogdev', 'media')),
    version='v0.1.2-alpha',
    license='MIT',
    description='Simple blog for Django',
    author='Eric Bujeque',
    author_email='noikzyr3@gmail.com',
    url='https://github.com/Eric-Bujeque/kioblog',
    download_url='https://github.com/Eric-Bujeque/kioblog/archive/refs/tags/v0.1.2-alpha.tar.gz',
    keywords=['blog', 'django'],
    install_requires=[
        'Django>=3.0',
        'django-robots>=4.0',
        'django-summernote>=0.8.20.0'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',  # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
