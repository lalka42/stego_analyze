''' 
Artificial Intelligence Techniques SL	
artelnics@artelnics.com	

Your model has been exported to this python file.
You can manage it with the 'NeuralNetwork' class.	
Example:

	model = NeuralNetwork()	
	sample = [input_1, input_2, input_3, input_4, ...]	
	outputs = model.calculate_outputs(sample)


Inputs Names: 	
	0) udp_dot_srcpo_rt
	1) udp_dot_dstpo_rt
	2) tcp_dot_srcpo_rt
	3) tcp_dot_dstpo_rt
	4) tcp_dot_ack
	5) tcp_dot_urgent_poin_ter
	6) tcp_dot_win_d_ow_size_value
	7) tcp_dot_reserved
	8) ip_dot_len
	9) ip_dot_id
	10) ip_dot_tos
	11) ip_dot_frag


You can predict with a batch of samples using calculate_batch_output method	
IMPORTANT: input batch must be <class 'numpy.ndarray'> type	
Example_1:	
	model = NeuralNetwork()	
	input_batch = np.array([[1, 2], [4, 5]])	
	outputs = model.calculate_batch_output(input_batch)
Example_2:	
	input_batch = pd.DataFrame( {'col1': [1, 2], 'col2': [3, 4]})	
	outputs = model.calculate_batch_output(input_batch.values)
'''

import numpy as np


class NeuralNetwork:
    def __init__(self):
        self.inputs_number = 12
        self.inputs_names = ['udp.srcport', 'udp.dstport', 'tcp.srcport', 'tcp.dstport', 'tcp.ack',
                             'tcp.urgent_pointer', 'tcp.window_size_value', 'tcp.reserved', 'ip.len', 'ip.id', 'ip.tos',
                             'ip.frag']

    def calculate_outputs(self, inputs):
        udp_dot_srcpo_rt = inputs[0]
        udp_dot_dstpo_rt = inputs[1]
        tcp_dot_srcpo_rt = inputs[2]
        tcp_dot_dstpo_rt = inputs[3]
        tcp_dot_ack = inputs[4]
        tcp_dot_urgent_poin_ter = inputs[5]
        tcp_dot_win_d_ow_size_value = inputs[6]
        tcp_dot_reserved = inputs[7]
        ip_dot_len = inputs[8]
        ip_dot_id = inputs[9]
        ip_dot_tos = inputs[10]
        ip_dot_frag = inputs[11]

        scaled_udp_dot_srcpo_rt = (udp_dot_srcpo_rt - 6028.029785) / 16401.5
        scaled_udp_dot_dstpo_rt = (udp_dot_dstpo_rt - 42366) / 21331
        scaled_tcp_dot_srcpo_rt = (tcp_dot_srcpo_rt - 2269.949951) / 11044.5
        scaled_tcp_dot_dstpo_rt = (tcp_dot_dstpo_rt - 2845.060059) / 12252.09961
        scaled_tcp_dot_ack = (tcp_dot_ack - 165344992) / 675323008
        scaled_tcp_dot_urgent_poin_ter = (tcp_dot_urgent_poin_ter - 73.02590179) / 1728.51001
        scaled_tcp_dot_win_d_ow_size_value = (tcp_dot_win_d_ow_size_value - 272.0849915) / 2976.120117
        scaled_tcp_dot_reserved = (tcp_dot_reserved + 0.9020649791) / 0.3628830016
        scaled_ip_dot_len = (ip_dot_len - 1077.160034) / 460.696991
        scaled_ip_dot_id = (ip_dot_id - 42217) / 105737
        scaled_ip_dot_tos = (ip_dot_tos - 0.5459700227) / 9.294119835
        scaled_ip_dot_frag = (ip_dot_frag - 17.76460075) / 301.4880066

        perceptron_layer_1_output_0 = np.tanh(
            0.885491 + (scaled_udp_dot_srcpo_rt * 0.0534756) + (scaled_udp_dot_dstpo_rt * -1.19513) + (
                        scaled_tcp_dot_srcpo_rt * 0.596938) + (scaled_tcp_dot_dstpo_rt * 0.975029) + (
                        scaled_tcp_dot_ack * -0.0396837) + (scaled_tcp_dot_urgent_poin_ter * 0.285022) + (
                        scaled_tcp_dot_win_d_ow_size_value * 0.755648) + (scaled_tcp_dot_reserved * -0.321843) + (
                        scaled_ip_dot_len * -1.60436) + (scaled_ip_dot_id * 0.173101) + (
                        scaled_ip_dot_tos * 1.13473) + (scaled_ip_dot_frag * 1.18388))
        perceptron_layer_1_output_1 = np.tanh(
            -1.11356 + (scaled_udp_dot_srcpo_rt * -0.00117439) + (scaled_udp_dot_dstpo_rt * -0.352451) + (
                        scaled_tcp_dot_srcpo_rt * 1.57638) + (scaled_tcp_dot_dstpo_rt * -0.54398) + (
                        scaled_tcp_dot_ack * -0.440363) + (scaled_tcp_dot_urgent_poin_ter * 0.416998) + (
                        scaled_tcp_dot_win_d_ow_size_value * -0.540006) + (scaled_tcp_dot_reserved * 0.683858) + (
                        scaled_ip_dot_len * -0.635522) + (scaled_ip_dot_id * -0.205739) + (
                        scaled_ip_dot_tos * 0.84772) + (scaled_ip_dot_frag * 2.03475))
        perceptron_layer_1_output_2 = np.tanh(
            2.00753 + (scaled_udp_dot_srcpo_rt * -0.478481) + (scaled_udp_dot_dstpo_rt * -0.585438) + (
                        scaled_tcp_dot_srcpo_rt * -0.167183) + (scaled_tcp_dot_dstpo_rt * 0.724704) + (
                        scaled_tcp_dot_ack * 0.457414) + (scaled_tcp_dot_urgent_poin_ter * -1.9663) + (
                        scaled_tcp_dot_win_d_ow_size_value * -1.4812) + (scaled_tcp_dot_reserved * 0.0405871) + (
                        scaled_ip_dot_len * 0.848929) + (scaled_ip_dot_id * 0.0335002) + (
                        scaled_ip_dot_tos * -1.60039) + (scaled_ip_dot_frag * -2.76912))

        probabilistic_layer_combinations_0 = -3.04376 - 0.184294 * perceptron_layer_1_output_0 + 3.29077 * perceptron_layer_1_output_1 - 5.3558 * perceptron_layer_1_output_2

        counter = 1.0 / (1.0 + np.exp(-probabilistic_layer_combinations_0))

        out = [None] * 1

        out[0] = counter

        return out

    def calculate_batch_output(self, input_batch):
        output_batch = [None] * input_batch.shape[0]

        for i in range(input_batch.shape[0]):
            inputs = list(input_batch[i])

            output = self.calculate_outputs(inputs)

            output_batch[i] = output

        return output_batch


'''
def main():

	inputs = []

	udp_dot_srcpo_rt = #- ENTER YOUR VALUE HERE -#
	inputs.append(udp_dot_srcpo_rt)

	udp_dot_dstpo_rt = #- ENTER YOUR VALUE HERE -#
	inputs.append(udp_dot_dstpo_rt)

	tcp_dot_srcpo_rt = #- ENTER YOUR VALUE HERE -#
	inputs.append(tcp_dot_srcpo_rt)

	tcp_dot_dstpo_rt = #- ENTER YOUR VALUE HERE -#
	inputs.append(tcp_dot_dstpo_rt)

	tcp_dot_ack = #- ENTER YOUR VALUE HERE -#
	inputs.append(tcp_dot_ack)

	tcp_dot_urgent_poin_ter = #- ENTER YOUR VALUE HERE -#
	inputs.append(tcp_dot_urgent_poin_ter)

	tcp_dot_win_d_ow_size_value = #- ENTER YOUR VALUE HERE -#
	inputs.append(tcp_dot_win_d_ow_size_value)

	tcp_dot_reserved = #- ENTER YOUR VALUE HERE -#
	inputs.append(tcp_dot_reserved)

	ip_dot_len = #- ENTER YOUR VALUE HERE -#
	inputs.append(ip_dot_len)

	ip_dot_id = #- ENTER YOUR VALUE HERE -#
	inputs.append(ip_dot_id)

	ip_dot_tos = #- ENTER YOUR VALUE HERE -#
	inputs.append(ip_dot_tos)

	ip_dot_frag = #- ENTER YOUR VALUE HERE -#
	inputs.append(ip_dot_frag)

	nn = NeuralNetwork()
	outputs = nn.calculate_outputs(inputs)
	print(outputs)

main()
'''