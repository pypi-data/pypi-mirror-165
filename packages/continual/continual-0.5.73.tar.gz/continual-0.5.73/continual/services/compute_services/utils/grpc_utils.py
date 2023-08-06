import logging

# get_context_sesssion gets the session token from the auth bearer
# currently this is used directly in the grpc servers to obtain a token to use
# for subsequent calls back to the management service.  We may want to move this
# or in addition, add it to an interceptor for better authorization checks.
def get_context_sesssion(context):
    try:
        metadict = dict(context.invocation_metadata())
        logging.info(
            "context.invocation_metadata(): {}".format(context.invocation_metadata())
        )
        auth = metadict["authorization"]
        logging.info("auth: {}".format(auth))
        token = auth.split(" ")[1]
        logging.info("token: {}".format(token))
        if token.startswith("sessions/"):
            return token
        logging.error(f"invalid token: {token}")
        raise Exception(f"invalid token: {token}")

    except Exception as e:
        logging.error(f"error getting session: {e}")
        raise Exception(f"error getting session: {e}")
