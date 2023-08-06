import aws_cdk
import constructs

from . import well_architected_construct


class WebApplicationFirewall(well_architected_construct.Construct):

    def __init__(
        self, scope: constructs.Construct, id: str,
        target_arn=None,
        error_topic=None,
        web_application_firewall_scope='REGIONAL',
        **kwargs
    ) -> None:
        '''NOTE: HTTP APIs are not supported yet'''
        super().__init__(
            scope, id,
            error_topic=error_topic,
            **kwargs
        )
        self.create_web_application_firewall_association(
            target_arn=target_arn,
            web_application_firewall=self.create_web_application_firewall(
                scope=web_application_firewall_scope,
                web_application_firewall_rules=self.web_application_firewall_rules(),
            ),
        )

    def web_application_firewall_rules(self):
        return [
            self.common_ruleset(1),
            self.anonymous_ip_rule(2),
            self.restricted_ip_list_rule(3),
            self.add_geoblock_rule(4),
        ]

    def create_visibility_configuration(self, metric_name):
        return aws_cdk.aws_wafv2.CfnWebACL.VisibilityConfigProperty(
            cloud_watch_metrics_enabled=True,
            metric_name=metric_name,
            sampled_requests_enabled=True
        )

    @staticmethod
    def create_managed_rule_group_statement(name=None, excluded_rules=None):
        return aws_cdk.aws_wafv2.CfnWebACL.StatementProperty(
            managed_rule_group_statement=aws_cdk.aws_wafv2.CfnWebACL.ManagedRuleGroupStatementProperty(
                name=name,
                vendor_name='AWS',
                excluded_rules=excluded_rules if excluded_rules else []
            )
        )

    def create_managed_rule(self, name=None, priority=None, excluded_rules=None):
        return aws_cdk.aws_wafv2.CfnWebACL.RuleProperty(
            name=name,
            priority=priority,
            override_action=aws_cdk.aws_wafv2.CfnWebACL.OverrideActionProperty(none={}),
            visibility_config=self.create_visibility_configuration(name),
            statement=self.create_managed_rule_group_statement(
                name=name,
                excluded_rules=excluded_rules
            ),
        )

    def common_ruleset(self, priority):
        return self.create_managed_rule(
            name='AWSManagedRulesCommonRuleSet',
            priority=priority,
            excluded_rules=[
                aws_cdk.aws_wafv2.CfnWebACL.ExcludedRuleProperty(
                    name='SizeRestrictions_BODY'
                )
            ],
        )

    def anonymous_ip_rule(self, priority):
        return self.create_managed_rule(
            name='AWSManagedRulesAnonymousIpList',
            priority=priority,
        )

    def restricted_ip_list_rule(self, priority):
        return self.create_managed_rule(
            name='AWSManagedRulesAmazonIpReputationList',
            priority=priority,
        )

    @staticmethod
    def country_codes():
        return ['NZ']

    def add_geoblock_rule(self, priority):
        return aws_cdk.aws_wafv2.CfnWebACL.RuleProperty(
            name='GeoBlockingRule',
            priority=priority,
            action=aws_cdk.aws_wafv2.CfnWebACL.RuleActionProperty(block={}),
            visibility_config=self.create_visibility_configuration('geoblock'),
            statement=aws_cdk.aws_wafv2.CfnWebACL.StatementProperty(
                geo_match_statement=aws_cdk.aws_wafv2.CfnWebACL.GeoMatchStatementProperty(
                    country_codes=self.country_codes(),
                )
            ),
        )

    def create_web_application_firewall(self, web_application_firewall_rules=None, scope=None):
        return aws_cdk.aws_wafv2.CfnWebACL(
            self, 'WebApplicationFirewall',
            default_action=aws_cdk.aws_wafv2.CfnWebACL.DefaultActionProperty(allow={}),
            scope=scope,
            visibility_config=self.create_visibility_configuration('webACL'),
            name='WebApplicationFirewall',
            rules=web_application_firewall_rules
        )

    def create_web_application_firewall_association(self, web_application_firewall=None, target_arn=None):
        return aws_cdk.aws_wafv2.CfnWebACLAssociation(
            self, 'WebApplicationFirewallAPIGatewayAssociation',
            web_acl_arn=web_application_firewall.attr_arn,
            resource_arn=target_arn
        )