import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sdutilities",
    version="1.1",
    author="Stephen Olsen, Taylor Ward, McKenna Magoffin",
    author_email="stephenolsen@sociallydetermined.com, \
                  taylorward@sociallydetermined.com, \
                  mckennamagoffin@sociallydetermined.com",
    description="This package is intended to implement uniformity across \
                 SD Data Science projects.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    Homepage="https://github.com/orgs/SociallyDetermined/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pandas >= 1.2.3",
        "numpy >= 1.16.5",
        "census >= 0.8.15",
        "us >= 2.0.2",
        "sqlalchemy >= 1.3.9",
        "matplotlib >= 3.1.1",
        "setuptools >= 50.3.0",
        "boto3 >= 1.17.43",
        "botocore >= 1.19.52",
    ],
    package_data={
        "sdutilities": ["cfg_tables/grp_table_cfg.json", "cfg_tables/sample_table_cfg.json"]
    },
)
