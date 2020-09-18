import logging
from arnparse import arnparse
from schematics import Model
from spaceone.inventory.libs.schema.resource import CloudWatchModel, CloudWatchDimensionModel
from schematics.types import ModelType, StringType, IntType, DateTimeType, ListType, BooleanType

_LOGGER = logging.getLogger(__name__)


class Tags(Model):
    key = StringType(deserialize_from="Key")
    value = StringType(deserialize_from="Value")

'''
Listener
'''
class AuthenticationRequestExtraParams(Model):
    string = StringType(deserialize_from="string")


class AuthenticateOidcConfig(Model):
    issuer = StringType(deserialize_from="Issuer")
    authorization_endpoint = StringType(deserialize_from="AuthorizationEndpoint")
    token_endpoint = StringType(deserialize_from="TokenEndpoint")
    user_info_endpoint = StringType(deserialize_from="UserInfoEndpoint")
    client_id = StringType(deserialize_from="ClientId")
    client_secret = StringType(deserialize_from="ClientSecret")
    session_cookie_name = StringType(deserialize_from="SessionCookieName")
    scope = StringType(deserialize_from="Scope")
    session_timeout = IntType(deserialize_from="SessionTimeout")
    authentication_request_extra_params = ModelType(AuthenticationRequestExtraParams,
                                                    deserialize_from="AuthenticationRequestExtraParams")
    on_unauthenticated_request = StringType(deserialize_from="OnUnauthenticatedRequest",
                                            choices=("deny", "allow", "authenticate"))
    use_existing_client_secret = BooleanType(deserialize_from="UseExistingClientSecret")


class AuthenticationRequestExtraParams(Model):
    string = StringType(deserialize_from="string")


class AuthenticateCognitoConfig(Model):
    user_pool_arn = StringType(deserialize_from="UserPoolArn")
    user_pool_client_id = StringType(deserialize_from="UserPoolClientId")
    user_pool_domain = StringType(deserialize_from="UserPoolDomain")
    session_cookie_name = StringType(deserialize_from="SessionCookieName")
    scope = StringType(deserialize_from="Scope")
    session_timeout = IntType(deserialize_from="SessionTimeout")
    authentication_request_extra_params = ModelType(AuthenticationRequestExtraParams,
                                                    deserialize_from="AuthenticationRequestExtraParams")
    on_unauthenticated_request = StringType(deserialize_from="OnUnauthenticatedRequest",
                                            choices=("deny", "allow", "authenticate"))


class RedirectConfig(Model):
    protocol = StringType(deserialize_from="Protocol")
    port = StringType(deserialize_from="Port")
    host = StringType(deserialize_from="Host")
    path = StringType(deserialize_from="Path")
    query = StringType(deserialize_from="Query")
    status_code = StringType(deserialize_from="StatusCode", choices=("HTTP_301", "HTTP_302"))


class FixedResponseConfig(Model):
    message_body = StringType(deserialize_from="MessageBody")
    status_code = StringType(deserialize_from="StatusCode")
    content_type = StringType(deserialize_from="ContentType")


class TargetGroupStickinessConfig(Model):
    enabled = BooleanType(deserialize_from="Enabled")
    duration_seconds = IntType(deserialize_from="DurationSeconds")


class ForwardConfigTargetGroups(Model):
    target_group_arn = StringType(deserialize_from="TargetGroupArn")
    weight = IntType(deserialize_from="Weight")


class ForwardConfig(Model):
    target_groups = ListType(ModelType(ForwardConfigTargetGroups), deserialize_from="TargetGroups")
    target_group_stickiness_config = ModelType(TargetGroupStickinessConfig,
                                               deserialize_from="TargetGroupStickinessConfig")


class ListenerCertificates(Model):
    certificate_arn = StringType(deserialize_from="CertificateArn")
    is_default = BooleanType(deserialize_from="IsDefault")


class ListenerDefaultActions(Model):
    type = StringType(deserialize_from="Type", choices=("forward", "authenticate-oidc",
                                                        "authenticate-cognito", "redirect", "fixed-response"))
    target_group_arn = StringType(deserialize_from="TargetGroupArn")
    authenticate_oidc_config = ModelType(AuthenticateOidcConfig, deserialize_from="AuthenticateOidcConfig")
    authenticate_cognito_config = ModelType(AuthenticateCognitoConfig, deserialize_from="AuthenticateCognitoConfig")
    order = IntType(deserialize_from="Order")
    redirect_config = ModelType(RedirectConfig, deserialize_from="RedirectConfig")
    fixed_response_config = ModelType(FixedResponseConfig, deserialize_from="FixedResponseConfig")
    forward_config = ModelType(ForwardConfig, deserialize_from="ForwardConfig")


class Listener(Model):
    listener_arn = StringType(deserialize_from="ListenerArn")
    load_balancer_arn = StringType(deserialize_from="LoadBalancerArn")
    port = IntType(deserialize_from="Port")
    protocol = StringType(deserialize_from="Protocol", choices=("HTTP", "HTTPS", "TCP", "TLS", "UDP", "TCP_UDP"))
    certificates = ListType(ModelType(ListenerCertificates), deserialize_from="Certificates")
    ssl_policy = StringType(deserialize_from="SslPolicy")
    default_actions = ListType(ModelType(ListenerDefaultActions), deserialize_from="DefaultActions")


'''
Target Group
'''
class TargetGroupAttributes(Model):
    stickiness_enabled = StringType(default="")
    deregistration_delay_timeout_seconds = StringType(default="")
    stickiness_type = StringType(default="")
    stickiness_lb_cookie_duration_seconds = StringType(default="")
    slow_start_duration_seconds = StringType(default="")
    load_balancing_algorithm_type = StringType(default="")


class Matcher(Model):
    http_code = StringType(deserialize_from="HttpCode")


class TargetGroup(Model):
    target_group_arn = StringType(deserialize_from="TargetGroupArn")
    target_group_name = StringType(deserialize_from="TargetGroupName")
    protocol = StringType(deserialize_from="Protocol", choices=("HTTP", "HTTPS", "TCP", "TLS", "UDP", "TCP_UDP"))
    port = IntType(deserialize_from="Port")
    vpc_id = StringType(deserialize_from="VpcId")
    health_check_protocol = StringType(deserialize_from="HealthCheckProtocol", choices=("HTTP", "HTTPS", "TCP",
                                                                                        "TLS", "UDP", "TCP_UDP"))
    health_check_port = StringType(deserialize_from="HealthCheckPort")
    health_check_enabled = BooleanType(deserialize_from="HealthCheckEnabled")
    health_check_interval_seconds = IntType(deserialize_from="HealthCheckIntervalSeconds")
    health_check_timeout_seconds = IntType(deserialize_from="HealthCheckTimeoutSeconds")
    healthy_threshold_count = IntType(deserialize_from="HealthyThresholdCount")
    unhealthy_threshold_count = IntType(deserialize_from="UnhealthyThresholdCount")
    health_check_path = StringType(deserialize_from="HealthCheckPath")
    matcher = ModelType(Matcher, deserialize_from="Matcher")
    load_balancer_arns = ListType(StringType, deserialize_from="LoadBalancerArns")
    target_type = StringType(deserialize_from="TargetType", choices=("instance", "ip", "lambda"))
    account_id = StringType(default="")
    tags = ListType(ModelType(Tags))
    attributes = ModelType(TargetGroupAttributes)

    def reference(self, region_code):
        return {
            "resource_id": self.target_group_arn,
            "external_link": f"https://console.aws.amazon.com/ec2/v2/home?region={region_code}#TargetGroups:search={self.target_group_arn};sort=targetGroupName"
        }

'''
Load Balancer
'''
class LoadBalancerAttributes(Model):
    access_logs_s3_enabled = StringType(default="")
    idle_timeout_seconds = StringType(default="")
    access_logs_s3_prefix = StringType(default="")
    deletion_protection_enabled = StringType(default="")
    access_logs_s3_bucket = StringType(default="")
    load_balancing_cross_zone_enabled = StringType(default="")


class AvailabilityZonesLoadBalancerAddresses(Model):
    ip_address = StringType(deserialize_from="IpAddress")
    allocation_id = StringType(deserialize_from="AllocationId")
    private_ipv4_address = StringType(deserialize_from="PrivateIPv4Address")


class State(Model):
    code = StringType(deserialize_from="Code", choices=("active", "provisioning", "active_impaired", "failed"))
    reason = StringType(deserialize_from="Reason")


class LoadBalancerAvailabilityZones(Model):
    zone_name = StringType(deserialize_from="ZoneName")
    subnet_id = StringType(deserialize_from="SubnetId")
    load_balancer_addresses = ListType(ModelType(AvailabilityZonesLoadBalancerAddresses),
                                       deserialize_from="LoadBalancerAddresses")


class LoadBalancer(Model):
    load_balancer_arn = StringType(deserialize_from="LoadBalancerArn")
    dns_name = StringType(deserialize_from="DNSName")
    canonical_hosted_zone_id = StringType(deserialize_from="CanonicalHostedZoneId")
    created_time = DateTimeType(deserialize_from="CreatedTime")
    load_balancer_name = StringType(deserialize_from="LoadBalancerName")
    scheme = StringType(deserialize_from="Scheme", choices=("internet-facing", "internal"))
    vpc_id = StringType(deserialize_from="VpcId")
    state = ModelType(State, deserialize_from="State")
    type = StringType(deserialize_from="Type", choices=("application", "network"))
    availability_zones = ListType(ModelType(LoadBalancerAvailabilityZones), deserialize_from="AvailabilityZones")
    security_group = ListType(StringType, deserialize_from="SecurityGroup")
    ip_address_type = StringType(deserialize_from="IpAddressType", choices=("ipv4", "dualstack"))
    account_id = StringType(default="")
    tags = ListType(ModelType(Tags))
    listeners = ListType(ModelType(Listener))
    attributes = ModelType(LoadBalancerAttributes)
    cloudwatch = ModelType(CloudWatchModel, serialize_when_none=False)

    def reference(self, region_code):
        return {
            "resource_id": self.load_balancer_arn,
            "external_link": f"https://console.aws.amazon.com/ec2/v2/home?region={region_code}#LoadBalancers:search={self.load_balancer_arn};sort=loadBalancerName"
        }

    def set_cloudwatch(self, region_code):
        namespace = ''
        _arn = arnparse(self.load_balancer_arn)
        dimensions = [CloudWatchDimensionModel({'Name': 'LoadBalancer', 'Value': _arn.resource})]

        if self.type == 'application':
            namespace = 'AWS/ApplicationELB'
        elif self.type == 'network':
            namespace = 'AWS/NetworkELB'

        return {
            "namespace": namespace,
            "dimensions": dimensions,
            "region_name": region_code
        }
