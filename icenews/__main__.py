import argparse
import uvicorn


def main():
    argparser = argparse.ArgumentParser(
        description="Analyze Icelandic text with icenews"
    )

    argparser.add_argument(
        "-b", "--bind", type=str, default="127.0.0.1", help="Address to bind to"
    )
    argparser.add_argument(
        "-p", "--port", type=int, default=8000, help="Port number to use"
    )
    argparser.add_argument(
        "-d", "--debug", action="store_true", help="Start in debug mode"
    )

    args = argparser.parse_args()
    uvicorn.run(
        "icenews.server:app",
        host=args.bind,
        port=args.port,
        log_level="info",
        reload=args.debug,
    )


if __name__ == "__main__":
    main()
