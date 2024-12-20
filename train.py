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
    parser.add_argument("--img_size", default=640, help="Image size.")
    parser.add_argument("--batch_size", default=16, help="Batch size.")
    parser.add_argument("--epochs", default=100, help="Number of epochs.")
    parser.add_argument("--resume", action="store_true", help="Resume training.")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    model = YOLO(args.model)
    model.train(
        data=args.data, imgsz=args.img_size, batch=args.batch_size, epochs=args.epochs, resume=args.resume
    )
