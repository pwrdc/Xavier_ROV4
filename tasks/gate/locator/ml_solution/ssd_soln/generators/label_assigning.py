import numpy as np
from utils import Box, FeatureMap, AnchorBoxDims, intersection_over_union
from net_parameters import S_MIN, S_MAX


def generate_fm_anchor_boxes(feature_map_index: int, num_feature_maps: int, aspect_ratios: [float]) -> [AnchorBoxDims]:
    # ref: https://arxiv.org/abs/1512.02325 equation 4
    anchor_boxes_sizes = []

    s = S_MIN + (S_MAX - S_MIN) / (num_feature_maps - 1) * feature_map_index  # no -1 because of 0-indexing!

    for ar in aspect_ratios:
        w = s * np.sqrt(ar)
        h = s / np.sqrt(ar)
        anchor_boxes_sizes.append(AnchorBoxDims(width=w, height=h))

    s_0 = np.sqrt(s * s + 1)
    anchor_boxes_sizes.append(AnchorBoxDims(width=s_0, height=s_0))

    return anchor_boxes_sizes


def generate_labels(bounding_box: Box, feature_maps: [FeatureMap]):
    feature_map_labels = []
    num_feature_maps = len(feature_maps)

    for i, feature_map in enumerate(feature_maps):
        num_aspect_ratios = len(feature_map.aspect_ratios) + 1

        feature_map_label = np.zeros(
            (feature_map.width, feature_map.height, num_aspect_ratios, 5),
            np.float)

        anchor_boxes = generate_fm_anchor_boxes(i, num_feature_maps, feature_map.aspect_ratios)

        for x in range(feature_map.width):
            for y in range(feature_map.height):
                x_norm = (x + 0.5) / feature_map.width
                y_norm = (y + 0.5) / feature_map.height

                best_iou_score = 0
                best_iou_index = 0
                best_iou_x_delta = 0
                best_iou_y_delta = 0
                best_iou_w_scale = 0
                best_iou_h_scale = 0

                for j, anchor_box in enumerate(anchor_boxes):
                    iou = intersection_over_union(Box(x_norm, y_norm, anchor_box.width, anchor_box.height),
                                                  bounding_box)

                    if iou > best_iou_score:
                        best_iou_score = iou
                        best_iou_index = j
                        best_iou_x_delta = bounding_box.x - x_norm
                        best_iou_y_delta = bounding_box.y - y_norm
                        best_iou_w_scale = bounding_box.w / anchor_box.width - 1.0
                        best_iou_h_scale = bounding_box.h / anchor_box.height - 1.0

                if best_iou_score > 0.5:
                    feature_map_label[x, y, best_iou_index] = [1.0,
                                                               best_iou_x_delta,
                                                               best_iou_y_delta,
                                                               best_iou_w_scale,
                                                               best_iou_h_scale]

        feature_map_labels.append(feature_map_label)
    return feature_map_labels

