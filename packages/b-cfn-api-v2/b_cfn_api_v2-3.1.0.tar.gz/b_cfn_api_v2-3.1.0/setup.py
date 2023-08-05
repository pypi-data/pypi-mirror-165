from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

with open('VERSION') as file:
    VERSION = file.read()
    VERSION = ''.join(VERSION.split())

setup(
    name='b_cfn_api_v2',
    version=VERSION,
    license='Apache License 2.0',
    packages=find_packages(exclude=[
        # Exclude virtual environment.
        'venv',
        # Exclude test source files.
        'b_cfn_api_v2_test'
    ]),
    description=(
        'Convenient wrapper around CfnApi.'
    ),
    long_description=README + '\n\n' + HISTORY,
    long_description_content_type='text/markdown',
    include_package_data=True,
    install_requires=[
        'b_cfn_custom_userpool_authorizer>=1.0.0,<2.0.0',
        'b_cfn_custom_api_key_authorizer>=2.2.0,<3.0.0',

        'aws-cdk.assets>=1.90.0,<2.0.0',
        'aws-cdk.aws-acmpca>=1.90.0,<2.0.0',
        'aws-cdk.aws-apigatewayv2>=1.90.0,<2.0.0',
        'aws-cdk.aws-applicationautoscaling>=1.90.0,<2.0.0',
        'aws-cdk.aws-autoscaling-common>=1.90.0,<2.0.0',
        'aws-cdk.aws-certificatemanager>=1.90.0,<2.0.0',
        'aws-cdk.aws-cloudformation>=1.90.0,<2.0.0',
        'aws-cdk.aws-cloudfront>=1.90.0,<2.0.0',
        'aws-cdk.aws-cloudfront-origins>=1.90.0,<2.0.0',
        'aws-cdk.aws-cloudwatch>=1.90.0,<2.0.0',
        'aws-cdk.aws-codeguruprofiler>=1.90.0,<2.0.0',
        'aws-cdk.aws-codestarnotifications>=1.90.0,<2.0.0',
        'aws-cdk.aws-cognito>=1.90.0,<2.0.0',
        'aws-cdk.aws-dynamodb>=1.90.0,<2.0.0',
        'aws-cdk.aws-ec2>=1.90.0,<2.0.0',
        'aws-cdk.aws-ecr>=1.90.0,<2.0.0',
        'aws-cdk.aws-ecr-assets>=1.90.0,<2.0.0',
        'aws-cdk.aws-efs>=1.90.0,<2.0.0',
        'aws-cdk.aws-elasticloadbalancingv2>=1.90.0,<2.0.0',
        'aws-cdk.aws-events>=1.90.0,<2.0.0',
        'aws-cdk.aws-iam>=1.90.0,<2.0.0',
        'aws-cdk.aws-kinesis>=1.90.0,<2.0.0',
        'aws-cdk.aws-kms>=1.90.0,<2.0.0',
        'aws-cdk.aws-lambda>=1.90.0,<2.0.0',
        'aws-cdk.aws-logs>=1.90.0,<2.0.0',
        'aws-cdk.aws-route53>=1.90.0,<2.0.0',
        'aws-cdk.aws-s3>=1.90.0,<2.0.0',
        'aws-cdk.aws-s3-assets>=1.90.0,<2.0.0',
        'aws-cdk.aws-signer>=1.90.0,<2.0.0',
        'aws-cdk.aws-sns>=1.90.0,<2.0.0',
        'aws-cdk.aws-sqs>=1.90.0,<2.0.0',
        'aws-cdk.aws-ssm>=1.90.0,<2.0.0',
        'aws-cdk.cloud-assembly-schema>=1.90.0,<2.0.0',
        'aws-cdk.core>=1.90.0,<2.0.0',
        'aws-cdk.custom-resources>=1.90.0,<2.0.0',
        'aws-cdk.cx-api>=1.90.0,<2.0.0',
        'aws-cdk.region-info>=1.90.0,<2.0.0',
    ],
    keywords='AWS API Gateway',
    url='https://github.com/biomapas/B.CfnApiV2.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
