# -*- coding: utf-8 -*-
import json
import logging
import os
from typing import Any
import boto3

logger = logging.getLogger(__name__)


class Connection:
    """AWS Connection base class

    Raises:
        Exception: Aws credential not found exeception

    Returns:
        Object: connection class
    """

    active_sessions = {}

    def __init__(self, **kwargs) -> None:
        """Constructor class"""
        aws_credentials = kwargs.get("credentials", None)
        self.application_id = kwargs.get("application_id", None)
        if aws_credentials is None:
            aws_credentials = self._load_credentials()
        self.access_key = aws_credentials.get("ACCESS_KEY_ID")
        self.secret_access_key = aws_credentials.get("SECRET_ACCESS_KEY")
        self.session_token = aws_credentials.get("SESSION_TOKEN", "")
        self.region = aws_credentials.get("DEFAULT_REGION", "us-west-2")
        self._session = None

    @classmethod
    def _load_credentials(cls):
        svc_account_filename = "aws_role_account.json"
        aws_svc_account_path = os.getenv("AWS_SVC_ACCOUNT_PATH", "credentials")
        _aws_svc_account_file = os.path.join(aws_svc_account_path, svc_account_filename)
        try:
            with open(_aws_svc_account_file, encoding="utf-8") as file:
                aws_credentials = json.load(file)
        except Exception as ex:
            AWS_CRED_EXCEPTION = "Not found account service json for AWS - credentials/aws_role_account.json"
            logger.error(ex)
            raise Exception(AWS_CRED_EXCEPTION) from ex
        return aws_credentials

    def _get_access_kwargs(self):
        kwargs = {
            "aws_access_key_id": self.access_key,
            "aws_secret_access_key": self.secret_access_key,
        }
        if self.session_token:
            kwargs.update({"aws_session_token": self.session_token})

        if self.region:
            kwargs.update({"region_name": self.region})

        return kwargs

    @property
    def session(self):
        """Session property"""
        if not self._session:
            self._session = boto3.Session(**self._get_access_kwargs())
        return self._session

    def resource(self, service_name: str) -> Any:
        """Aws Resource get method"""
        return self.session.resource(service_name)

    def client(self, service_name: str, region_name=None) -> Any:
        """Aws client get method"""
        if region_name is not None:
            return self.session.client(service_name, region_name=region_name)
        return self.session.client(service_name)
