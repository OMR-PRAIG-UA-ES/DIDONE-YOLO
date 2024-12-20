# To train a YOLO model in DIDONE
## Gather data
Go to the `datasets/didone`folder and execute the following python command:

```python
python obtain_data.py
```
## Train the model
From the project folder execute:
```python
python train.py --model yolov11s.pt --data datasets/didone/data.yaml
```
The checkpoint from the previous step will be saved in `runs/detect/train/weights`. A folder will be created for each training instance, take that into consideration.

## Testing the model
From the project folder execute:
```python
python test.py --model PATH_TO_CHECKPOINT --data datasets/didone/data.yaml
```
Where `PATH_TO_CHECKPOINT`is the path to the checkpoint file of the trained YOLO model.
