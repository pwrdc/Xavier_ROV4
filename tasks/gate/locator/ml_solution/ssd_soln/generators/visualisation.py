from utils import Box, draw_box
from generators.label_assigning import generate_fm_anchor_boxes
from net_parameters import FEATURE_MAPS


def show_bounding_boxes(image, nn_predictions, threshold=0.5, with_corrections = True):
    for fm_index, result in enumerate(nn_predictions):
        anchor_boxes = generate_fm_anchor_boxes(fm_index, len(nn_predictions), FEATURE_MAPS[fm_index].aspect_ratios)

        for i, anchor_box in enumerate(anchor_boxes):
            r = result[:, :, i, :]

            for x in range(FEATURE_MAPS[fm_index].width):
                for y in range(FEATURE_MAPS[fm_index].height):
                    if r[x, y, 0] > threshold:
                        x_det = (x + 0.5) / FEATURE_MAPS[fm_index].width
                        y_det = (y + 0.5) / FEATURE_MAPS[fm_index].height
                        w_det = anchor_box.width
                        h_det = anchor_box.height

                        if with_corrections:
                            x_det = x_det + r[x, y, 1]
                            y_det = y_det + r[x, y, 2]
                            w_det = w_det * (1 + r[x, y, 3])
                            h_det = h_det * (1 + r[x, y, 4])

                        draw_box(image, Box(x_det, y_det, w_det, h_det))

