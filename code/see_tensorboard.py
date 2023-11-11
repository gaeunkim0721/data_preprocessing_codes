import tensorflow as tf
from tensorflow.python.summary.summary_iterator import summary_iterator





# Path to the event file
filename = '/home/gaeun/yolov5/runs/train/exp8/events.out.tfevents.1699295857.gaeun-ubuntu.17912.0'

# Extract events from the file
events_data = []
for e in summary_iterator(filename):
    for v in e.summary.value:
        events_data.append({"tag": v.tag, "value": v.simple_value if v.HasField("simple_value") else None})

# Print the first few entries for verification
print(events_data[:10])
