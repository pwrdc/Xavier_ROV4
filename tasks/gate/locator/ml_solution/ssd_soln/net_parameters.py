from utils import FeatureMap

S_MIN = 0.2
S_MAX = 0.9

FEATURE_MAPS = [
    FeatureMap(38, 38, [1, 2, 1/2]),
    FeatureMap(19, 19, [1, 2, 3, 1/3, 1/2]),
    FeatureMap(10, 10, [1, 2, 3, 1/3, 1/2]),
    FeatureMap(5, 5, [1, 2, 3, 1/3, 1/2]),
    FeatureMap(3, 3, [1, 2, 1/2]),
    FeatureMap(1, 1, [1, 2, 1/2]),
]
