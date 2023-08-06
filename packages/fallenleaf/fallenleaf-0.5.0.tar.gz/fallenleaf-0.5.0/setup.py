import setuptools

with open("README.md", "r") as fh:
	description = fh.read()

setuptools.setup(
	name = "fallenleaf",
	version = "0.5.0",
	author = "nakanoyoichi83",
	author_mail = "nakanoyoichi83@gmail.com",
	packages = ["fallenleaf"],
	description = "Fallenleaf is simple dependecy injection container",
	long_description = description,
	long_description_content_type="text/markdown",
	url="https://github.com/AfterSchoolTeaParty/fallenleaf",
	license="MIT",
	python_requires=">=3.8",
	install_requires=["werkzeug"]
)