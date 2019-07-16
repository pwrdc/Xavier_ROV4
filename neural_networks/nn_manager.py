from neural_networks.yolo_model_proxy import YoloModelProxy
from typing import Optional
from collections import namedtuple
import json


class _ActiveNetwork:
    def __init__(self, name: str, network: YoloModelProxy):
        self.name = name
        self.network = network
class _NNManagerClass:
    def __init__(self):
        self.active_network: Optional[_ActiveNetwork] = None
        self.secondary_network: Optional[_ActiveNetwork] = None

        with open("models/models.json", "r") as f:
            self.config = json.load(f)

    def get_yolo_model(self, name):
        if self.active_network is not None:
            if self.active_network.name == name:
                return self.active_network.network

        config = self.config[name]

        if self.active_network is not None:
            self.active_network.network.release()

        if self.active_network is not None:
            self.secondary_network.network.release()
            self.secondary_network = None

        self.active_network = _ActiveNetwork(name,
                                             YoloModelProxy(model_path=config['path'],
                                                            threshold=config['threshold'],
                                                            input_tensor_name=config['input_tensor'],
                                                            output_tensor_name=config['output_tensor']))
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
