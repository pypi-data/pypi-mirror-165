import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
f = open("requirements.txt","w")
f.write('requests\nuser_agent\njson\nsecrets\nnames\nhashlib\nurllib\nuuid\nre\nmechanize\ninstaloader\nbase64 ')

fr = open("requirements.txt",'r')
requires = fr.read().split('\n')
    
setuptools.setup(
    name="SalamEnc",
    version="0.0.1",
    author="keegang_6705",
    author_email="salamhunter@gmail.com",
    description="• encrypt encode text •",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/keegang6705/encrypt_encode",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3",
    install_requires=requires,
)
