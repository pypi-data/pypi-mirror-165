import json
from typing import Optional, Any, Union, Dict

from aws_cdk.aws_apigatewayv2 import CfnApi, CfnStage
from aws_cdk.aws_cloudfront import *
from aws_cdk.aws_cloudfront_origins import HttpOrigin
from aws_cdk.aws_iam import ServicePrincipal
from aws_cdk.aws_logs import LogGroup, RetentionDays
from aws_cdk.aws_ssm import StringParameter
from aws_cdk.core import Stack, IResolvable, RemovalPolicy
from b_cfn_custom_api_key_authorizer.custom_authorizer import ApiKeyCustomAuthorizer
from b_cfn_custom_userpool_authorizer.config.user_pool_config import UserPoolConfig
from b_cfn_custom_userpool_authorizer.config.user_pool_ssm_config import UserPoolSsmConfig
from b_cfn_custom_userpool_authorizer.user_pool_custom_authorizer import UserPoolCustomAuthorizer


class Api(CfnApi):
    def __init__(
            self,
            scope: Stack,
            id: str,
            name: str,
            api_key_selection_expression: Optional[str] = None,
            base_path: Optional[str] = None,
            body: Any = None,
            body_s3_location: Optional[Union[IResolvable, CfnApi.BodyS3LocationProperty]] = None,
            cors_configuration: Optional[Union[IResolvable, CfnApi.CorsProperty]] = None,
            credentials_arn: Optional[str] = None,
            description: Optional[str] = None,
            disable_execute_api_endpoint: Optional[Union[bool, IResolvable]] = None,
            disable_schema_validation: Optional[Union[bool, IResolvable]] = None,
            fail_on_warnings: Optional[Union[bool, IResolvable]] = None,
            protocol_type: Optional[str] = None,
            route_key: Optional[str] = None,
            route_selection_expression: Optional[str] = None,
            tags: Any = None,
            target: Optional[str] = None,
            version: Optional[str] = None,
            **kwargs
    ) -> None:
        self.__scope = scope
        self.__name = name

        super().__init__(
            scope=scope,
            id=id,
            api_key_selection_expression=api_key_selection_expression,
            base_path=base_path,
            body=body,
            body_s3_location=body_s3_location,
            cors_configuration=cors_configuration,
            credentials_arn=credentials_arn,
            description=description,
            disable_execute_api_endpoint=disable_execute_api_endpoint,
            disable_schema_validation=disable_schema_validation,
            fail_on_warnings=fail_on_warnings,
            name=name,
            protocol_type=protocol_type,
            route_key=route_key,
            route_selection_expression=route_selection_expression,
            tags=tags,
            target=target,
            version=version,
            **kwargs
        )

        # Deprecated.
        self.authorizer: Optional[UserPoolCustomAuthorizer] = None
        # Authorizers.
        self.user_pool_authorizer: Optional[UserPoolCustomAuthorizer] = None
        self.api_key_authorizer: Optional[ApiKeyCustomAuthorizer] = None

        self.default_stage: Optional[CfnStage] = None
        self.cdn: Optional[Distribution] = None

    """
    Authorizers.
    """

    # Deprecated. Do not use this function.
    def enable_authorizer(
            self,
            user_pool_config_for_auth: Union[UserPoolConfig, UserPoolSsmConfig],
            **kwargs
    ) -> None:
        self.enable_user_pool_authorizer(user_pool_config_for_auth, **kwargs)

    def enable_user_pool_authorizer(
            self,
            user_pool_config_for_auth: Union[UserPoolConfig, UserPoolSsmConfig],
            **kwargs
    ) -> UserPoolCustomAuthorizer:
        authorizer = UserPoolCustomAuthorizer(
            scope=self.__scope,
            name=f'{self.__name}Authorizer',
            api=self,
            user_pool_config=user_pool_config_for_auth,
            **kwargs
        )

        self.authorizer = authorizer
        self.user_pool_authorizer = authorizer

        return authorizer

    def enable_api_key_authorizer(self, **kwargs) -> ApiKeyCustomAuthorizer:
        authorizer = ApiKeyCustomAuthorizer(
            scope=self.__scope,
            resource_name_prefix=f'{self.__name}ApiKeyAuthorizer',
            api=self,
            **kwargs
        )

        self.api_key_authorizer = authorizer

        return authorizer

    """
    Other.
    """

    def enable_default_stage(self, stage_name: str, enable_logging: bool = False, **kwargs) -> None:
        """
        Creates a stage resource for this API. A stage could represent a version (V1, V2, V3...)
        or an environment (DEV, STAGE, PROD...) or anything else actually...

        :param stage_name: The name of the stage e.g. "V1", "PROD", etc.
        :param enable_logging: A flag that (if set to True) enables API logging by creating a logging
            group and attaching it to the stage. WARNING! If this flag is set to True, the named
            argument "access_log_settings" in kwargs will be overridden.
        :param kwargs: Other named arguments for maximum flexibility.

        :return: No return.
        """
        if enable_logging:
            log_group = LogGroup(
                scope=self.__scope,
                id=f'{self.__name}{stage_name}StageLogGroup',
                retention=RetentionDays.ONE_MONTH,
                # At some point in time you will get this weird error:
                # Cannot enable logging. Policy document length breaking Cloudwatch Logs Constraints,
                # either < 1 or > 5120 (Service: AmazonApiGatewayV2; ...), hence we need to
                # prefix the name with "/aws/vendedlogs/".
                log_group_name=f'/aws/vendedlogs/{self.__name}-{stage_name}-Stage-LogGroup',
                removal_policy=RemovalPolicy.DESTROY,
            )

            log_group.grant_write(ServicePrincipal('apigateway.amazonaws.com'))

            kwargs['access_log_settings'] = CfnStage.AccessLogSettingsProperty(
                destination_arn=log_group.log_group_arn,
                format=json.dumps({
                    'requestId': '$context.requestId',
                    'ip': '$context.identity.sourceIp',
                    'requestTime': '$context.requestTime',
                    'httpMethod': '$context.httpMethod',
                    'routeKey': '$context.routeKey',
                    'status': '$context.status',
                    'protocol': '$context.protocol',
                    'responseLength': '$context.responseLength'
                })
            )

        self.default_stage = CfnStage(
            scope=self.__scope,
            id=f'{self.__name}Stage',
            api_id=self.ref,
            stage_name=stage_name,
            auto_deploy=True,
            **kwargs
        )

    def expose_full_url_ssm(self, ssm_key_name: str) -> None:
        StringParameter(
            scope=self.__scope,
            id=ssm_key_name,
            parameter_name=ssm_key_name,
            string_value=self.full_url
        )

    def enable_cdn(
            self,
            default_behavior_cache_policy: Optional[CachePolicy] = None,
            additional_behaviors: Optional[Dict[str, BehaviorOptions]] = None,
            http_version: HttpVersion = HttpVersion.HTTP2,
            price_class: PriceClass = PriceClass.PRICE_CLASS_100,
            **kwargs
    ) -> None:
        self.cdn = Distribution(
            scope=self.__scope,
            id=f'{self.__name}Cdn',
            default_behavior=BehaviorOptions(
                allowed_methods=AllowedMethods.ALLOW_ALL,
                cached_methods=CachedMethods.CACHE_GET_HEAD_OPTIONS,
                cache_policy=default_behavior_cache_policy,
                viewer_protocol_policy=ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                origin=HttpOrigin(
                    domain_name=self.api_domain_name,
                    origin_path=self.api_origin_path
                )
            ),
            additional_behaviors=additional_behaviors,
            http_version=http_version,
            price_class=price_class,
            **kwargs
        )

    @property
    def full_url(self) -> str:
        """
        Property for API url. If CDN is set, then it returns CDN url.

        :return: Returns this API's (or CDN's if set) full url.
        """
        # In case CDN is enabled - return CDN URL.
        if self.cdn:
            return f'https://{self.cdn.domain_name}'
        # In case CDN is not enabled - return API URL.
        else:
            return f'https://{self.api_domain_name}{self.api_origin_path}'

    """
    API-related props.
    """

    @property
    def api_domain_name(self):
        return f'{self.ref}.execute-api.{self.__scope.region}.amazonaws.com'

    @property
    def api_arn(self) -> str:
        """
        Property for API ARN.

        :return: Returns this API's amazon resource name (ARN).
        """
        return f'arn:aws:apigateway:{self.__scope.region}::/restapis/{self.ref}/stages/{self.stage.stage_name}'

    @property
    def api_origin_path(self) -> str:
        """
        Property for API origin path (usually what comes after domain name).

        :return: Origin path which is a stage name (e.g. /dev).
        """
        if not self.default_stage:
            raise ValueError('Default stage is not set.')

        return f'/{self.default_stage.stage_name}'

    """
    CDN-related props.
    """

    @property
    def cdn_domain_name(self):
        return self.cdn.domain_name

    @property
    def cdn_arn(self) -> str:
        """
        Property for CDN ARN.

        :return: Returns this CDN's amazon resource name (ARN).
        """
        return f'arn:aws:cloudfront::{self.__scope.account}:distribution/{self.cdn.distribution_id}'
