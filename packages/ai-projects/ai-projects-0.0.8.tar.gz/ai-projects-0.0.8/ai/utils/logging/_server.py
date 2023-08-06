import warnings
from typing import  Mapping, Optional
from multiprocessing import Process
from multiprocessing.connection import Connection, Pipe

import zmq
from torch.utils.tensorboard.writer import SummaryWriter

import ai.utils.logging as logging


def run(port: Optional[int], name: str,  conn: Connection, fields: Mapping[str, logging.field.Base]):
    writer = SummaryWriter(comment=name)

    for field in fields.values():
        field.writer = writer

    socket = zmq.Context.instance().socket(zmq.SUB)
    socket.subscribe("")
    if port is None:
        port = socket.bind_to_random_port(f"tcp://*")
    else:
        socket.bind(f"tcp://*:{port}")

    conn.send(port)
    conn.close()

    failed_keys = set()

    while True:
        if socket.poll(timeout=1000.0, flags=zmq.POLLIN) != zmq.POLLIN:
            continue
        field, value = socket.recv_pyobj()
        try:
            fields[field].log(value)
        except KeyError:
            if field not in failed_keys:
                warnings.warn(
                    f"Failed logging field '{field}'. Make sure these fields are "
                    "configured by your logging server."
                )
                failed_keys.add(field)


class Server:
    """Process handling a summary writer."""

    def __init__(self, *fields: logging.field.Base, name: str, port: int=None):
        """
        Args:
            fields (logging.field.Base): Logging fields.
            name (str): Name of the logger.
            port (int, optional): Port on which the server will listen for logging
                values. If `None`, then a random port is chosen.
        """
        self._fields = {field.name: field for field in fields}
        self._port = port
        self._name = name
        self._process: Process = None

    @property
    def port(self) -> int:
        """Port on which the server is running."""
        return self._port

    @property
    def started(self) -> bool:
        """Returns whether the server was started."""
        return self._process is not None

    def start(self) -> int:
        """Starts the logging server.

        Returns:
            int: The port on which the server started listening to.
        """
        a, b = Pipe(duplex=False)
        self._process = Process(target=run, args=(self._port, self._name, b, self._fields), daemon=True)
        self._process.start()
        for _ in range(15):
            if a.poll(timeout=1.0):
                break
        if not a.poll(timeout=0):
            raise RuntimeError(f"Failed starting logging server '{self._name}'.")
        self._port = a.recv()
        a.close()
        return self.port
