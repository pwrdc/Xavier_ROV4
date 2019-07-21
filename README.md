# Xavier_ROV4
Brain of ROV4

## Downloading models
To download newest trained models you need to enter models folder and run
```bash
./download_models.sh
```
To setup all paths edit models.json file in models folder. Eg
```json
"path": {
    "path": "models/modelYOLO_path",
    "input_tensor": "input_1:0",
    "output_tensor": "conv2d_1/Sigmoid:0",
    "threshold": 0.5
}
```
Means that files for this neural networks alre supplied in models/modelYOLO_path folder, tensor in which image will be 