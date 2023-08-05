from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: MacOS :: MacOS X',
    'Programming Language :: Python :: 3.8'
]

setup(
    name='tiffextract',
    version='0.0.1',
    description='Converts AFM images with the raw format file .ibw into .tif images from each AFM channel used in the measurement',
    url='https://engineering.case.edu/centers/sdle/',
    author='Roger French(ORCID:000000-0002-6162-0532), Liangyi Huang(ORCID:0000-0003-0845-3293), Will Oltjen(ORCID:0000-0003-0380-1033),Arafath Nihar, Jiqi Liu(ORCiD: 0000-0003-2016-4160), Justin Glynn, Kehley Coleman, Harsha Nandan Madiraju',
    author_email='roger.french@case.edu, lxh442@case.edu, wco3@case.edu,axn392@case.edu,jxl1763@case.edu,jpg90@case.edu, kac196@case.edu, hxm434@case.edu',
    license='BSD License (BSD-3)',
    classifiers=classifiers,
    keywords='AFM, conversion, automated, .ibw to .tif',
    packages=find_packages(),
    dependencies='os',
    install_requires=['']
)
