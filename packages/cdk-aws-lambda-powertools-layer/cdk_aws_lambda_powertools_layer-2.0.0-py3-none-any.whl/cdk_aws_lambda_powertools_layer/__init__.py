'''
# AWS Lambda powertools layer

## Why this project exists

This is a custom construct that will create AWS Lambda Layer with AWS Powertools for Python or NodeJS library. There are different
ways how to create a layer and when working with CDK you need to install the library, create a zip file and wire it
correctly. With this construct you don't have to care about packaging and dependency management, create a construct
and add it to your function. The construct is an extension of the
existing [`LayerVersion`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_lambda.LayerVersion.html) construct
from the CDK library, so you have access to all fields and methods.

See the [API](API.md) for details.

```python
import { LambdaPowertoolsLayer } from 'cdk-aws=lambda-powertools-python-layer';

const powertoolsLayer = new LambdaPowertoolsLayer(this, 'TestLayer');
```

Python

```python
from cdk_aws_lambda_powertools_layer import LambdaPowertoolsLayer

powertoolsLayer = LambdaPowertoolsLayer(self, 'PowertoolsLayer')
```

The layer will be created during the CDK `synth` step and thus requires Docker.

## Install

TypeSript/JavaScript:

```shell
npm i cdk-aws-lambda-powertools-layer
```

Python:

```shell
pip install cdk-aws-lambda-powertools-layer
```

## Usage

### Python

A single line will create a layer with powertools for python:

```python
from cdk_aws_lambda_powertools_layer import LambdaPowertoolsLayer

powertoolsLayer = LambdaPowertoolsLayer(self, 'PowertoolsLayer')
```

You can then add the layer to your funciton:

```python
from aws_cdk import aws_lambda

aws_lambda.Function(self, 'LambdaFunction',
                            code=aws_lambda.Code.from_asset('function'),
                            handler='app.handler',
                            runtime=aws_lambda.Runtime.PYTHON_3_9,
                            layers=[powertoolsLayer])
```

You can specify the powertools version by passing the optional `version` paramter, otherwise the construct will take the
latest version from pypi repository.

```python
LambdaPowertoolsLayer(self, 'PowertoolsLayer', version='1.24.0')
```

Additionally, powertools have extras depenedncies such as
Pydantic, [documented here](https://awslabs.github.io/aws-lambda-powertools-python/latest/#lambda-layer). This is not
included by default, and you have to set this option in the construct definition if you need it:

```python
LambdaPowertoolsLayer(self, 'PowertoolsLayer', include_extras=True)
```

Full example:

```python
from aws_cdk import Stack, aws_lambda
from cdk_aws_lambda_powertools_layer import LambdaPowertoolsLayer
from constructs import Construct


class LayerTestStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        powertoolsLayer = LambdaPowertoolsLayer(
            self, 'PowertoolsLayer', include_extras=True, version='1.24.0')

        aws_lambda.Function(self, 'LambdaFunction',
                            code=aws_lambda.Code.from_asset('function'),
                            handler='app.handler',
                            runtime=aws_lambda.Runtime.PYTHON_3_9,
                            layers=[powertoolsLayer])

```

### TypeScript

Full example for TypeScript:

```python
import { Stack, StackProps } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { LambdaPowertoolsLayer } from 'cdk-aws-lambda-powertools-layer';
import { Code, Function, Runtime } from 'aws-cdk-lib/aws-lambda';
import * as path from 'path';

export class CdkPowertoolsExampleStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    const powertoolsLayer = new LambdaPowertoolsLayer(this, 'TestLayer', {
      version: '1.22.0',
      includeExtras: true
    });

    new Function(this, 'LambdaFunction', {
      code: Code.fromAsset(path.join('./function')),
      handler: 'app.handler',
      runtime: Runtime.PYTHON_3_9,
      layers: [powertoolsLayer],
    });
  }
}
```
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

import aws_cdk.aws_lambda
import constructs


class LambdaPowertoolsLayer(
    aws_cdk.aws_lambda.LayerVersion,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-aws-lambda-powertools-layer.LambdaPowertoolsLayer",
):
    '''Defines a new Lambda Layer with Powertools for python library.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        include_extras: typing.Optional[builtins.bool] = None,
        layer_version_name: typing.Optional[builtins.str] = None,
        runtime_family: typing.Optional[aws_cdk.aws_lambda.RuntimeFamily] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param include_extras: A flag for the pydantic extras dependency, used for parsing. This will increase the size of the layer significantly. If you don't use parsing, ignore it.
        :param layer_version_name: the name of the layer, will be randomised if empty.
        :param runtime_family: the runtime of the layer.
        :param version: The powertools package version from pypi repository.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(LambdaPowertoolsLayer.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = PowertoolsLayerProps(
            include_extras=include_extras,
            layer_version_name=layer_version_name,
            runtime_family=runtime_family,
            version=version,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="constructBuildArgs")
    @builtins.classmethod
    def construct_build_args(
        cls,
        runtime_family: aws_cdk.aws_lambda.RuntimeFamily,
        include_extras: typing.Optional[builtins.bool] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> builtins.str:
        '''creates build argument for the Dockerfile.

        There are multiple combinations between version and extras package that results in different suffix for the installation.
        With and without version, with and without extras flag.
        We construct one suffix here because it is easier to do in code than inside the Dockerfile with bash commands.
        For example, if we set extras=true and version=1.22.0 we get '[pydantic]==1.22.0'.

        :param runtime_family: -
        :param include_extras: -
        :param version: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(LambdaPowertoolsLayer.construct_build_args)
            check_type(argname="argument runtime_family", value=runtime_family, expected_type=type_hints["runtime_family"])
            check_type(argname="argument include_extras", value=include_extras, expected_type=type_hints["include_extras"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "constructBuildArgs", [runtime_family, include_extras, version]))


@jsii.data_type(
    jsii_type="cdk-aws-lambda-powertools-layer.PowertoolsLayerProps",
    jsii_struct_bases=[],
    name_mapping={
        "include_extras": "includeExtras",
        "layer_version_name": "layerVersionName",
        "runtime_family": "runtimeFamily",
        "version": "version",
    },
)
class PowertoolsLayerProps:
    def __init__(
        self,
        *,
        include_extras: typing.Optional[builtins.bool] = None,
        layer_version_name: typing.Optional[builtins.str] = None,
        runtime_family: typing.Optional[aws_cdk.aws_lambda.RuntimeFamily] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for Powertools layer for python.

        :param include_extras: A flag for the pydantic extras dependency, used for parsing. This will increase the size of the layer significantly. If you don't use parsing, ignore it.
        :param layer_version_name: the name of the layer, will be randomised if empty.
        :param runtime_family: the runtime of the layer.
        :param version: The powertools package version from pypi repository.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(PowertoolsLayerProps.__init__)
            check_type(argname="argument include_extras", value=include_extras, expected_type=type_hints["include_extras"])
            check_type(argname="argument layer_version_name", value=layer_version_name, expected_type=type_hints["layer_version_name"])
            check_type(argname="argument runtime_family", value=runtime_family, expected_type=type_hints["runtime_family"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[str, typing.Any] = {}
        if include_extras is not None:
            self._values["include_extras"] = include_extras
        if layer_version_name is not None:
            self._values["layer_version_name"] = layer_version_name
        if runtime_family is not None:
            self._values["runtime_family"] = runtime_family
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def include_extras(self) -> typing.Optional[builtins.bool]:
        '''A flag for the pydantic extras dependency, used for parsing.

        This will increase the size of the layer significantly. If you don't use parsing, ignore it.
        '''
        result = self._values.get("include_extras")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def layer_version_name(self) -> typing.Optional[builtins.str]:
        '''the name of the layer, will be randomised if empty.'''
        result = self._values.get("layer_version_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runtime_family(self) -> typing.Optional[aws_cdk.aws_lambda.RuntimeFamily]:
        '''the runtime of the layer.'''
        result = self._values.get("runtime_family")
        return typing.cast(typing.Optional[aws_cdk.aws_lambda.RuntimeFamily], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''The powertools package version from pypi repository.'''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PowertoolsLayerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "LambdaPowertoolsLayer",
    "PowertoolsLayerProps",
]

publication.publish()
