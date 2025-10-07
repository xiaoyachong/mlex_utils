# test_utils.py
import os
from unittest.mock import MagicMock, patch

import pytest


# Common fixtures for MLflow testing
@pytest.fixture
def mock_mlflow_model_client():
    """Mock MlflowClient class"""
    with patch("mlflow.tracking.MlflowClient") as mock_client_class:
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        yield mock_client


@pytest.fixture
def mock_mlflow_algorithm_client():
    """Mock MlflowClient class for algorithm client"""
    with patch("mlflow.tracking.MlflowClient") as mock_client_class:
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        yield mock_client


@pytest.fixture
def mock_os_makedirs():
    """Mock os.makedirs to avoid file system errors"""
    with patch("os.makedirs") as mock_makedirs:
        yield mock_makedirs


@pytest.fixture
def mlflow_test_model_client(mock_mlflow_model_client, mock_os_makedirs):
    """Create a MLflowModelClient instance with mocked dependencies"""
    with patch("mlflow.set_tracking_uri"):  # Avoid actually setting tracking URI
        from mlex_utils.mlflow_utils.mlflow_model_client import MLflowModelClient

        client = MLflowModelClient(
            tracking_uri="http://mock-mlflow:5000",
            username="test-user",
            password="test-password",
            cache_dir="/tmp/test_mlflow_cache",
        )
        # Set the mocked client
        client.client = mock_mlflow_model_client
        return client


@pytest.fixture
def mlflow_test_algorithm_client(mock_mlflow_algorithm_client, mock_os_makedirs):
    """Create a MlflowAlgorithmClient instance with mocked dependencies"""
    with patch("mlflow.set_tracking_uri"):  # Avoid actually setting tracking URI
        from mlex_utils.mlflow_utils.mlflow_algorithm_client import MlflowAlgorithmClient

        client = MlflowAlgorithmClient(
            tracking_uri="http://mock-mlflow:5000",
            username="test-user",
            password="test-password",
            cache_dir="/tmp/test_mlflow_algorithm_cache",
        )
        # Set the mocked client
        client.client = mock_mlflow_algorithm_client
        return client