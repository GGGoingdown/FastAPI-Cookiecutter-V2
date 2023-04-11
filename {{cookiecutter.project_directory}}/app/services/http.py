from loguru import logger
from aiohttp import ClientSession, ClientTimeout
from aiohttp_retry import RetryClient, ExponentialRetry
from dependency_injector import resources
from typing import Dict, Callable, Any, Tuple, Union


class BaseRequestClient:
    RAISE_STATUS = {500, 501, 502, 503, 504, 505, 506, 507, 508}

    @classmethod
    def show_request_info(
        cls, url: str, status_code: int, response: Union[str, Dict]
    ) -> None:
        logger.info(f"[{url}]::Status code: {status_code} - Response: {response}")


class AsyncRequestClient(BaseRequestClient):
    def __init__(self, request_client: RetryClient) -> None:
        self._request_client = request_client

        self._http_method: Dict = {
            "GET": self._request_client.get,
            "POST": self._request_client.post,
            "PATCH": self._request_client.patch,
            "DELETE": self._request_client.delete,
        }

    async def close(self):
        return await self._request_client.close()

    async def _request(
        self, method: Callable, url: str, **kwargs: Any
    ) -> Tuple[int, Dict]:
        async with method(url, **kwargs) as response:
            status_code = response.status
            if status_code in self.RAISE_STATUS:
                return status_code, {
                    "detail": f"request server crash. status code: {status_code}"
                }
            rsp_json = await response.json()
        self.show_request_info(url=url, status_code=status_code, response=rsp_json)
        return status_code, rsp_json

    async def get(self, url: str, **kwargs: Any) -> Tuple[int, Dict]:
        return await self._request(self._http_method["GET"], url=url, **kwargs)

    async def post(self, url: str, **kwargs: Any) -> Tuple[int, Dict]:
        return await self._request(self._http_method["POST"], url=url, **kwargs)

    async def patch(self, url: str, **kwargs: Any) -> Tuple[int, Dict]:
        return await self._request(self._http_method["PATCH"], url=url, **kwargs)

    async def delete(self, url: str, **kwargs: Any) -> Tuple[int, Dict]:
        return await self._request(self._http_method["DELETE"], url=url, **kwargs)


class AsyncRequestHandler(resources.AsyncResource):
    async def init(
        self, retry_attempts: int = 3, timeout: int = 10, raise_for_status: bool = False
    ) -> AsyncRequestClient:
        logger.info("--- AsyncRequestClient init ---")
        logger.info(f"retry_attempts: {retry_attempts} - timeout: {timeout}")
        timeout = ClientTimeout(total=timeout)
        client_session = ClientSession(timeout=timeout)
        retry_options = ExponentialRetry(
            attempts=retry_attempts, statuses=AsyncRequestClient.RAISE_STATUS
        )
        retry_client = RetryClient(
            raise_for_status=raise_for_status,
            retry_options=retry_options,
            client_session=client_session,
        )

        client = AsyncRequestClient(request_client=retry_client)

        return client

    async def shutdown(self, client: AsyncRequestClient) -> None:
        await client.close()
        logger.info("--- AsyncRequestClient shutdown ---")
