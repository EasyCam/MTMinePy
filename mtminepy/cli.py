"""CLI entry point for MTMinePy."""
import argparse
import sys


def main():
    parser = argparse.ArgumentParser(
        prog='mtminepy',
        description='MTMinePy - Multilingual Text Mining Platform'
    )
    parser.add_argument(
        '--host', default='0.0.0.0',
        help='Host to bind to (default: 0.0.0.0)'
    )
    parser.add_argument(
        '--port', '-p', type=int, default=5000,
        help='Port to listen on (default: 5000)'
    )
    parser.add_argument(
        '--debug', action='store_true',
        help='Run in Flask debug mode (not for production)'
    )
    parser.add_argument(
        '--version', action='store_true',
        help='Show version and exit'
    )

    args = parser.parse_args()

    if args.version:
        from . import __version__
        print(f"mtminepy {__version__}")
        sys.exit(0)

    print("Starting MTMinePy initialization...")
    from .app import create_app

    app = create_app()

    if args.debug:
        print(f"MTMinePy is running in debug mode on http://{args.host}:{args.port}")
        app.run(host=args.host, port=args.port, debug=True)
    else:
        print(f"MTMinePy is running on http://{args.host}:{args.port}")
        try:
            from waitress import serve
            serve(app, host=args.host, port=args.port, threads=6)
        except ImportError:
            print("Waitress not installed, falling back to Flask dev server.")
            print("Install waitress for production use: pip install waitress")
            app.run(host=args.host, port=args.port)


if __name__ == '__main__':
    main()
