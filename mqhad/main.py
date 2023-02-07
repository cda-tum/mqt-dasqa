import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="mqhad cli")
    parser.add_argument(
        "--file-path", type=str, help="QASM 2.0 file path", required=True
    )

    args = parser.parse_args()
    print("#### Start generating")
    print("#### Generation ended")
