from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.file import File
from ...models.not_found_error import NotFoundError
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    file_id: str,
) -> Dict[str, Any]:
    url = "{}/files/{file_id}".format(client.base_url, file_id=file_id)

    headers: Dict[str, Any] = client.httpx_client.headers
    headers.update(client.get_headers())

    cookies: Dict[str, Any] = client.httpx_client.cookies
    cookies.update(client.get_cookies())

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[File, NotFoundError]]:
    if response.status_code == 200:
        response_200 = File.from_dict(response.json())

        return response_200
    if response.status_code == 404:
        response_404 = NotFoundError.from_dict(response.json())

        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[File, NotFoundError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    file_id: str,
) -> Response[Union[File, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        file_id=file_id,
    )

    response = client.httpx_client.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    file_id: str,
) -> Optional[Union[File, NotFoundError]]:
    """ Get a file """

    return sync_detailed(
        client=client,
        file_id=file_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    file_id: str,
) -> Response[Union[File, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        file_id=file_id,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    file_id: str,
) -> Optional[Union[File, NotFoundError]]:
    """ Get a file """

    return (
        await asyncio_detailed(
            client=client,
            file_id=file_id,
        )
    ).parsed
