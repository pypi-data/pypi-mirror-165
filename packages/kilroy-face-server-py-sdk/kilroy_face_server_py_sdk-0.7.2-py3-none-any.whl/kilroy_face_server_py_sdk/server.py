import logging

from grpclib.events import RecvRequest
from grpclib.server import Server

from kilroy_face_server_py_sdk import Face
from kilroy_face_server_py_sdk.service import FaceService


class FaceServer:
    def __init__(
        self,
        face: Face,
        logger: logging.Logger = logging.getLogger(__name__),
    ) -> None:
        self._service = FaceService(face)
        self._logger = logger

    async def _on_request(self, event: RecvRequest) -> None:
        self._logger.debug(f'Handling "{event.method_name}"...')

    async def run(self, *args, **kwargs) -> None:
        server = Server([self._service])
        await server.start(*args, **kwargs)
        self._logger.info("Server started.")
        try:
            await server.wait_closed()
        finally:
            self._logger.info("Server stopped.")
