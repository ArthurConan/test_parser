import asyncio
import aiohttp
import aioredis


request_errors = (
            ConnectionRefusedError,
            ConnectionResetError,
            asyncio.TimeoutError,
            aiohttp.InvalidURL,
            aiohttp.client_exceptions.ClientConnectorError,
            aiohttp.client_exceptions.ClientResponseError,
            aiohttp.client_exceptions.ClientOSError,
            aiohttp.client_exceptions.ServerDisconnectedError,
            aiohttp.client_exceptions.ClientConnectionError,
            aiohttp.client_exceptions.ClientResponseError
)
redis_errors = (
    ConnectionRefusedError,
    ConnectionResetError,
    aioredis.RedisError,
    aioredis.ProtocolError,
    aioredis.ReplyError,
    aioredis.MaxClientsError,
    aioredis.AuthError,
    aioredis.PipelineError,
    aioredis.MultiExecError,
    aioredis.WatchVariableError,
    aioredis.ChannelClosedError,
    aioredis.ConnectionClosedError,
    aioredis.ConnectionForcedCloseError,
    aioredis.PoolClosedError,
    aioredis.MasterNotFoundError,
    aioredis.SlaveNotFoundError,
    aioredis.ReadOnlyError
)
