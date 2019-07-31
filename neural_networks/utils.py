def extract_prediction(bounding_boxes, name):
    for bounding_box in bounding_boxes:
        if bounding_box.detected_item == name:
            return bounding_box

    return None