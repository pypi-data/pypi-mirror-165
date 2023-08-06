from continual.services.dataingest.server import DataIngestService
from continual.rpc.dataingest.v1 import dataingest_pb2_grpc
import grpc
import logging
from concurrent import futures
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

CONFIG_ENV = "CONFIG_ENV"
CONFIG_LOCAL_BASE = "CONFIG_LOCAL_BASE"


def start_health_server(health_path="/healthz", port=8000):
    logging.info(f"starting health server on port {port}")
    health_server = HealthHTTPRequestHandler(health_path)
    httpd = HTTPServer(("", port), health_server)
    httpd.serve_forever()


class HealthHTTPRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, health_path):
        self.health_path = health_path

    def __call__(self, *args, **kwargs):
        """Handle a request."""
        super().__init__(*args, **kwargs)

    def do_GET(self):
        # currently this health check does not validate anything other than it has been called after
        # the grpc server has started, allowing kubernetes to wait until this has occured.
        # currently the grpc server does no startup tasks, if some are added, this can be modified
        # to wait and check for success
        logging.info(f"health_path: {self.health_path} - process get: {self.path}")
        if self.path == self.health_path:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'"health": "ok"')
        else:
            self.send_response(503)
            self.end_headers()
            self.wfile.write(b'"health": "invalid path"')


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    dataingest_pb2_grpc.add_DataIngestAPIServicer_to_server(DataIngestService(), server)
    server.add_insecure_port("[::]:3000")
    logging.info("server starting")
    server.start()

    # Start health server
    port = 5011
    health_daemon = threading.Thread(
        name="health_daemon_server", target=start_health_server, args=("/healthz", port)
    )
    health_daemon.setDaemon(
        True
    )  # Set as a daemon so it will be killed once the main thread is dead.
    health_daemon.start()

    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # for root, dirs, files in os.walk("/", topdown=False):
    #    for name in files:
    #        print(os.path.join(root, name))
    logging.info("starting service")
    serve()
