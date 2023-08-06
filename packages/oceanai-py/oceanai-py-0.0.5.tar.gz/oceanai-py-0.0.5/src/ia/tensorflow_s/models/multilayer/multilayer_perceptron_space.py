from typing import List
import tensorflow as tf
from src.ia.tensorflow_s.sequential_space import SequentialSpace

class MultilayerPerceptronArgs:
    
    def __init__(self,inputs:int,outputs:int,hidden:List[int],activation=None,use_bias=True,kernel_initializer="glorot_uniform", bias_initializer='zeros',kernel_regularizer=None,bias_regularizer=None,activity_regularizer=None, kernel_constraint=None,bias_constraint=None) -> None:
        self.inputs=inputs
        self.outputs=outputs
        self.hidden=hidden
        self.activation=activation
        self.use_bias = use_bias
        self.kernel_initializer=kernel_initializer
        self.bias_initializer=bias_initializer
        self.kernel_regularizer = kernel_regularizer
        self.bias_regularizer = bias_regularizer
        self.activity_regularizer = activity_regularizer
        self.kernel_constrain = kernel_constraint
        self.bias_constraint = bias_constraint
        

class MultilayerPerceptronSpace(SequentialSpace):
    
    def __init__(self,args:MultilayerPerceptronArgs):
        layers = [tf.keras.layers.Dense(
                    units=args.inputs,
                    activation=args.activation,
                    use_bias=args.use_bias,
                    kernel_initializer=args.kernel_initializer,
                    bias_initializer=args.bias_initializer,
                    kernel_regularizer=args.kernel_regularizer,
                    bias_regularizer=args.bias_regularizer,
                    activity_regularizer=args.activity_regularizer,
                    kernel_constraint=args.kernel_constrain,
                    bias_constraint=args.bias_constraint,
                    input_shape=(args.inputs,)
                    )
                ]
        for size in args.hidden:
            layers.append(tf.keras.layers.Dense(
                    units=size,
                    activation=args.activation,
                    use_bias=args.use_bias,
                    kernel_initializer=args.kernel_initializer,
                    bias_initializer=args.bias_initializer,
                    kernel_regularizer=args.kernel_regularizer,
                    bias_regularizer=args.bias_regularizer,
                    activity_regularizer=args.activity_regularizer,
                    kernel_constraint=args.kernel_constrain,
                    bias_constraint=args.bias_constraint
                    ))
        
        layers.append(tf.keras.layers.Dense(
                    units=args.outputs,
                    activation=args.activation,
                    use_bias=args.use_bias,
                    kernel_initializer=args.kernel_initializer,
                    bias_initializer=args.bias_initializer,
                    kernel_regularizer=args.kernel_regularizer,
                    bias_regularizer=args.bias_regularizer,
                    activity_regularizer=args.activity_regularizer,
                    kernel_constraint=args.kernel_constrain,
                    bias_constraint=args.bias_constraint
                    ))
        super().__init__(layers)
        
        
        
        
        
        