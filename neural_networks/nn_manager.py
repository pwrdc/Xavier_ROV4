from neural_networks.yolo_model_proxy import YoloModelProxy
from typing import Optional
from collections import namedtuple
import json
from utils.logging import Log, LogType
class _ActiveNetwork:
    def __init__(self, name: str, network: YoloModelProxy):
        self.name = name
        self.network = network
class _NNManagerClass:
    def __init__(self):
        self.active_network: Optional[_ActiveNetwork] = None
        self.secondary_network: Optional[_ActiveNetwork] = None

        with open("configs/models.json", "r") as f:
            self.config = json.load(f)

    def get_yolo_model(self, name) -> Optional[YoloModelProxy]:
        if self.active_network is not None:
            if self.active_network.name == name:
                return self.active_network.network

        if not name in self.config:
            Log(LogType.ERROR, f"Neural network named {name} not found!")
            exit(-1)

        config = self.config[name]

        if self.active_network is not None:
            self.active_network.network.release()

        if self.secondary_network is not None:
            self.secondary_network.network.release()
            self.secondary_network = None

        if not name in self.config:
            Log(LogType.ERROR, f"Neural network named {name} not found!")
            exit(-1)

        for param in ['path', 'threshold', 'input_tensor', 'output_tensor']:
            if param not in config:
                Log(LogType.ERROR, f"{param} value not found int models.json!")
                exit(-1)

        self.active_network = _ActiveNetwork(name,
                                             YoloModelProxy(model_path=config['path'],
                                                            threshold=config['threshold'],
                                                            input_tensor_name=config['input_tensor'],
                                                            output_tensor_name=config['output_tensor'],
                                                            detector_type=config['type']))
        self.active_network.network.load()

        return self.active_network.network


    def get_secondary_yolo_model(self, name):
        if self.secondary_network is not None:
            if self.secondary_network.name == name:
                return

        config = self.config[name]

        if self.secondary_network is not None:
            self.secondary_network.network.release()

        self.secondary_network = _ActiveNetwork(name,
                                             YoloModelProxy(model_path=config['path'],
                                                            threshold=config['threshold'],
                                                            input_tensor_name=config['input_tensor'],
                                                            output_tensor_name=config['output_tensor']))
        self.secondary_network.network.load()

        return self.secondary_network.network

NNManager = _NNManagerClass()
