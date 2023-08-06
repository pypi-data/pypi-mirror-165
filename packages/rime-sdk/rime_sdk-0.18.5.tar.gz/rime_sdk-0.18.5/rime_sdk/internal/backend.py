"""Library for connecting to RIME backend services."""

import logging
from typing import Any, Callable, Dict, Generic, Optional, TypeVar

import grpc
import importlib_metadata

from rime_sdk.internal.client_interceptor import (
    AddMetadataUnaryStreamClientInterceptor,
    AddMetadataUnaryUnaryClientInterceptor,
)
from rime_sdk.internal.grpc_error_handler import GRPCErrorHandler
from rime_sdk.protos.data_collector.data_collector_pb2_grpc import DataCollectorStub
from rime_sdk.protos.feature_flag.feature_flag_pb2_grpc import FeatureFlagStub
from rime_sdk.protos.file_upload.file_upload_pb2_grpc import FileUploadStub
from rime_sdk.protos.firewall.firewall_pb2_grpc import FirewallServiceStub
from rime_sdk.protos.image_registry.image_registry_pb2_grpc import ImageRegistryStub
from rime_sdk.protos.jobs.jobs_pb2_grpc import JobReaderStub
from rime_sdk.protos.model_testing.model_testing_pb2_grpc import ModelTestingStub
from rime_sdk.protos.notification.notification_pb2_grpc import NotificationSettingStub
from rime_sdk.protos.project.project_pb2_grpc import ProjectManagerStub
from rime_sdk.protos.rime_info.rime_info_pb2 import GetRIMEInfoRequest
from rime_sdk.protos.rime_info.rime_info_pb2_grpc import RIMEInfoStub
from rime_sdk.protos.test_run_results.test_run_results_pb2_grpc import ResultsReaderStub
from rime_sdk.protos.test_run_tracker.test_run_tracker_pb2_grpc import (
    TestRunTrackerStub,
)

logger = logging.getLogger()

# Generic type representing a client stub for a gRPC server.
C = TypeVar("C")


# GrpcApiKeyAuth is an AuthMetadataPlugin to add api key in header on all calls
class GrpcApiKeyAuth(grpc.AuthMetadataPlugin):
    """Auth plugin to add 'rime-api-key' header to grpc calls."""

    def __init__(self, api_key: str) -> None:
        """Create an Auth plugin to add 'rime-api-key' header to grpc calls.

        Args:
            api_key: str
                Valid RIME Api Key to add to requests
        """
        self._api_key = api_key

    def __call__(self, context: Any, callback: Callable) -> None:
        """Add rime-api-key to grpc metadata when called."""
        callback((("rime-api-key", self._api_key),), None)


class RIMEConnection(Generic[C]):
    """A connection to a backend client of type C."""

    def __init__(
        self,
        create_backend_fn: Callable[..., C],
        addr: str,
        api_key: str,
        channel_timeout: float = 5.0,
        disable_tls: bool = False,
        ssl_config: Optional[Dict[str, str]] = None,
    ) -> None:
        """Create a new connection for a RIME backend.

        Args:
            create_backend_fn: Callable[..., C]
                Function to create a backend of type C from the channel acquired for
                this connection.
            addr: str
                The address of the backend server to create a channel to.
            api_key: str
                Api Key to validate RIME grpc requests with.
            channel_timeout: float
                The timeout in seconds for waiting for the given channel.
            disable_tls: bool
                Whether to disable tls when connecting to the backend.
            ssl_config: dict(str)
                SSL config to be passed to grpc.ssl_channel_credentials. Documentation
                can be found here: https://grpc.github.io/grpc/python/_modules/grpc.html#ssl_channel_credentials
        """
        self._create_backend_fn = create_backend_fn
        self._api_key = api_key
        self._addr = addr
        self._channel_timeout = channel_timeout
        self._channel: Optional[grpc.Channel] = None
        self._disable_tls = disable_tls
        self._ssl_config = ssl_config if ssl_config is not None else {}

    def __enter__(self) -> C:
        """Acquires the channel created in the with-context."""
        self._channel = self._build_and_validate_channel(
            self._addr, self._channel_timeout
        )
        return self._create_backend_fn(self._channel)

    def __exit__(self, exc_type: Any, exc_value: Any, exc_traceback: Any) -> None:
        """Frees the channel created in the with-context.

        Args:
            exc_type: Any
                The type of the exception (None if no exception occurred).
            exc_value: Any
                The value of the exception (None if no exception occurred).
            exc_traceback: Any
                The traceback of the exception (None if no exception occurred).
        """
        if self._channel:
            self._channel.close()

    def _build_and_validate_channel(self, addr: str, timeout: float,) -> grpc.Channel:
        """Build and validate a secure gRPC channel at `addr`.

        Args:
            addr: str
                The address of the RIME gRPC service.
            timeout: float
                The amount of time in seconds to wait for the channel to become ready.

        Raises:
            ValueError
                If a connection cannot be made to a backend service within `timeout`.
        """

        try:
            # create credentials
            if self._disable_tls:
                channel = grpc.insecure_channel(addr)
            else:
                credentials = grpc.composite_channel_credentials(
                    self._get_ssl_channel_credentials(),
                    grpc.metadata_call_credentials(GrpcApiKeyAuth(self._api_key)),
                )
                channel = grpc.secure_channel(addr, credentials)

            channel = grpc.intercept_channel(
                channel,
                AddMetadataUnaryUnaryClientInterceptor(),
                AddMetadataUnaryStreamClientInterceptor(),
            )
            grpc.channel_ready_future(channel).result(timeout=timeout)
            return channel
        except grpc.FutureTimeoutError:
            raise ValueError(
                f"Could not connect to server at address `{addr}`. "
                "Please confirm the URL is correct and check your network connection."
            ) from None

    def _get_ssl_channel_credentials(self) -> grpc.ChannelCredentials:
        """Fetch channel credentials for an SSL channel."""
        return grpc.ssl_channel_credentials(**self._ssl_config)


class RIMEBackend:
    """An abstraction for connecting to RIME's backend services."""

    GRPCErrorHandler = GRPCErrorHandler

    def __init__(
        self,
        domain: str,
        api_key: str = "",
        channel_timeout: float = 5.0,
        disable_tls: bool = False,
        ssl_config: Optional[Dict[str, str]] = None,
    ):
        """Create a new RIME backend.

        Args:
            domain: str
                The backend domain/address of the RIME service.
            api_key: str
                The api key providing authentication to RIME services
            channel_timeout: float
                The amount of time in seconds to wait for channels to become ready
                when opening connections to gRPC servers.
            disable_tls: bool
                Whether to disable tls when connecting to the backend.
            ssl_config: dict(str)
                SSL config to be passed to grpc.ssl_channel_credentials. Documentation
                can be found here: https://grpc.github.io/grpc/python/_modules/grpc.html#ssl_channel_credentials
        """
        self._channel_timeout = channel_timeout
        self._api_key = api_key
        self._disable_tls = disable_tls
        domain_split = domain.split(".", 1)
        self._ssl_config = ssl_config if ssl_config is not None else {}
        if domain_split[0][-4:] == "rime":
            base_domain = domain_split[1]
            domain = "rime-backend." + base_domain
        if domain.endswith("/"):
            domain = domain[:-1]
        self._backend_addr = self._get_backend_addr(domain, disable_tls)
        # Make sure this is last as it is dependent on connections being configured.
        self.customer_name = self._check_version()

    def _check_version(self) -> str:
        """Check current RIME version and return client name."""
        with self.get_rime_info_stub() as rime_info_client:
            with self.GRPCErrorHandler():
                rime_info_response = rime_info_client.GetRIMEInfo(GetRIMEInfoRequest())

        server_version = rime_info_response.cluster_info_version
        client_version = importlib_metadata.version("rime_sdk")
        if client_version != server_version:
            logger.warning(
                "Python SDK package and server are on different versions. "
                f"The Python SDK package is on version {client_version}, "
                f"while the server is on version {server_version}. "
                f"In order to make them be on the same version, please "
                f"install the correct version of the Python SDK package with "
                f"`pip install rime_sdk=={server_version}`"
            )
        return rime_info_response.customer_name

    def _get_backend_addr(self, domain: str, disable_tls: bool = False) -> str:
        """Construct an address to the all backend services from `domain`.

        Args:
            domain: str
                The backend domain/address of the RIME service.
            disable_tls: bool
                Whether to disable tls when connecting to the backend.
        """
        if disable_tls:
            return f"{domain}:80"
        return f"{domain}:443"

    def get_file_upload_stub(self) -> RIMEConnection[FileUploadStub]:
        """Return a file upload client."""
        # Note: the file upload service is currently co-located with the
        # data-manager until the file upload service is replaced.
        return RIMEConnection[FileUploadStub](
            FileUploadStub,
            self._backend_addr,
            self._api_key,
            channel_timeout=self._channel_timeout,
            disable_tls=self._disable_tls,
            ssl_config=self._ssl_config,
        )

    def get_image_registry_stub(self) -> RIMEConnection[ImageRegistryStub]:
        """Return an image registry client."""
        return RIMEConnection[ImageRegistryStub](
            ImageRegistryStub,
            self._backend_addr,
            self._api_key,
            channel_timeout=self._channel_timeout,
            disable_tls=self._disable_tls,
            ssl_config=self._ssl_config,
        )

    def get_model_testing_stub(self) -> RIMEConnection[ModelTestingStub]:
        """Return a model testing client."""
        return RIMEConnection[ModelTestingStub](
            ModelTestingStub,
            self._backend_addr,
            self._api_key,
            channel_timeout=self._channel_timeout,
            disable_tls=self._disable_tls,
            ssl_config=self._ssl_config,
        )

    def get_test_run_tracker_stub(self) -> RIMEConnection[TestRunTrackerStub]:
        """Return a test run tracker client."""
        return RIMEConnection[TestRunTrackerStub](
            TestRunTrackerStub,
            self._backend_addr,
            self._api_key,
            channel_timeout=self._channel_timeout,
            disable_tls=self._disable_tls,
            ssl_config=self._ssl_config,
        )

    def get_test_run_results_stub(self) -> RIMEConnection[ResultsReaderStub]:
        """Return a test run results reader client."""
        return RIMEConnection[ResultsReaderStub](
            ResultsReaderStub,
            self._backend_addr,
            self._api_key,
            channel_timeout=self._channel_timeout,
            disable_tls=self._disable_tls,
            ssl_config=self._ssl_config,
        )

    def get_firewall_stub(self) -> RIMEConnection[FirewallServiceStub]:
        """Return a firewall client."""
        return RIMEConnection[FirewallServiceStub](
            FirewallServiceStub,
            self._backend_addr,
            self._api_key,
            channel_timeout=self._channel_timeout,
            disable_tls=self._disable_tls,
            ssl_config=self._ssl_config,
        )

    def get_data_collector_stub(self) -> RIMEConnection[DataCollectorStub]:
        """Return a Data Collector client."""
        return RIMEConnection[DataCollectorStub](
            DataCollectorStub,
            self._backend_addr,
            self._api_key,
            channel_timeout=self._channel_timeout,
            disable_tls=self._disable_tls,
            ssl_config=self._ssl_config,
        )

    def get_project_manager_stub(self) -> RIMEConnection[ProjectManagerStub]:
        """Return a project management client."""
        return RIMEConnection[ProjectManagerStub](
            ProjectManagerStub,
            self._backend_addr,
            self._api_key,
            channel_timeout=self._channel_timeout,
            disable_tls=self._disable_tls,
            ssl_config=self._ssl_config,
        )

    def get_feature_flag_stub(self) -> RIMEConnection[FeatureFlagStub]:
        """Return a feature flag client."""
        return RIMEConnection[FeatureFlagStub](
            FeatureFlagStub,
            self._backend_addr,
            self._api_key,
            channel_timeout=self._channel_timeout,
            disable_tls=self._disable_tls,
            ssl_config=self._ssl_config,
        )

    def get_rime_info_stub(self) -> RIMEConnection[RIMEInfoStub]:
        """Return a rime info client."""
        return RIMEConnection[RIMEInfoStub](
            RIMEInfoStub,
            self._backend_addr,
            self._api_key,
            channel_timeout=self._channel_timeout,
            disable_tls=self._disable_tls,
            ssl_config=self._ssl_config,
        )

    def get_job_reader_stub(self) -> RIMEConnection[JobReaderStub]:
        """Return a job reader client."""
        return RIMEConnection[JobReaderStub](
            JobReaderStub,
            self._backend_addr,
            self._api_key,
            channel_timeout=self._channel_timeout,
            disable_tls=self._disable_tls,
            ssl_config=self._ssl_config,
        )

    def get_notification_settings_stub(self) -> RIMEConnection[NotificationSettingStub]:
        """Return a Notification setting client."""
        return RIMEConnection[NotificationSettingStub](
            NotificationSettingStub,
            self._backend_addr,
            self._api_key,
            channel_timeout=self._channel_timeout,
            disable_tls=self._disable_tls,
            ssl_config=self._ssl_config,
        )
