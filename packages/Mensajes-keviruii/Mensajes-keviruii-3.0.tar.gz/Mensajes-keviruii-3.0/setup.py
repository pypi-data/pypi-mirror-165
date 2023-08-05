from setuptools import setup, find_packages
setup(
    name = "Mensajes-keviruii",
    version = "3.0",
    description = "Un paquete para saludar y despedir",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author = "Kevin Ruiz",
    author_email = "kevinagustinrockz@gmail.com",
    url = "http://hcosta.info",
    license_files=['LICENSE'],
    packages=find_packages(),
    scripts = [],
    test_suite='tests',
    install_requires=[paquete.strip() for paquete in open('requirements.txt').readlines()],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Topic :: Utilities'
    ]
)


