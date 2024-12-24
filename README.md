<p align="center">
  <a href=""><img src="https://i.imgur.com/Iu7CvC1.png" alt="PRAIG-logo" width="100"></a>
</p>

<h1 align="center">Training a YOLO model for DIDONE</h1>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.10.0-orange" alt="Gitter">
  <img src="https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=flat&logo=PyTorch&logoColor=white" alt="PyTorch">
  <img src="https://img.shields.io/static/v1?label=License&message=MIT&color=blue" alt="License">
</p>

<p align="center">
  <a href="#about">About</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#acknowledgments">Acknowledgments</a>
</p>

## About

This repository focuses on Document Analysis as the first phase of Optical Music Recognition (OMR) for classical manuscripts, specifically leveraging the DIDONE dataset. The goal is to develop and train a YOLO model to accurately detect and classify structural elements within handwritten musical scores, laying the foundation for downstream transcription processes.

---

#### <ins>Why Focus on Document Analysis?</ins>

End-to-end transcription requires precise detection of musical components as input. By isolating the document analysis phase, this repository ensures the foundation for later processes is reliable and accurate. Separating concerns between layout detection and symbolic recognition improves performance and allows targeted optimizations for each phase.

This repository complements a separate project dedicated to end-to-end transcription, ensuring modularity and scalability for future extensions.

## How To Use

To run the code, you'll need to meet certain requirements which are specified in the [`Dockerfile`](Dockerfile). Alternatively, you can set up a virtual environment if preferred. Once you have prepared your environment (either a Docker container or a virtual environment), you are ready to begin. 

> [!IMPORTANT]
> If you are using MacOS it is recommendable to use a virtual environment rather than docker. There is some known issues between Docker and the Apple OS. If perhaps you still want to use docker, try to use [Colima](https://github.com/abiosoft/colima) as a Docker wrapper.

### Deploying with Docker

#### $${\color{lightblue} 1. \space Build \space the \space image}$$

The first step is to build the Docker image using the provided <ins>Dockerfile</ins>. This image contains all the necessary dependencies and configurations required to run the project.

```shell
docker build --tag yolo-classical .
```

Once the image is built, it can be used to create and run containers.

#### $${\color{lightblue} 2. \space Run \space a \space container}$$

Next, create a Docker container from the image built in the previous step. The container serves as an isolated runtime environment for the project.

```shell
docker run -itd --rm -v ./:/workspace --name yolo yolo-classical
```

> It is important to correctly mount the volume. It ensures that project data will be consistent between the host and the container.

#### $${\color{lightblue} 3. \space Attach \space to \space the \space container}$$

Finally, attach to the running container to execute commands or monitor its operation.

```shell
docker attach yolo
```

>  [!TIP]
>  To exit the container without stopping it, press `Ctrl + P` followed by `Ctrl + Q`. To reattach later, use the docker attach yolo-doc command.

### To train a YOLO model in DIDONE

#### $${\color{lightblue} 1. \space Gather \space the \space data}$$
DIDONE corpus is codified in the [MuRET](https://muret.iuii.ua.es/) format which is used internally to manage OMR data. This codified data can be located at `datasets/didone/files`. To parse the data to a trainable YOLO format, go to the `datasets/didone`folder and execute the following python command:

```python
python obtain_data.py
```

For future generations, if you already have the images downloaded you can add the `--only-dicts` option to only regenarate labels and dictionaries of the corpus.

> [!WARNING]
> Usually, you want to only perform this step once. <br />
> To train multiple checkpoints, gather data once and repeat step 2.

#### $${\color{lightblue} 2. \space Execute \space the \space training \space script}$$

From the project folder execute:
```python
python train.py --model yolov11s.pt --data datasets/didone/data.yaml
```

The checkpoint from the previous step will be saved in `runs/detect/train/weights`. A folder will be created for each training instance, take that into consideration. For simplicity, 

> [!TIP]
> Is recomendable to move the checkpoints to the `checkpoints`folder. This avoids loosing any checkpoints by overriding them and allows quicker access by terminal. Also, rename the file to a proper name as this will help to later on identify the checkpoint source. A good name could include the date of training and the model architecture. As an example `yolov11s_20241210` would be a YOLO v11 model trained with the `small`configuration trained the 10/12/2024.

---

### To test a YOLO model in DIDONE

> [!WARNING]
> We assume data is already available from step 1 of the training of the model. If not, repeat step 1 of the previous section before continuing.

From the project folder execute:
```shell
python test.py --model PATH_TO_CHECKPOINT --data datasets/didone/data.yaml
```

Where `PATH_TO_CHECKPOINT`is the path to the checkpoint file of the trained YOLO model.

## Acknowledgments

This code is part of REPERTORIUM project, funded by the European Union’s Horizon Europe programme under grant agreement No 101095065.
