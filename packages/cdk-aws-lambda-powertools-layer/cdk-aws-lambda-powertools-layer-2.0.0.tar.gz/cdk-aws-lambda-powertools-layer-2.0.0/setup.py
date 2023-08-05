import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-aws-lambda-powertools-layer",
    "version": "2.0.0",
    "description": "A lambda layer for AWS Powertools for python and typescript",
    "license": "MIT-0",
    "url": "https://github.com/awslabs/cdk-aws-lambda-powertools-layer.git",
    "long_description_content_type": "text/markdown",
    "author": "Amazon Web Services",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/awslabs/cdk-aws-lambda-powertools-layer.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_aws_lambda_powertools_layer",
        "cdk_aws_lambda_powertools_layer._jsii"
    ],
    "package_data": {
        "cdk_aws_lambda_powertools_layer._jsii": [
            "cdk-aws-lambda-powertools-layer@2.0.0.jsii.tgz"
        ],
        "cdk_aws_lambda_powertools_layer": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "aws-cdk-lib>=2.24.1, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.65.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard~=2.13.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
