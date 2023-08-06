from setuptools import find_packages, setup
from pine import PROJECT_NAME, VERSION

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

with open("README.md") as f:
	long_description = f.read()

setup(
	name=PROJECT_NAME,
	description="CLI to manage Multi-tenant deployments for Melon apps",
	long_description=long_description,
	long_description_content_type="text/markdown",
	version=VERSION,
	license="GPLv3",
	author="Alphamonak Solutions",
	author_email="amonak@alphamonak.com",
	url="https://monakerp.com/pine",
	project_urls={
		"Documentation": "https://docs.monakerp.com/docs/user/en/pine",
		"Source": "https://github.com/amonak/pine",
		"Changelog": "https://github.com/amonak/pine/releases",
	},
	classifiers=[
		"Development Status :: 5 - Production/Stable",
		"Environment :: Console",
		"License :: OSI Approved :: GNU Affero General Public License v3",
		"Natural Language :: English",
		"Operating System :: MacOS",
		"Operating System :: OS Independent",
		"Topic :: Software Development :: Build Tools",
		"Topic :: Software Development :: User Interfaces",
		"Topic :: System :: Installation/Setup",
	],
	packages=find_packages(),
	python_requires="~=3.6",
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires,
	entry_points={"console_scripts": ["pine=pine.cli:cli"]},
)
