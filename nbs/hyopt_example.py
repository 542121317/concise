from concise.preprocessing import encodeDNA
import pandas as pd
import numpy as np

import concise.layers as cl
import keras.layers as kl
import concise.initializers as ci
import concise.regularizers as cr
from keras.callbacks import EarlyStopping
from keras.models import Model, load_model
from keras.optimizers import Adam

#@mem.cache
def data(seq_length=101):
      
    def load(split="train"):
        dt = pd.read_csv("../data/RBP/PUM2_{0}.csv".format(split))
        # DNA/RNA sequence
        xseq = encodeDNA(dt.seq, maxlen=seq_length, seq_align='center')
        # response variable
        y = dt.binding_site.as_matrix().reshape((-1, 1)).astype("float")
        if split=="train":
            from concise.data import attract
            # add also the pwm_list
            pwm_list = attract.get_pwm_list(["129"])
            return {"seq": xseq}, y, pwm_list
        else:
            return {"seq": xseq}, y

    return load("train"), load("valid"), load("test")


def model(train_data, filters=1, kernel_size=9, motif_init=None, lr=0.001):
    seq_length = train_data[0]["seq"].shape[1]
    pwm_list = train_data[2]
    
    if motif_init is not None:
        # Motif init is a dictionary with fields: "stddev" 
        kinit = ci.PSSMKernelInitializer(pwm_list, 
                                         stddev=motif_init.get("stddev", 0.05),  # if not specified, use 0.05
                                         add_noise_before_Pwm2Pssm=True)
        binit = "zeros"
    else:
        kinit = "glorot_uniform"
        binit = "zeros"
        
        
    # sequence
    in_dna = cl.InputDNA(seq_length=seq_length, name="seq")
    x = cl.ConvDNA(filters=filters, 
                   kernel_size=kernel_size, 
                   activation="relu",
                   kernel_initializer=kinit,
                   bias_initializer=binit,
                   name="conv1")(in_dna)
    x = kl.AveragePooling1D(pool_size=4)(x)
    x = kl.Flatten()(x)
    
    x = kl.Dense(units=1)(x)
    m = Model(in_dna, x)
    m.compile(Adam(lr=lr), loss="binary_crossentropy", metrics=["acc"])
    return m