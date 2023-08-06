import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "aws_prototyping_sdk.pipeline",
    "version": "0.8.3",
    "description": "@aws-prototyping-sdk/pipeline",
    "license": "Apache-2.0",
    "url": "https://github.com/aws/aws-prototyping-sdk",
    "long_description_content_type": "text/markdown",
    "author": "AWS APJ COPE<apj-cope@amazon.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/aws/aws-prototyping-sdk"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "aws_prototyping_sdk.pipeline",
        "aws_prototyping_sdk.pipeline._jsii"
    ],
    "package_data": {
        "aws_prototyping_sdk.pipeline._jsii": [
            "pipeline@0.8.3.jsii.tgz"
        ],
        "aws_prototyping_sdk.pipeline": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "aws-cdk-lib>=2.39.1, <3.0.0",
        "aws_prototyping_sdk.pdk_nag>=0.7.8, <0.8.0",
        "cdk-nag>=2.17.2, <3.0.0",
        "constructs>=10.1.92, <11.0.0",
        "jsii>=1.66.0, <2.0.0",
        "projen>=0.61.37, <0.62.0",
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
