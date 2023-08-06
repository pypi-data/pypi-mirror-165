from setuptools import setup, find_packages


with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='raya',
    packages=find_packages(),
    version='0.8.1',
    license='MIT',
    description='Raya OS skelaton by Unlimited Robotics',
    long_description=readme,
    author='Ofir Ozeri',
    author_email='ofiro@unlimited-robotics.com',
    url='', 
    python_requires=">=3.8",
    install_requires=[
        'rayasdk'
    ]  
)
