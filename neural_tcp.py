

import numpy as np
import pandas as pd
from pandas import ExcelWriter
import tkinter.filedialog as fd
import matplotlib.pyplot as plt
from variable import variable


def tcp_nn(filename):
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
    plt.title("Вычисление нейронной сетью для TCP")
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
 
        self.parameters_number = 45
 
    def scaling_layer(self,inputs):

        outputs = [None] * 5

        outputs[0] = (inputs[0]-14370.40039)/25680
        outputs[1] = (inputs[1]-15935.2002)/26807.59961
        outputs[2] = (inputs[2]-5834.339844)/13162.5
        outputs[3] = (inputs[3]-37.24300003)/206.1849976
        outputs[4] = (inputs[4]-3263.669922)/8581.629883

        return outputs;


    def perceptron_layer_1(self,inputs):

        combinations = [None] * 4

        combinations[0] = -0.2855 -0.381023*inputs[0] -0.45088*inputs[1] +0.0779454*inputs[2] +0.0547478*inputs[3] -0.0402656*inputs[4] 
        combinations[1] = 0.372812 +0.485452*inputs[0] +0.528542*inputs[1] -0.112544*inputs[2] -0.0747865*inputs[3] +0.00395*inputs[4] 
        combinations[2] = -0.334456 -0.522634*inputs[0] -0.533194*inputs[1] +0.0944311*inputs[2] +0.0614533*inputs[3] -0.02099*inputs[4] 
        combinations[3] = 0.00368617 -1.45805*inputs[0] -0.0797397*inputs[1] -0.0590527*inputs[2] +0.00376823*inputs[3] +2.33803*inputs[4] 
        
        activations = [None] * 4

        activations[0] = np.tanh(combinations[0])
        activations[1] = np.tanh(combinations[1])
        activations[2] = np.tanh(combinations[2])
        activations[3] = np.tanh(combinations[3])

        return activations;


    def perceptron_layer_2(self,inputs):

        combinations = [None] * 3

        combinations[0] = -0.427384 +0.572397*inputs[0] -0.782182*inputs[1] +0.800959*inputs[2] +1.79491*inputs[3] 
        combinations[1] = -0.357662 +0.497297*inputs[0] -0.637927*inputs[1] +0.653574*inputs[2] +1.5058*inputs[3] 
        combinations[2] = 0.0869644 -0.155965*inputs[0] +0.136485*inputs[1] -0.134234*inputs[2] -0.403223*inputs[3] 
        
        activations = [None] * 3

        activations[0] = np.tanh(combinations[0])
        activations[1] = np.tanh(combinations[1])
        activations[2] = np.tanh(combinations[2])

        return activations;


    def perceptron_layer_3(self,inputs):

        combinations = [None] * 1

        combinations[0] = 0.157755 -2.25473*inputs[0] -1.85197*inputs[1] +0.4648*inputs[2] 
        
        activations = [None] * 1

        activations[0] = np.tanh(combinations[0])

        return activations;


    def probabilistic_layer(self, inputs):

        combinations = [None] * 1

        combinations[0] = -0.135208 -4.03328*inputs[0] 
        
        activations = [None] * 1

        activations[0] = 1.0/(1.0 + np.exp(-combinations[0]));

        return activations;


    def calculate_output(self, inputs):

        output_scaling_layer = self.scaling_layer(inputs)

        output_perceptron_layer_1 = self.perceptron_layer_1(output_scaling_layer)

        output_perceptron_layer_2 = self.perceptron_layer_2(output_perceptron_layer_1)

        output_perceptron_layer_3 = self.perceptron_layer_3(output_perceptron_layer_2)

        output_probabilistic_layer = self.probabilistic_layer(output_perceptron_layer_3)

        return output_probabilistic_layer


    def calculate_batch_output(self, input_batch):

        output = []

        for i in range(input_batch.shape[0]):

            inputs = list(input_batch[i])

            output_scaling_layer = self.scaling_layer(inputs)

            output_perceptron_layer_1 = self.perceptron_layer_1(output_scaling_layer)

            output_perceptron_layer_2 = self.perceptron_layer_2(output_perceptron_layer_1)

            output_perceptron_layer_3 = self.perceptron_layer_3(output_perceptron_layer_2)

            output_probabilistic_layer = self.probabilistic_layer(output_perceptron_layer_3)

            output = np.append(output,output_probabilistic_layer, axis=0)

        return output



