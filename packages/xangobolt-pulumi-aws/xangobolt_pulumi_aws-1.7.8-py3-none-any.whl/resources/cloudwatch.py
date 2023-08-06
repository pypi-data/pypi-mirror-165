from arpeggio.cleanpeg import NOT, prefix
from pulumi.resource import ResourceOptions
import pulumi_aws.cloudwatch as cw

def Event_Rule(stem, props, description=None, event_pattern=None , event_bus=None, is_enabled=None, schedule_expression=None, provider=None, parent=None, depends_on=None):
    event_rule = cw.EventRule(
        f'er-{stem}',
        name=f'er-{stem}',
        description=description,
        event_pattern=event_pattern,
        event_bus_name=event_bus,
        is_enabled=is_enabled,
        schedule_expression=schedule_expression,
        tags=props.base_tags,
        opts=ResourceOptions(provider=provider, parent=parent, depends_on=depends_on)
    )
    return event_rule

def Event_Target(stem, props, arn=None, rule=None , role_arn=None, provider=None, parent=None, depends_on=None):
    event_target = cw.EventTarget(
        f'et-{stem}',
        arn=arn,
        rule=rule,
        role_arn=role_arn,
        tags=props.base_tags,
        opts=ResourceOptions(provider=provider, parent=parent, depends_on=depends_on)
    )
    return event_target