import os
from tensorflow.keras.models import load_model as lm
import tensorflow as tf
physical_devices = tf.config.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(physical_devices[0], True)

def exactModel(model='srGAN', inpSize=(None, 128, 128, 3), save='ram'):
    path = 'models/{}'.format(model)
    gen = lm(path)
    model_conf = gen.get_config()
    input_layer_name = model_conf['layers'][0]['name']
    model_conf['layers'][0] = {
                          'name': 'new_input',
                          'class_name': 'InputLayer',
                          'config': {
                              'batch_input_shape': inpSize,
                              'dtype': 'float32',
                              'sparse': False,
                              'name': 'new_input'
                          },
                          'inbound_nodes': []
                      }
    model_conf['layers'][1]['inbound_nodes'] = [[['new_input', 0, 0, {}]]]
    model_conf['input_layers'] = [['new_input', 0, 0]]

    newGen = gen.__class__.from_config(model_conf, custom_objects={})
    weights = [layer.get_weights() for layer in gen.layers[1:]]
    for layer, weight in zip(newGen.layers[1:], weights):
        layer.set_weights(weight)

    if save == 'disk':
        filename = 'gen_{}_{}'.format(inpSize[1], inpSize[2])
        newGen.save(os.path.join(path, filename))
    else:
        return newGen
