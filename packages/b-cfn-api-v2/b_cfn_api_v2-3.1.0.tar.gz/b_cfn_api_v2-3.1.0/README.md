# B.CfnApiV2

![Pipeline](https://github.com/Biomapas/B.CfnApiV2/workflows/Pipeline/badge.svg?branch=master)

An API Gateway resource that adds convenient functionality over traditional `CfnApi` resource. 
It lets you easily enable authorization, stages, and CDNs. 

### Description

Essentially this resource is a wrapper resource for `aws_apigatewayv2` module's `CfnApi`. Meaning, 
that you can easily swap `CfnApi` and this `Api` resource with no major impact. But why would you 
want to switch a traditional `CfnApi` to this one. Mainly these convenient features:
- Easy to add `CloudFront` distribution on top of the API (enabling CDN).
- Easy to enable `Stage` and attached to the api.
- Easy to add authorization with `UserPoolAuthorizer` & `ApiKeyAuthorizer`.

### Remarks

[Biomapas](https://www.biomapas.com/) aims to modernise life-science industry by sharing its IT knowledge with other companies and the community. 
This is an open source library intended to be used by anyone. 
Improvements and pull requests are welcome. 

### Related technology

- Python3
- AWS CDK
- AWS Lambda
- AWS API Gateway
- AWS CloudFront
- AWS User Pool authorization

### Assumptions

This project assumes you know what Lambda functions are and how code is being shared between them
(Lambda layers). 

- Excellent knowledge in IaaC (Infrastructure as a Code) principles.
- Excellent knowledge in Lambda functions and API Gateway service.  
- Good experience in AWS CDK and AWS CloudFormation.

### Useful sources

- AWS CDK:<br>https://docs.aws.amazon.com/cdk/api/latest/docs/aws-construct-library.html
- AWS CloudFormation:<br>https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html
- AWS API Gateway:<br>https://docs.aws.amazon.com/apigateway/latest/developerguide/welcome.html
- AWS API Gateway V2:<br>https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html
- Custom User Pool Authorizer:<br>https://github.com/Biomapas/B.CfnCustomUserPoolAuthorizer
- Custom api key authorizer:<br>https://github.com/Biomapas/B.CfnCustomApiKeyAuthorizer
- Custom user pool authorizer:<br>https://github.com/Biomapas/B.CfnCustomUserPoolAuthorizer

### Install

Before installing this library, ensure you have these tools setup:

- Python / Pip
- AWS CDK

To install this project from source run:

```
pip install .
```


Or you can install it from a PyPi repository:

```
pip install b-cfn-api-v2
```


### Usage & Examples

The traditional way of creating an API looks something like this:

```python
from aws_cdk.aws_apigatewayv2 import CfnApi

CfnApi(
    scope=Stack(),
    id='Api',
    name='Api',
    description='Sample description.',
    protocol_type='HTTP',
    cors_configuration=CfnApi.CorsProperty(
        allow_methods=['GET', 'PUT', 'POST', 'OPTIONS', 'DELETE'],
        allow_origins=['*'],
        allow_headers=[
            'Content-Type',
            'Authorization'
        ],
        max_age=300
    )
)
```

To create our resource `Api` is exactly the same:<br>
(It works since `Api` is a pure wrapper of `CfnApi` resource.)

```python
from b_cfn_api_v2.api import Api

Api(
    scope=Stack(),
    id='Api',
    name='Api',
    description='Sample description.',
    protocol_type='HTTP',
    cors_configuration=Api.CorsProperty(
        allow_methods=['GET', 'PUT', 'POST', 'OPTIONS', 'DELETE'],
        allow_origins=['*'],
        allow_headers=[
            'Content-Type',
            'Authorization'
        ],
        max_age=300
    )
)
```

Three main advantages of this `Api` resource:

- **Easy to enable default stage.**

```python
from b_cfn_api_v2.api import Api

api = Api(...)
api.enable_default_stage('dev')
```

- **Easy to enable authorization.**

```python
from b_cfn_api_v2.api import Api
from b_cfn_custom_userpool_authorizer.config.user_pool_config import UserPoolConfig

api = Api(...)

# Your authorized endpoint will require `Authorization`
# supplied in headers.
# Read more:
# https://github.com/Biomapas/B.CfnCustomUserPoolAuthorizer
api.enable_user_pool_authorizer(UserPoolConfig(
    user_pool_id='id',
    user_pool_region='region',
    user_pool_client_id='client'
))

# Your authorized endpoint will require `ApiKey` and `ApiSecret`
# supplied in headers.
# Read more:
# https://github.com/Biomapas/B.CfnCustomApiKeyAuthorizer
api.enable_api_key_authorizer()
```

- **Easy to enable CDN.**

```python
from b_cfn_api_v2.api import Api
from aws_cdk.aws_cloudfront import CachePolicy

api = Api(...)
api.enable_cdn(default_behavior_cache_policy=CachePolicy.CACHING_OPTIMIZED)
```

### Testing

This package has integration tests based on **pytest**.
To run tests simply run:

```
pytest b_cfn_api_v2_test/integration/tests
```

### Contribution

Found a bug? Want to add or suggest a new feature? 
Contributions of any kind are gladly welcome. 
You may contact us directly, create a pull-request or an issue in github platform. 
Lets modernize the world together.
