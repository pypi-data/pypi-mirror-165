'''
# Eventbridge SaaS Partner fURLs

[![View on Construct Hub](https://constructs.dev/badge?package=cdk-eventbridge-partner-processors)](https://constructs.dev/packages/cdk-eventbridge-partner-processors)

[![npm version](https://badge.fury.io/js/cdk-eventbridge-partner-processors.svg)](https://badge.fury.io/js/cdk-eventbridge-partner-processors)
[![PyPI version](https://badge.fury.io/py/a-bigelow.cdk-eventbridge-partner-processors.svg)](https://badge.fury.io/py/a-bigelow.cdk-eventbridge-partner-processors)
[![Go project version](https://badge.fury.io/go/github.com%2Fa-bigelow%2Fcdk-eventbridge-partner-processors-go.svg)](https://badge.fury.io/go/github.com%2Fa-bigelow%2Fcdk-eventbridge-partner-processors-go)

This CDK Construct library provides CDK constructs for the 1st-party (i.e. developed by AWS) lambda fURL webhook receivers for:

* GitHub
* Stripe
* Twilio

## Usage Examples (Simplified)

These examples are consistent for all 3 primary exported constructs of this library:

* `GitHubEventProcessor`
* `TwilioEventProcessor`
* `StripeEventProcessor`

> Note: Click on the above `View on Construct Hub` button to view auto-generated examples in Python/Go

### Typescript

```python
import { GitHubEventProcessor } from 'cdk-eventbridge-partner-processors';
import { Stack, StackProps } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { EventBus } from 'aws-cdk-lib/aws-events';
import { Secret } from 'aws-cdk-lib/aws-secretsmanager';

export class MyStackWithABetterName extends Stack {
    constructor(scope: Construct, id: string, props: StackProps) {
        super(scope, id, props);

        // This library has no opinion on how you reference your EventBus,
        // It just needs to fulfill the IEventBus protocol
        const myEventBus = new EventBus(this, 'TheBestBusEver', {
            eventBusName: 'TheGreatestBus'
        });

        // This library has no opinion on how you reference your secret,
        // It just needs to fulfill the ISecret protocol
        const mySecret = Secret.fromSecretNameV2(this, 'MyNuclearCodeSecret', '/home/recipes/icbm')

        // Function will automatically receive permission to:
        // 1. Post events to the given bus
        // 2. Read the given secret
        const githubEventProcessor = new GitHubEventProcessor(this, 'GitHubProcessor', {
            eventBus: myEventBus,
            webhookSecret: mySecret,
            lambdaInvocationAlarmThreshold: 2000,
        })

    }
}
```

### Disclaimer

> :warning: The Lambda Functions that handle the actual event processing in this Library are owned and maintained by Amazon Web Services. This CDK Construct library provides a thin deployment wrapper for these functions. Changes made to the S3 location of the functions will break this library. Until I have a way to deterministically track where these things are, please raise an **issue** if you have reason to believe that the functions have moved.

### AWS Documentation

See [here](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-saas-furls.html) for additional information.
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk.aws_events
import aws_cdk.aws_lambda
import aws_cdk.aws_secretsmanager
import constructs


@jsii.data_type(
    jsii_type="cdk-eventbridge-partner-processors.GitHubProps",
    jsii_struct_bases=[],
    name_mapping={
        "event_bus": "eventBus",
        "lambda_invocation_alarm_threshold": "lambdaInvocationAlarmThreshold",
        "webhook_secret": "webhookSecret",
    },
)
class GitHubProps:
    def __init__(
        self,
        *,
        event_bus: aws_cdk.aws_events.IEventBus,
        lambda_invocation_alarm_threshold: jsii.Number,
        webhook_secret: aws_cdk.aws_secretsmanager.ISecret,
    ) -> None:
        '''
        :param event_bus: Eventbus to send GitHub events to.
        :param lambda_invocation_alarm_threshold: Maximum number of concurrent invocations on the fURL function before triggering the alarm.
        :param webhook_secret: SM Secret containing the secret string used to validate webhook events.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(GitHubProps.__init__)
            check_type(argname="argument event_bus", value=event_bus, expected_type=type_hints["event_bus"])
            check_type(argname="argument lambda_invocation_alarm_threshold", value=lambda_invocation_alarm_threshold, expected_type=type_hints["lambda_invocation_alarm_threshold"])
            check_type(argname="argument webhook_secret", value=webhook_secret, expected_type=type_hints["webhook_secret"])
        self._values: typing.Dict[str, typing.Any] = {
            "event_bus": event_bus,
            "lambda_invocation_alarm_threshold": lambda_invocation_alarm_threshold,
            "webhook_secret": webhook_secret,
        }

    @builtins.property
    def event_bus(self) -> aws_cdk.aws_events.IEventBus:
        '''Eventbus to send GitHub events to.'''
        result = self._values.get("event_bus")
        assert result is not None, "Required property 'event_bus' is missing"
        return typing.cast(aws_cdk.aws_events.IEventBus, result)

    @builtins.property
    def lambda_invocation_alarm_threshold(self) -> jsii.Number:
        '''Maximum number of concurrent invocations on the fURL function before triggering the alarm.'''
        result = self._values.get("lambda_invocation_alarm_threshold")
        assert result is not None, "Required property 'lambda_invocation_alarm_threshold' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def webhook_secret(self) -> aws_cdk.aws_secretsmanager.ISecret:
        '''SM Secret containing the secret string used to validate webhook events.'''
        result = self._values.get("webhook_secret")
        assert result is not None, "Required property 'webhook_secret' is missing"
        return typing.cast(aws_cdk.aws_secretsmanager.ISecret, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GitHubProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class InvocationAlarm(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-eventbridge-partner-processors.InvocationAlarm",
):
    '''Cloudwatch Alarm used across this construct library.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        event_function: aws_cdk.aws_lambda.IFunction,
        threshold: jsii.Number,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param event_function: The function to monitor.
        :param threshold: Lambda Invocation threshold.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(InvocationAlarm.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = InvocationAlarmProps(
            event_function=event_function, threshold=threshold
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="cdk-eventbridge-partner-processors.InvocationAlarmProps",
    jsii_struct_bases=[],
    name_mapping={"event_function": "eventFunction", "threshold": "threshold"},
)
class InvocationAlarmProps:
    def __init__(
        self,
        *,
        event_function: aws_cdk.aws_lambda.IFunction,
        threshold: jsii.Number,
    ) -> None:
        '''
        :param event_function: The function to monitor.
        :param threshold: Lambda Invocation threshold.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(InvocationAlarmProps.__init__)
            check_type(argname="argument event_function", value=event_function, expected_type=type_hints["event_function"])
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
        self._values: typing.Dict[str, typing.Any] = {
            "event_function": event_function,
            "threshold": threshold,
        }

    @builtins.property
    def event_function(self) -> aws_cdk.aws_lambda.IFunction:
        '''The function to monitor.'''
        result = self._values.get("event_function")
        assert result is not None, "Required property 'event_function' is missing"
        return typing.cast(aws_cdk.aws_lambda.IFunction, result)

    @builtins.property
    def threshold(self) -> jsii.Number:
        '''Lambda Invocation threshold.'''
        result = self._values.get("threshold")
        assert result is not None, "Required property 'threshold' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InvocationAlarmProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-eventbridge-partner-processors.Partner")
class Partner(enum.Enum):
    '''Supported partners with fURL integrations.'''

    GITHUB = "GITHUB"
    STRIPE = "STRIPE"
    TWILIO = "TWILIO"


@jsii.data_type(
    jsii_type="cdk-eventbridge-partner-processors.PartnerFunctionProps",
    jsii_struct_bases=[],
    name_mapping={
        "eventbridge_partner": "eventbridgePartner",
        "event_bus": "eventBus",
        "lambda_invocation_alarm_threshold": "lambdaInvocationAlarmThreshold",
        "webhook_secret": "webhookSecret",
    },
)
class PartnerFunctionProps:
    def __init__(
        self,
        *,
        eventbridge_partner: Partner,
        event_bus: aws_cdk.aws_events.IEventBus,
        lambda_invocation_alarm_threshold: jsii.Number,
        webhook_secret: aws_cdk.aws_secretsmanager.ISecret,
    ) -> None:
        '''
        :param eventbridge_partner: The partner to create an events processor for.
        :param event_bus: Eventbus to send Partner events to.
        :param lambda_invocation_alarm_threshold: Maximum number of concurrent invocations on the fURL function before triggering the alarm.
        :param webhook_secret: SM Secret containing the secret string used to validate webhook events.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(PartnerFunctionProps.__init__)
            check_type(argname="argument eventbridge_partner", value=eventbridge_partner, expected_type=type_hints["eventbridge_partner"])
            check_type(argname="argument event_bus", value=event_bus, expected_type=type_hints["event_bus"])
            check_type(argname="argument lambda_invocation_alarm_threshold", value=lambda_invocation_alarm_threshold, expected_type=type_hints["lambda_invocation_alarm_threshold"])
            check_type(argname="argument webhook_secret", value=webhook_secret, expected_type=type_hints["webhook_secret"])
        self._values: typing.Dict[str, typing.Any] = {
            "eventbridge_partner": eventbridge_partner,
            "event_bus": event_bus,
            "lambda_invocation_alarm_threshold": lambda_invocation_alarm_threshold,
            "webhook_secret": webhook_secret,
        }

    @builtins.property
    def eventbridge_partner(self) -> Partner:
        '''The partner to create an events processor for.'''
        result = self._values.get("eventbridge_partner")
        assert result is not None, "Required property 'eventbridge_partner' is missing"
        return typing.cast(Partner, result)

    @builtins.property
    def event_bus(self) -> aws_cdk.aws_events.IEventBus:
        '''Eventbus to send Partner events to.'''
        result = self._values.get("event_bus")
        assert result is not None, "Required property 'event_bus' is missing"
        return typing.cast(aws_cdk.aws_events.IEventBus, result)

    @builtins.property
    def lambda_invocation_alarm_threshold(self) -> jsii.Number:
        '''Maximum number of concurrent invocations on the fURL function before triggering the alarm.'''
        result = self._values.get("lambda_invocation_alarm_threshold")
        assert result is not None, "Required property 'lambda_invocation_alarm_threshold' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def webhook_secret(self) -> aws_cdk.aws_secretsmanager.ISecret:
        '''SM Secret containing the secret string used to validate webhook events.'''
        result = self._values.get("webhook_secret")
        assert result is not None, "Required property 'webhook_secret' is missing"
        return typing.cast(aws_cdk.aws_secretsmanager.ISecret, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PartnerFunctionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PartnerProcessor(
    constructs.Construct,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="cdk-eventbridge-partner-processors.PartnerProcessor",
):
    '''CDK wrapper for the GitHub Eventbridge processor.

    :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-saas-furls.html#furls-connection-github
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        eventbridge_partner: Partner,
        event_bus: aws_cdk.aws_events.IEventBus,
        lambda_invocation_alarm_threshold: jsii.Number,
        webhook_secret: aws_cdk.aws_secretsmanager.ISecret,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param eventbridge_partner: The partner to create an events processor for.
        :param event_bus: Eventbus to send Partner events to.
        :param lambda_invocation_alarm_threshold: Maximum number of concurrent invocations on the fURL function before triggering the alarm.
        :param webhook_secret: SM Secret containing the secret string used to validate webhook events.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(PartnerProcessor.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = PartnerFunctionProps(
            eventbridge_partner=eventbridge_partner,
            event_bus=event_bus,
            lambda_invocation_alarm_threshold=lambda_invocation_alarm_threshold,
            webhook_secret=webhook_secret,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="invocationAlarm")
    def invocation_alarm(self) -> InvocationAlarm:
        return typing.cast(InvocationAlarm, jsii.get(self, "invocationAlarm"))

    @invocation_alarm.setter
    def invocation_alarm(self, value: InvocationAlarm) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(PartnerProcessor, "invocation_alarm").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "invocationAlarm", value)

    @builtins.property
    @jsii.member(jsii_name="partnerEventsFunction")
    def partner_events_function(self) -> aws_cdk.aws_lambda.Function:
        return typing.cast(aws_cdk.aws_lambda.Function, jsii.get(self, "partnerEventsFunction"))

    @partner_events_function.setter
    def partner_events_function(self, value: aws_cdk.aws_lambda.Function) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(PartnerProcessor, "partner_events_function").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "partnerEventsFunction", value)


class _PartnerProcessorProxy(PartnerProcessor):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, PartnerProcessor).__jsii_proxy_class__ = lambda : _PartnerProcessorProxy


class StripeEventProcessor(
    PartnerProcessor,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-eventbridge-partner-processors.StripeEventProcessor",
):
    '''CDK wrapper for the GitHub Eventbridge processor.

    :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-saas-furls.html#furls-connection-github
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        event_bus: aws_cdk.aws_events.IEventBus,
        lambda_invocation_alarm_threshold: jsii.Number,
        webhook_secret: aws_cdk.aws_secretsmanager.ISecret,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param event_bus: Eventbus to send GitHub events to.
        :param lambda_invocation_alarm_threshold: Maximum number of concurrent invocations on the fURL function before triggering the alarm.
        :param webhook_secret: SM Secret containing the secret string used to validate webhook events.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(StripeEventProcessor.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = StripeProps(
            event_bus=event_bus,
            lambda_invocation_alarm_threshold=lambda_invocation_alarm_threshold,
            webhook_secret=webhook_secret,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="cdk-eventbridge-partner-processors.StripeProps",
    jsii_struct_bases=[],
    name_mapping={
        "event_bus": "eventBus",
        "lambda_invocation_alarm_threshold": "lambdaInvocationAlarmThreshold",
        "webhook_secret": "webhookSecret",
    },
)
class StripeProps:
    def __init__(
        self,
        *,
        event_bus: aws_cdk.aws_events.IEventBus,
        lambda_invocation_alarm_threshold: jsii.Number,
        webhook_secret: aws_cdk.aws_secretsmanager.ISecret,
    ) -> None:
        '''
        :param event_bus: Eventbus to send GitHub events to.
        :param lambda_invocation_alarm_threshold: Maximum number of concurrent invocations on the fURL function before triggering the alarm.
        :param webhook_secret: SM Secret containing the secret string used to validate webhook events.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(StripeProps.__init__)
            check_type(argname="argument event_bus", value=event_bus, expected_type=type_hints["event_bus"])
            check_type(argname="argument lambda_invocation_alarm_threshold", value=lambda_invocation_alarm_threshold, expected_type=type_hints["lambda_invocation_alarm_threshold"])
            check_type(argname="argument webhook_secret", value=webhook_secret, expected_type=type_hints["webhook_secret"])
        self._values: typing.Dict[str, typing.Any] = {
            "event_bus": event_bus,
            "lambda_invocation_alarm_threshold": lambda_invocation_alarm_threshold,
            "webhook_secret": webhook_secret,
        }

    @builtins.property
    def event_bus(self) -> aws_cdk.aws_events.IEventBus:
        '''Eventbus to send GitHub events to.'''
        result = self._values.get("event_bus")
        assert result is not None, "Required property 'event_bus' is missing"
        return typing.cast(aws_cdk.aws_events.IEventBus, result)

    @builtins.property
    def lambda_invocation_alarm_threshold(self) -> jsii.Number:
        '''Maximum number of concurrent invocations on the fURL function before triggering the alarm.'''
        result = self._values.get("lambda_invocation_alarm_threshold")
        assert result is not None, "Required property 'lambda_invocation_alarm_threshold' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def webhook_secret(self) -> aws_cdk.aws_secretsmanager.ISecret:
        '''SM Secret containing the secret string used to validate webhook events.'''
        result = self._values.get("webhook_secret")
        assert result is not None, "Required property 'webhook_secret' is missing"
        return typing.cast(aws_cdk.aws_secretsmanager.ISecret, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StripeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TwilioEventProcessor(
    PartnerProcessor,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-eventbridge-partner-processors.TwilioEventProcessor",
):
    '''CDK wrapper for the GitHub Eventbridge processor.

    :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-saas-furls.html#furls-connection-github
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        event_bus: aws_cdk.aws_events.IEventBus,
        lambda_invocation_alarm_threshold: jsii.Number,
        webhook_secret: aws_cdk.aws_secretsmanager.ISecret,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param event_bus: Eventbus to send GitHub events to.
        :param lambda_invocation_alarm_threshold: Maximum number of concurrent invocations on the fURL function before triggering the alarm.
        :param webhook_secret: SM Secret containing the secret string used to validate webhook events.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TwilioEventProcessor.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = TwilioProps(
            event_bus=event_bus,
            lambda_invocation_alarm_threshold=lambda_invocation_alarm_threshold,
            webhook_secret=webhook_secret,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="cdk-eventbridge-partner-processors.TwilioProps",
    jsii_struct_bases=[],
    name_mapping={
        "event_bus": "eventBus",
        "lambda_invocation_alarm_threshold": "lambdaInvocationAlarmThreshold",
        "webhook_secret": "webhookSecret",
    },
)
class TwilioProps:
    def __init__(
        self,
        *,
        event_bus: aws_cdk.aws_events.IEventBus,
        lambda_invocation_alarm_threshold: jsii.Number,
        webhook_secret: aws_cdk.aws_secretsmanager.ISecret,
    ) -> None:
        '''
        :param event_bus: Eventbus to send GitHub events to.
        :param lambda_invocation_alarm_threshold: Maximum number of concurrent invocations on the fURL function before triggering the alarm.
        :param webhook_secret: SM Secret containing the secret string used to validate webhook events.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(TwilioProps.__init__)
            check_type(argname="argument event_bus", value=event_bus, expected_type=type_hints["event_bus"])
            check_type(argname="argument lambda_invocation_alarm_threshold", value=lambda_invocation_alarm_threshold, expected_type=type_hints["lambda_invocation_alarm_threshold"])
            check_type(argname="argument webhook_secret", value=webhook_secret, expected_type=type_hints["webhook_secret"])
        self._values: typing.Dict[str, typing.Any] = {
            "event_bus": event_bus,
            "lambda_invocation_alarm_threshold": lambda_invocation_alarm_threshold,
            "webhook_secret": webhook_secret,
        }

    @builtins.property
    def event_bus(self) -> aws_cdk.aws_events.IEventBus:
        '''Eventbus to send GitHub events to.'''
        result = self._values.get("event_bus")
        assert result is not None, "Required property 'event_bus' is missing"
        return typing.cast(aws_cdk.aws_events.IEventBus, result)

    @builtins.property
    def lambda_invocation_alarm_threshold(self) -> jsii.Number:
        '''Maximum number of concurrent invocations on the fURL function before triggering the alarm.'''
        result = self._values.get("lambda_invocation_alarm_threshold")
        assert result is not None, "Required property 'lambda_invocation_alarm_threshold' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def webhook_secret(self) -> aws_cdk.aws_secretsmanager.ISecret:
        '''SM Secret containing the secret string used to validate webhook events.'''
        result = self._values.get("webhook_secret")
        assert result is not None, "Required property 'webhook_secret' is missing"
        return typing.cast(aws_cdk.aws_secretsmanager.ISecret, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TwilioProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GitHubEventProcessor(
    PartnerProcessor,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-eventbridge-partner-processors.GitHubEventProcessor",
):
    '''CDK wrapper for the GitHub Eventbridge processor.

    :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-saas-furls.html#furls-connection-github
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        event_bus: aws_cdk.aws_events.IEventBus,
        lambda_invocation_alarm_threshold: jsii.Number,
        webhook_secret: aws_cdk.aws_secretsmanager.ISecret,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param event_bus: Eventbus to send GitHub events to.
        :param lambda_invocation_alarm_threshold: Maximum number of concurrent invocations on the fURL function before triggering the alarm.
        :param webhook_secret: SM Secret containing the secret string used to validate webhook events.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(GitHubEventProcessor.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = GitHubProps(
            event_bus=event_bus,
            lambda_invocation_alarm_threshold=lambda_invocation_alarm_threshold,
            webhook_secret=webhook_secret,
        )

        jsii.create(self.__class__, self, [scope, id, props])


__all__ = [
    "GitHubEventProcessor",
    "GitHubProps",
    "InvocationAlarm",
    "InvocationAlarmProps",
    "Partner",
    "PartnerFunctionProps",
    "PartnerProcessor",
    "StripeEventProcessor",
    "StripeProps",
    "TwilioEventProcessor",
    "TwilioProps",
]

publication.publish()
