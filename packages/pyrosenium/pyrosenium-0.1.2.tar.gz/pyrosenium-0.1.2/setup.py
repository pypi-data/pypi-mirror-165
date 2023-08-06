from setuptools import setup, find_packages

setup(
    name="pyrosenium",
    version="0.1.2",    
    description="A example Python package",
    url="https://gitlab.com/pyrosenium/pyrosenium",
    author="Namdy Yeung",
    author_email="dropicode@protonmail.com",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "pytest==7.1.2",
        "selenium==4.2.0",
        "webdriver-manager==3.7.0"                    
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    entry_points={
        'console_scripts': [
            'create-rosepom-app = pyrosenium.rosepom.core.rosepom_app:create_rosepom_app',
        ]
    }
)
