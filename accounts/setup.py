from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in accounts/__init__.py
from accounts import __version__ as version

setup(
	name="accounts",
	version=version,
	description="In Store accounting",
	author="aaron M",
	author_email="aaron@frappe.io",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
