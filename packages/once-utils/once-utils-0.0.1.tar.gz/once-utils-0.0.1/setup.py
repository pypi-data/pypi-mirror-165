from setuptools import setup, find_packages

setup(
    name="once-utils",
    version="0.0.1",
    keywords=["pip", "once-utils"],
    description="Simplest utils.",
    long_description="A lib with simple style.",
    license="MIT Licence",
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers'],

    url="https://github.com/Mingyueyixi/once-utils",
    author="Lu",
    author_email="Mingyueyixi@hotmail.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[]
)
