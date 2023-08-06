from setuptools import setup, find_packages

requrements = []
with open('requirements.txt') as f:
        requrements = [line.replace('\n', '') for line in f.readlines()]

print(requrements)



setup(
    name='tb_rna_velo',
    version='0.1',
    license='TEST',
    author="RijeshShrestha",
    author_email='craaabby@gmail.com.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    keywords='example project',
    install_requires=requrements
)