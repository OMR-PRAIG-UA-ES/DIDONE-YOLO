from ultralytics import YOLO
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description="Train a YOLO model.")
    parser.add_argument("--data", required=True, help="Path to the data yaml.")
    parser.add_argument(
        "--model",
        default="yolo11s.pt",
        help="Path to the model checkpoint. If not a ultralytics model, must be a path to a .pt file.",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    model = YOLO(args.model)
    metrics = model.val(data=args.data, split="test", plots=True)
