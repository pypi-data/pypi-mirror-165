from continual.services.dataingest.server import DataIngestService
from continual.rpc.dataingest.v1 import dataingest_pb2_grpc
import grpc
import logging
from concurrent import futures

CONFIG_ENV = "CONFIG_ENV"
CONFIG_LOCAL_BASE = "CONFIG_LOCAL_BASE"


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    dataingest_pb2_grpc.add_DataIngestAPIServicer_to_server(DataIngestService(), server)
    server.add_insecure_port("[::]:3000")
    logging.info("server starting")
    server.start()
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
