import json
import os
import yaml
import requests
from PIL import Image
from io import BytesIO
import numpy as np
import cv2
from tqdm import tqdm

os.makedirs("./images", exist_ok=True)
os.makedirs("./labels", exist_ok=True)


def load_img_from_url(url):
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    img_array = np.array(image)
    return img_array, image.width, image.height


def pascal2yolo(voc, img_width, img_height):
    x_min, y_min, x_max, y_max = voc
    x_center = (x_min + x_max) / 2.0 / img_width
    y_center = (y_min + y_max) / 2.0 / img_height
    width = (x_max - x_min) / img_width
    height = (y_max - y_min) / img_height
    return [x_center, y_center, width, height]


c2i = {}
files = os.listdir("./files")
partitions = {
    "train": files[: int(len(files) * 0.8)],
    "val": files[int(len(files) * 0.8) : int(len(files) * 0.9)],
    "test": files[int(len(files) * 0.9) :],
}

for partition, files in partitions.items():
    os.makedirs(f"./images/{partition}", exist_ok=True)
    os.makedirs(f"./labels/{partition}", exist_ok=True)
    for file in tqdm(files, desc=f"Processing {partition} partition"):
        path = os.path.join("./files", file)
        with open(path, "r") as f:
            data = json.load(f)

        for document in data["documents"]:
            for section in document["sections"]:
                for image in section["images"]:
                    for page in image["pages"]:
                        if len(page["regions"]) == 0:
                            continue
                        
                        page_data = []

                        img_array, img_width, img_height = load_img_from_url(image["url"])
                        identifier = (
                            document["name"].strip().replace(" ", "_")
                            + "_"
                            + str(image["id"])
                        )

                        cv2.imwrite(f"./images/{partition}/{identifier}.jpg", img_array)

                        if "page" not in c2i:
                            c2i["page"] = len(c2i)

                        page_bbox = [
                            page["bounding_box"].get(k)
                            for k in ("fromX", "fromY", "toX", "toY")
                        ]
                        page_yolo = pascal2yolo(page_bbox, img_width, img_height)
                        page_data.append(
                            " ".join([str(c2i["page"]), *map(str, page_yolo)])
                        )

                        for region in page["regions"]:
                            if "bounding_box" not in region:
                                continue

                            if region["type"] not in c2i:
                                c2i[region["type"]] = len(c2i)

                            region_bbox = [
                                region["bounding_box"].get(k)
                                for k in ("fromX", "fromY", "toX", "toY")
                            ]
                            region_yolo = pascal2yolo(
                                region_bbox, img_width, img_height
                            )
                            page_data.append(
                                " ".join(
                                    [str(c2i[region["type"]]), *map(str, region_yolo)]
                                )
                            )

                        with open(f"./labels/{partition}/{identifier}.txt", "w") as f:
                            f.write("\n".join(page_data))

with open("data.yaml", "w") as f:
    data = {
        "path": "didone",
        "train": "images/train",
        "val": "images/val",
        "test": "images/test",
        "names": {v: k for k, v in c2i.items()},
    }
    yaml.dump(data, f)
