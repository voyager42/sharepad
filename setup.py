from setuptools import setup, find_packages

version = '0.1'

setup(
    name='sharepad',
    version=version,
    description='Share your Andiccio24 pizza creations',
    long_description=open('README.rst', 'rb').read(),
    author='Johan Kohler',
    author_email='johan.kohler@gmail.com',
    url='https://github.com/voyager42/sharepad',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask==0.10.1',
        'Jinja2==2.7.3',
        'MarkupSafe==0.23',
        'Werkzeug==0.9.6',
        'gunicorn==19.0.0',
        'pretty==0.1',
        'flask-sqlalchemy',
    ],
)
