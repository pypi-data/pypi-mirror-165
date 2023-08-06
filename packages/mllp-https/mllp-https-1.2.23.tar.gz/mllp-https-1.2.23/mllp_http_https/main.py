import argparse
import logging
import urllib.parse
from .version import __version__


class ArgumentFormatter(
    argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter
):
    pass


def log_level(arg):
    if arg == "error":
        return logging.ERROR
    elif arg == "warn":
        return logging.WARNING
    elif arg == "info":
        return logging.INFO


def url_type(arg):
    return urllib.parse.urlparse(arg)


def http2mllp():
    parser = argparse.ArgumentParser(
        "http2mllp",
        description="""
            HTTP server that proxies an MLLP server.
            Expects an MLLP response message and uses it as the HTTP response.
        """,
        formatter_class=ArgumentFormatter,
    )
    parser.add_argument(
        "-H",
        "--host",
        default="0.0.0.0",
        help="HTTP host",
    )
    parser.add_argument(
        "-p",
        "--port",
        default=8000,
        type=int,
        help="HTTP port",
    )
    parser.add_argument(
        "--keep-alive",
        type=int,
        default=-1,
        help="keep-alive in milliseconds, or unlimited if -1.",
    )
    parser.add_argument(
        "--log-level",
        choices=("error", "warn", "info"),
        default="info",
    )
    parser.add_argument(
        "--mllp-keep-alive",
        type=int,
        default=-1,
        help="keep-alive in milliseconds, or unlimited if -1.",
    )
    parser.add_argument(
        "--mllp-max-messages",
        type=int,
        default=-1,
        help="maximum number of messages per connection, or unlimited if -1.",
    )
    parser.add_argument(
        "--mllp-release",
        default="1",
        choices=("1"),
        help="MLLP release version",
    )
    parser.add_argument(
        "--timeout",
        default=0,
        type=float,
        help="socket timeout, in milliseconds, or unlimited if 0.",
    )
    parser.add_argument(
        "--content-type",
        default="x-application/hl7-v2+er7",
        help="HTTP Content-Type header",
    )
    parser.add_argument(
        "-v", "--version", action="version", version="%(prog)s {}".format(__version__)
    )
    parser.add_argument(
        "mllp_url",
        #type=url_type,
        help="MLLP URL, Defaulf: hostname"
    )
    parser.add_argument(
        "--mllp_port",
        default=2575,
        type=int,
        help="MLLP PORT",
    )

    args = parser.parse_args()

    import mllp_http_https.http2mllp

    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] %(name)s %(message)s",
        level=log_level(args.log_level),
    )

    http_server_options = mllp_http_https.http2mllp.HttpServerOptions(
        timeout=args.timeout / 1000,
        content_type=args.content_type,
        keep_alive=args.keep_alive,
    )
    mllp_client_options = mllp_http_https.http2mllp.MllpClientOptions(
        keep_alive=args.mllp_keep_alive / 1000,
        max_messages=args.mllp_max_messages,
        timeout=args.timeout / 100,
    )

    try:
        mllp_http_https.http2mllp.serve(
            address=(
                args.host,
                args.port,
            ),
            options=http_server_options,
            mllp_address=(args.mllp_url, args.mllp_port),
            mllp_options=mllp_client_options,
        )
    except KeyboardInterrupt:
        pass


def mllp2http():
    parser = argparse.ArgumentParser(
        "mllp2http",
        description="MLLP server that proxies an HTTP server. Sends back the HTTP response.",
        formatter_class=ArgumentFormatter,
        epilog="""
environment variables:
    HTTP_AUTHORIZATION - HTTP Authorization header
    X-API-KEY - HTTP X-API-KEY header
        """,
    )
    parser.add_argument(
        "-H",
        "--host",
        default="0.0.0.0",
        help="MLLP host",
    )
    parser.add_argument(
        "-p",
        "--port",
        default=2575,
        type=int,
        help="MLLP port",
    )
    parser.add_argument(
        "--content-type",
        default="x-application/hl7-v2+er7",
        help="HTTP Content-Type header",
    )
    parser.add_argument(
        "--log-level",
        choices=("error", "warn", "info"),
        default="info",
    )
    parser.add_argument(
        "--mllp-release",
        default="1",
        choices=("1"),
        help="MLLP release version",
    )
    parser.add_argument(
        "--timeout",
        default=0,
        type=float,
        help="timeout in milliseconds",
    )
    parser.add_argument(
        "-v", "--version", action="version", version="%(prog)s {}".format(__version__)
    )
    parser.add_argument("http_url", help="HTTP URL", type=url_type)
    args = parser.parse_args()

    import mllp_http_https.mllp2http

    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] %(name)s %(message)s",
        level=log_level(args.log_level),
    )

    http_client_options = mllp_http_https.mllp2http.HttpClientOptions(
        content_type=args.content_type,
        timeout=args.timeout if args.timeout else None,
    )
    mllp_server_options = mllp_http_https.mllp2http.MllpServerOptions(
        timeout=args.timeout / 1000 if args.timeout else None
    )

    try:
        mllp_http_https.mllp2http.serve(
            address=(args.host, args.port),
            http_options=http_client_options,
            http_url=args.http_url,
            options=mllp_server_options,
        )
    except KeyboardInterrupt:
        pass


### Added features: MLLP to HTTPS and vice-versa
### By Tiago Rodrigues
### Sectra Iberia, Aug 2022

def mllp2https():
    parser = argparse.ArgumentParser(
        "mllp2https",
        description="MLLP server that proxies an HTTPS server. Sends back the HTTPS response.",
        formatter_class=ArgumentFormatter,
        epilog="""
environment variables:
    HTTP_AUTHORIZATION - HTTP Authorization header
    X-API-KEY - HTTP X-API-KEY header
        """,
    )
    parser.add_argument(
        "-H",
        "--host",
        default="0.0.0.0",
        help="MLLP host",
    )
    parser.add_argument(
        "-p",
        "--port",
        default=2575,
        type=int,
        help="MLLP port",
    )
    parser.add_argument(
        "--content-type",
        default="x-application/hl7-v2+er7",
        help="HTTPS Content-Type header",
    )
    parser.add_argument(
        "--log-level",
        choices=("error", "warn", "info"),
        default="info",
    )
    parser.add_argument(
        "--mllp-release",
        default="1",
        choices=("1"),
        help="MLLP release version",
    )
    parser.add_argument(
        "--timeout",
        default=0,
        type=float,
        help="timeout in milliseconds",
    )
    parser.add_argument(
        "--verify",
        choices=("False", "True"),
        default="True",
        type=str,
        help="Verify SSL certificate on server side. True as default",
    )
    parser.add_argument(
        "-v", "--version", action="version", version="%(prog)s {}".format(__version__)
    )
    parser.add_argument("https_url", help="HTTPS URL", type=url_type)
    args = parser.parse_args()

    import mllp_http_https.mllp2https

    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] %(name)s %(message)s",
        level=log_level(args.log_level),
    )

    https_client_options = mllp_http_https.mllp2https.HttpsClientOptions(
        content_type=args.content_type,
        timeout=args.timeout if args.timeout else None,
        verify=True if args.verify == "True" else False,
    )
    mllp_server_options = mllp_http_https.mllp2https.MllpServerOptions(
        timeout=args.timeout / 1000 if args.timeout else None
    )

    try:
        mllp_http_https.mllp2https.serve(
            address=(args.host, args.port),
            https_options=https_client_options,
            https_url=args.https_url,
            options=mllp_server_options,
        )
    except KeyboardInterrupt:
        pass


def https2mllp():
    parser = argparse.ArgumentParser(
        "https2mllp",
        description="""
            HTTPS server that proxies an MLLP server.
            Expects an MLLP response message and uses it as the HTTPS response.
        """,
        formatter_class=ArgumentFormatter,
    )
    parser.add_argument(
        "-H",
        "--host",
        default="0.0.0.0",
        help="HTTPS host",
    )
    parser.add_argument(
        "-p",
        "--port",
        default=8000,
        type=int,
        help="HTTPS port",
    )
    parser.add_argument(
        "--keep-alive",
        type=int,
        default=-1,
        help="keep-alive in milliseconds, or unlimited if -1.",
    )
    parser.add_argument(
        "--log-level",
        choices=("error", "warn", "info"),
        default="info",
    )
    parser.add_argument(
        "--mllp-keep-alive",
        type=int,
        #default=10 * 1000,
        default=-1,
        help="keep-alive in milliseconds, or unlimited if -1.",
    )
    parser.add_argument(
        "--mllp-max-messages",
        type=int,
        default=-1,
        help="maximum number of messages per connection, or unlimited if -1.",
    )
    parser.add_argument(
        "--mllp-release",
        default="1",
        choices=("1"),
        help="MLLP release version",
    )
    parser.add_argument(
        "--timeout",
        default=0,
        type=float,
        help="socket timeout, in milliseconds, or unlimited if 0.",
    )
    parser.add_argument(
        "--content-type",
        default="x-application/hl7-v2+er7",
        help="HTTPS Content-Type header",
    )
    parser.add_argument(
        "mllp_url",
        # type=url_type,
        help="MLLP URL, Defaulf: hostname"
    )
    parser.add_argument(
        "--mllp_port",
        default=2575,
        type=int,
        help="MLLP PORT",
    )
    parser.add_argument(
        "--certfile",
        default="C:/ssl/certfile.crt",
        type=str,
        help="Path for HTTPS Server's SSL/TLS Certificate. Default: C:/ssl/certfile.crt",
    )
    parser.add_argument(
        "--keyfile",
        default="C:/ssl/keyfile.key",
        type=str,
        help="Path for HTTPS Server's SSL/TLS Private Key. Default: C:/ssl/keyfile.key",
    )
    parser.add_argument(
        "-v", "--version", action="version", version="%(prog)s {}".format(__version__)
    )

    args = parser.parse_args()

    import mllp_http_https.https2mllp

    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] %(name)s %(message)s",
        level=log_level(args.log_level),
    )

    https_server_options = mllp_http_https.https2mllp.HttpsServerOptions(
        timeout=args.timeout / 1000,
        content_type=args.content_type,
        certfile=args.certfile,
        keyfile=args.keyfile,
        keep_alive=args.keep_alive,
    )
    mllp_client_options = mllp_http_https.https2mllp.MllpClientOptions(
        keep_alive=args.mllp_keep_alive / 1000,
        max_messages=args.mllp_max_messages,
        timeout=args.timeout / 100,
    )

    try:
        mllp_http_https.https2mllp.serve(
            address=(
                args.host,
                args.port,
            ),
            options=https_server_options,
            mllp_address=(args.mllp_url, args.mllp_port),
            mllp_options=mllp_client_options,
        )
    except KeyboardInterrupt:
        pass





# For debugging reasons
#https2mllp()