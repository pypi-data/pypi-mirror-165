import io

import zmq
import torch


class InferenceClient:
    """Client for running remote model inferences."""

    def __init__(self, router_address: str):
        """
        Args:
            router_address (str): Address to `InferenceServer` instance, e.g.
                'tcp://127.0.0.1:33333`.
        """
        self._router_address = router_address
        self._socket: zmq.Socket = None
        self._create_socket()

    def _create_socket(self):
        if self._socket is not None:
            self._socket.setsockopt(zmq.LINGER, 0)
            self._socket.close()
        self._socket = zmq.Context.instance().socket(zmq.REQ)
        self._socket.connect(self._router_address)

    def evaluate_model(self, data: torch.Tensor, attempts: int = 10) -> torch.Tensor:
        """Runs a remote inference.

        Args:
            data (torch.Tensor): State.
            attempts (int, optional): Number of attempts made before an exception is
                raised. Defaults to 5.

        Returns:
            torch.Tensor: Inference result.
        """
        device = data.device
        bytedata = io.BytesIO()
        torch.save(data, bytedata)
        self._socket.send(bytedata.getbuffer(), copy=False)
        if self._socket.poll(timeout=10000, flags=zmq.POLLIN) != zmq.POLLIN:
            if attempts == 1:
                raise RuntimeError("Remote model evaluation failed.")
            else:
                self._create_socket()
                return self.evaluate_model(data, attempts=attempts - 1)
        recvbytes = io.BytesIO(self._socket.recv(copy=False).buffer)
        return torch.load(recvbytes, map_location=device)
