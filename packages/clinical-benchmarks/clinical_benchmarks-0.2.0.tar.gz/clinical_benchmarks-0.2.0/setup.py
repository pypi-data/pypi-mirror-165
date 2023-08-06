import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='clinical_benchmarks',
    version='0.2.0',
    author="Alex Bennett",
    author_email="alexmbennett2@gmail.com",
    description="A repo of clinical benchmarks for MIMIC-IV",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kind-lab/clinical-benchmarks",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts':
        ['clinical_benchmarks = clinical_benchmarks.__main__:main']
    },
)
