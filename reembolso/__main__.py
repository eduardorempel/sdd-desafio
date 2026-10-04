import argparse
import sys


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m reembolso",
        description="Motor de cálculo de reembolso de despesas corporativas.",
    )
    parser.parse_args(argv)
    return 0


if __name__ == "__main__":
    sys.exit(main())
