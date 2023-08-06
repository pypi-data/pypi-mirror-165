# -*- coding: utf-8 -*-
"""AWS config parameters."""

RESOURCE_CONFIG = {
    "eks": ("get_cluster_details", "client"),
    "ec2": ("get_instance_details", "client"),
}


INSTANCE_TYPE_CONFIG = {
    "t2.nano": {"memory": 0.5, "cpu": 1},
    "t2.micro": {"memory": 1, "cpu": 1},
    "t2.small": {"memory": 2, "cpu": 1},
    "t2.medium": {"memory": 4, "cpu": 2},
    "t2.large": {"memory": 8, "cpu": 2},
    "t2.xlarge": {"memory": 16, "cpu": 4},
    "t2.2xlarge": {"memory": 32, "cpu": 8},
}


AWS_GROUPED_RESOURCE = {
    "Containers": ["cluster"],
    "Compute": [
        "instance",
        "lb",
        "snapshot",
        "policy",
        "disk",
        "eip",
        "kms",
        "apphosting",
        "functions",
        "ssm",
    ],
    "VPC": ["network"],
    "Database": ["sql", "no_sql", "dax"],
    "CloudTrail": ["trail", "logs_metrics"],
    "IAM": ["serviceAccount", "analyzer", "user_groups"],
    "Storage": ["storage", "filesystem", "s3control"],
    "SageMaker": ["sagemaker"],
    "Cloud Search": ["elasticsearch", "opensearch"],
    "Config": ["config_service"],
    "GuardDuty": ["guardduty"],
    "RedShift": ["redshift"],
    "CloudFront": ["cloudfront"],
    "Serverless": ["apigateway", "rest_api", "sqs", "docdb"],
    "Notifications": ["sns"],
    "CodeBuild": ["codebuild"],
    "Glue": ["glue"],
    "ACM": ["acm"],
    "SecurityHub": ["securityhub"],
}


class AWSConfig:

    filter_name_map = {
        "instance_id": "InstanceId",
    }
