import requests
from setuptools import setup


response = requests.get('https://raw.githubusercontent.com/BdVade/DjangoRestAdmin/main/README.md')

README = response.text
# The directory containing this file

# The text of the README file
# README = (HERE / "README.md").read_text()
setup(
    name="drf-admin",
    version="0.1.0",
    description="A package to generate CRUD endpoints for registered models with the Django-REST Framework.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/BdVade/DjangoRestAdmin/",
    author="Aderibigbe Victor",
    author_email="victoraderibigbe03@gmail.com",
    keywords=['django', 'python', 'django-rest-framework', "admin", "api"],
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        'Intended Audience :: Developers',  # Define that your audience are developers
        'Topic :: Software Development :: Build Tools'
    ],
    packages=[],
    include_package_data=True,
    install_requires=["Django>=3.2.9", "djangorestframework", "coreapi"],
    package_dir={"": "restadmin"},
    python_requires='>=3',
    test_suite='load_tests.get_suite'



    # project_urls={
    #
    # },


)
