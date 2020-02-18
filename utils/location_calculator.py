# focal length of camera [mm]
FOCAL_LENGTH = 1000


def location_calculator(b_box, size_real, feature):
    """
    @param: b_box - bounding box of object [px]
    @param: size_real - real size of object feature [mm], taken from configs/objects_size.json
    @param: feature - name of b_box feature of which size is to be compared,
            "height" for b_box.h or "width" for b_box.w
    :return: object location relative to camera [mm]
    """
    if feature == "height":
        size_image = b_box.h
    elif feature == "width":
        size_image = b_box.w
    else:
        return
    distance = FOCAL_LENGTH * size_real / size_image
    x = distance * b_box.x / FOCAL_LENGTH
    y = distance * b_box.y / FOCAL_LENGTH

    return {"distance": distance, "x": x, "y": y}
