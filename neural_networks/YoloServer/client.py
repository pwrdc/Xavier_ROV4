from utils.project_managment import PROJECT_ROOT
import cv2
from utils.python_rest_subtask import PythonRESTSubtask

# Test use only!!!!
# Todo: MAKE MANUAL TEST FROM THIS FILE!

img = cv2.imread(f"{PROJECT_ROOT}/tests/integration/img.png")
server_task = PythonRESTSubtask.run("neural_networks/YoloServer/server.py",
                                    "-p 5000 -m tests/integration/yolo_test_model", port=5000, wait_ready=True)

result = server_task.post("predict", img)

result.denormalize(img.shape[1], img.shape[0], inplace=True)

p1 = (int(result.x1), int(result.y1))
p2 = (int(result.x2), int(result.y2))

img = cv2.rectangle(img, p1, p2, (255, 0, 255))
cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
