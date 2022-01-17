from setuptools import setup, find_packages


def read(f):
    return open(f, 'r', encoding='utf-8').read()


setup(
    name="django-request-viewer",
    version='1.0.1',
    description="Log and view requests and exceptions made on your Django app",
    long_description=read("README.md"),
    long_description_content_type='text/markdown',
    url="https://github.com/sirrobot01/django-request-viewer",
    author="Mukhtar Akere",
    author_email="akeremukhtar10@gmail.com",
    license="BSD-3-Clause",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 3.1",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    install_requires=[
        "django>=2.2"
    ],
    packages=find_packages(),
    include_package_data=True,
    extras_require={},
    project_urls={
        'Source': 'https://github.com/sirrobot01/django-request-viewer',
    },
)
