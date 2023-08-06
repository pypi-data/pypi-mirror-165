"""Package setup"""

from pathlib import Path

from setuptools import setup  # type: ignore

import fortigate_api as package

VERSION = "0.2.6"
PACKAGE = package.__title__
PACKAGE_ = package.__title__.lower().replace("-", "_")  # PEP 503 normalization
ROOT = Path(__file__).parent.resolve()
README = "README.rst"

if __name__ == "__main__":
    setup(
        name=PACKAGE_,
        packages=[PACKAGE_],
        package_data={PACKAGE_: ["py.typed"]},
        version=VERSION,
        description=package.__summary__,
        license=package.__license__,
        long_description=open(README).read(),
        long_description_content_type="text/x-rst",
        author=package.__author__,
        author_email=package.__email__,
        url=package.__url__,
        download_url=package.__download_url__,
        keywords="fortigate, api, fortios, firewall, networking, telecommunication",
        python_requires=">=3.8",
        install_requires=["requests"],
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "Intended Audience :: System Administrators",
            "Intended Audience :: Telecommunications Industry",
            # "Operating System :: FortiOS",
            "Topic :: System :: Networking :: Firewalls",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3.8",
            "Natural Language :: English",
        ],
    )
