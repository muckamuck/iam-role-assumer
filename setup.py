from setuptools import setup
setup(
    name="iam_role_assumer",
    version='0.1.0',
    packages=['iam_role_assumer'],
    description='Assume an AWS IAM role',
    author='Chuck Muckamuck',
    author_email='Chuck.Muckamuck@gmail.com',
    install_requires=[
        "boto3>=1.4",
        "Click>=6.7"
    ],
    entry_points="""
        [console_scripts]
        iam_role_assumer=iam_role_assumer.command:cli
    """
)
