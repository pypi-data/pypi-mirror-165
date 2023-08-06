import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-cloudwatch-alarm-chatbot",
    "version": "1.0.9",
    "description": "cdk-cloudwatch-alarm-chatbot",
    "license": "Apache-2.0",
    "url": "https://github.com/lvthillo/cdk-cloudwatch-alarm-chatbot.git",
    "long_description_content_type": "text/markdown",
    "author": "Lorenz Vanthillo<lorenz.vanthillo@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/lvthillo/cdk-cloudwatch-alarm-chatbot.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_cloudwatch_alarm_chatbot",
        "cdk_cloudwatch_alarm_chatbot._jsii"
    ],
    "package_data": {
        "cdk_cloudwatch_alarm_chatbot._jsii": [
            "cdk-cloudwatch-alarm-chatbot@1.0.9.jsii.tgz"
        ],
        "cdk_cloudwatch_alarm_chatbot": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "aws-cdk-lib>=2.1.0, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.66.0, <2.0.0",
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
        "Development Status :: 4 - Beta",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
