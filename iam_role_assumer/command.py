"""
The command line interface to stackility.

Major help from: https://www.youtube.com/watch?v=kNke39OZ2k0
"""
import boto3
import click
import sys
import platform

valid_systems = [
    'linux',
    'darwin'
]

default_session_name = 'sts-access'
default_duration = 3600


@click.group()
@click.version_option(version='0.1.0')
def cli():
    pass


@cli.command()
@click.option('--role', '-r', help='IAM role', required=True)
@click.option('--session', '-s', help='session name')
@click.option('--duration', '-t', help='duration, in seconds, of the role session')
@click.option('--profile', '-p', help='profile for the STS client creation')
@click.option('--region', help='AWS region')
def assume(role, session, duration, profile, region):
    '''
    print needed bash variables to assume the indicated role
    example: $(iam_role_assumer assume -r <role-arn>)
    '''
    try:
        if not region:
            region = find_myself()

        if not session:
            session = default_session_name

        try:
            duration = int(duration)
        except:
            duration = default_duration

        if profile:
            s = boto3.Session(
                profile_name=profile,
                region_name=region
            )
            sts_client = s.client('sts')
        else:
            sts_client = boto3.client('sts')

        assumed_role = sts_client.assume_role(
            RoleArn=role,
            RoleSessionName=session,
            DurationSeconds=duration
        )

        session = boto3.session.Session(
            aws_access_key_id=assumed_role['Credentials']['AccessKeyId'],
            aws_secret_access_key=assumed_role['Credentials']['SecretAccessKey'],
            aws_session_token=assumed_role['Credentials']['SessionToken']
        )

        print('export AWS_ACCESS_KEY_ID={}'.format(
                assumed_role['Credentials']['AccessKeyId']
            )
        )

        print('export AWS_SECRET_ACCESS_KEY={}'.format(
                assumed_role['Credentials']['SecretAccessKey']
            )
        )

        print('export AWS_SECURITY_TOKEN={}'.format(
                assumed_role['Credentials']['SessionToken']
            )
        )

        print('export AWS_DEFAULT_REGION={}'.format(region))

        sys.exit(0)
    except Exception as wtf:
        print('echo assume() exploded: {}'.format(wtf))
        sys.exit(1)


@cli.command()
def unset():
    '''
    unset the AWS environment variable for an assumed role.
    example: $(iam_role_assumer unset)
    '''
    print('unset AWS_ACCESS_KEY_ID')
    print('unset AWS_SECRET_ACCESS_KEY')
    print('unset AWS_SECURITY_TOKEN')


def find_myself():
    s = boto3.session.Session()
    region = s.region_name
    if region:
        return region
    else:
        return 'us-east-1'


def verify_real_system():
    try:
        current_system = platform.system().lower()
        return current_system in valid_systems
    except:
        return False

if not verify_real_system():
    print('error: unsupported system')
    sys.exit(1)
