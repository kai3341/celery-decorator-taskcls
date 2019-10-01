from setuptools import setup

requirements = (
    'celery',
)

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.md') as history_file:
    history = history_file.read()

long_description = '\n\n'.join((readme, history))

setup(
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Celery taskcls decorator",
    install_requires=requirements,
    license="MIT",
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords='celery_decorator_taskcls',
    name='celery-decorator-taskcls',
    py_modules=['celery_decorator_taskcls'],
    url='https://github.com/kai3341/celery-decorator-taskcls',
    version='0.1.2',
    zip_safe=True,
)
