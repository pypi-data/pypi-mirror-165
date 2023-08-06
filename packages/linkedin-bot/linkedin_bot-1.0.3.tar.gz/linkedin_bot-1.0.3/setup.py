import setuptools

with open("README.md", "r", encoding="utf-8") as readme_file:
    readme = readme_file.read()

def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]

install_reqs = parse_requirements('requirements/requirements.txt')
reqs = [str(ir) for ir in install_reqs if not str(ir).startswith("-") ]

VERSION ='1.0.3'

setuptools.setup(
    name="linkedin_bot",
    version=VERSION, 
    description="This library allow to do automatisation actions like, share and comment on LinkedIn",
    long_description_content_type="text/markdown",
    author="ADEBO",
    author_email="madebo@kaisensdata.fr",
    license="MIT",
    long_description=readme,
    url="https://gitlab.kaisens.fr/amouhite02/automatisation-rs",
    packages=setuptools.find_packages(exclude=['tests']),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.5",
    install_requires=reqs,
    keywords=[
        'linkedin', 'bot', 'bot_linkedin', 'automatisation',
    ],
)
