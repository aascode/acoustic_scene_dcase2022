'''
Baseline network
'''

from tensorflow.keras.layers import (Conv2D, MaxPool2D, Dropout, Input, BatchNormalization,
                                    GlobalAveragePooling2D, GlobalMaxPooling2D, Dense, ELU)
from tensorflow.keras.models import Model

def construct_baseline_model(include_classification=True, nclasses=10, **parameters):

    spectrogram_dim = parameters['spectrogram_dim']
    filters = parameters['nfilters']
    top_flatten = parameters['top_flatten']
    dropout = parameters['dropout']
    pooling = parameters['pooling']
    kernel_size  = parameters['kernel_size']
    verbose = parameters['verbose']

    
    spectogram_dim = tuple(map(int, spectrogram_dim.split(', ')))
    print(type(spectogram_dim))
    inp = Input(shape=(64,51,1))

    for i in range(0, len(filters)):
        if i == 0:
            x = Conv2D(filters[i], kernel_size, padding='same')(inp)
        else:
            x = Conv2D(filters[i], kernel_size, padding='same')(x)
        
        x = BatchNormalization()(x)
        x = ELU()(x)
 
        x = Conv2D(filters[i], kernel_size, padding='same')(x)
        x = BatchNormalization()(x)
        x = ELU()(x)

        x = MaxPool2D(pool_size=pooling[i])(x)
        x = Dropout(rate=dropout[i])(x)

    if top_flatten == 'avg':
         x = GlobalAveragePooling2D()(x)
    elif top_flatten == 'max':
         x = GlobalMaxPooling2D()(x)

    if include_classification:

        x = Dense(units=nclasses, activation='softmax', name='pred_layer')(x)

    model = Model(inputs=inp, outputs=x)

    if verbose:
        print(model.summary())

    return model


if __name__ == '__main__':

    audio_network_settings = {
        'kernel_size': 3,
        'nfilters': (40, 40),
        'pooling': [(1, 10), (1, 10)],
        'dropout': [0.3, 0.3],
        'top_flatten': 'avg',
        'spectrogram_dim': (64, 500, 1),
        'verbose': True
    }

    audio_model = construct_baseline_model(include_classification=True, **audio_network_settings)