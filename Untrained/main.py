import numpy as np

from google.colab import files

from tflite_model_maker.config import ExportFormat, QuantizationConfig
from tflite_model_maker import model_spec
from tflite_model_maker import object_detector

from tflite_support import metadata

import tensorflow as tf
assert tf.__version__.startswith('2')

tf.get_logger().setLevel('ERROR')
from absl import logging
logging.set_verbosity(logging.ERROR)

train_data = object_detector.DataLoader.from_pascal_voc(
    'Aerials/train',
    ['food']
)

val_data = object_detector.DataLoader.from_pascal_voc(
    'Aerials/validate'
    ['food']
)

spec = model_spec.get('efficientdet_lite1')
model = object_detector.create(train_data, model_spec=spec, batch_size=4, train_whole_model=True, epochs=20, validation_data=val_data)

model.evaluate(val_data)

model.export(export_dir='.', tflite_filename='food_model.tflite')
model.evaluate_tflite('food_model.tflite', val_data)

files.download('food_model.tflite')

populator_dst = metadata.MetadataPopulator.with_model_file('food_model_edgetpu.tflite')

with open('food_model.tflite', 'rb') as f:
  populator_dst.load_metadata_and_associated_files(f.read())

populator_dst.populate()
updated_model_buf = populator_dst.get_model_buffer()

files.download('food_model_edgetpu.tflite')