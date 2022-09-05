'''
Artificial Intelligence Techniques SL	
artelnics@artelnics.com	

Your model has been exported to this python file.
You can manage it with the 'NeuralNetwork' class.	
Example:

	model = NeuralNetwork()	
	sample = [input_1, input_2, input_3, input_4, ...]	
	outputs = model.calculate_output(sample)

	Inputs Names: 	
	1 )udp.srcport
	2 )udp.dstport

You can predict with a batch of samples using calculate_batch_output method	
IMPORTANT: input batch must be <class 'numpy.ndarray'> type	
Example_1:	
	model = NeuralNetwork()	
	input_batch = np.array([[1, 2], [4, 5]], np.int32)	
	outputs = model.calculate_batch_output(input_batch)
Example_2:	
	input_batch = pd.DataFrame( {'col1': [1, 2], 'col2': [3, 4]})	
	outputs = model.calculate_batch_output(input_batch.values)
'''

import numpy as np
import pandas as pd
from pandas import ExcelWriter
import tkinter.filedialog as fd
import matplotlib.pyplot as plt
from variable import variable

def udp_nn(filename):
    model = NeuralNetwork()
    input_batch = pd.read_csv(filename)
    outputs = model.calculate_batch_output(input_batch.values)
    input_batch['probability'] = outputs.tolist()
    input_batch['probability'] = input_batch['probability'].round()
    
    #Построение графика
    sum_prob = input_batch['probability'].sum()
    sum_all = input_batch.shape[0]
    labels = ["Всего пакетов","С вложениями"]
    vals = [sum_all,sum_prob]
    fig, ax = plt.subplots()
    explode = (0.1, 0)
    ax.pie(vals,labels = labels,autopct='%1.1f%%', shadow=True,explode=explode)
    plt.title("Вычисление нейронной сетью для UDP")
    text_g = 'Всего пакетов: ' + str(sum_all) + ' | Пакетов с вложениями: ' + str(sum_prob)
    ax.text(-1.25,-1.2,text_g,fontsize=10)
    plt.show()
     
    if variable.check():
        saved = fd.asksaveasfilename(
                filetypes=(("Excel files", "*.xlsx"),
                           ("All files", "*.*")))
        if saved!='':
            input_batch.to_excel(saved + '.xlsx')

class NeuralNetwork:
 
    def __init__(self):
 
        self.parameters_number = 13
 
    def scaling_layer(self,inputs):

        outputs = [None] * 2

        outputs[0] = (inputs[0]-7265.120117)/18142.40039
        outputs[1] = (inputs[1]-4200.870117)/13345.09961

        return outputs;


    def perceptron_layer_1(self,inputs):

        combinations = [None] * 3

        combinations[0] = 0.160645 +0.292793*inputs[0] +0.303344*inputs[1] 
        combinations[1] = -0.643541 -1.4614*inputs[0] -1.45779*inputs[1] 
        combinations[2] = 0.675969 +1.52381*inputs[0] +1.55778*inputs[1] 
        
        activations = [None] * 3

        activations[0] = np.tanh(combinations[0])
        activations[1] = np.tanh(combinations[1])
        activations[2] = np.tanh(combinations[2])

        return activations;


    def probabilistic_layer(self, inputs):

        combinations = [None] * 1

        combinations[0] = -0.418286 -0.455136*inputs[0] +2.18167*inputs[1] -2.29962*inputs[2] 
        
        activations = [None] * 1

        activations[0] = 1.0/(1.0 + np.exp(-combinations[0]));

        return activations;


    def calculate_output(self, inputs):

        output_scaling_layer = self.scaling_layer(inputs)

        output_perceptron_layer_1 = self.perceptron_layer_1(output_scaling_layer)

        output_probabilistic_layer = self.probabilistic_layer(output_perceptron_layer_1)

        return output_probabilistic_layer


    def calculate_batch_output(self, input_batch):

        output = []

        for i in range(input_batch.shape[0]):

            inputs = list(input_batch[i])

            output_scaling_layer = self.scaling_layer(inputs)

            output_perceptron_layer_1 = self.perceptron_layer_1(output_scaling_layer)

            output_probabilistic_layer = self.probabilistic_layer(output_perceptron_layer_1)

            output = np.append(output,output_probabilistic_layer, axis=0)

        return output
