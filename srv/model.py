import numpy as np

class NeuralNetwork:
    def __init__(self):
        self.inputs_number = 12
        self.inputs_names = ['udp.srcport', 'udp.dstport', 'tcp.srcport', 'tcp.dstport', 'tcp.ack', 'tcp.urgent_pointer', 'tcp.window_size_value', 'tcp.reserved', 'ip.len', 'ip.id', 'ip.tos', 'ip.frag']


    def ReLU (x):
        z = max(0, x)
        return z


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

        scaled_udp_dot_srcpo_rt = (udp_dot_srcpo_rt-5218.049805)/16602.69922
        scaled_udp_dot_dstpo_rt = (udp_dot_dstpo_rt-999.5170288)/7427.040039
        scaled_tcp_dot_srcpo_rt = (tcp_dot_srcpo_rt-17752.69922)/25262.19922
        scaled_tcp_dot_dstpo_rt = (tcp_dot_dstpo_rt-26093.19922)/26673.5
        scaled_tcp_dot_ack = (tcp_dot_ack-1022990016)/1182620032
        scaled_tcp_dot_urgent_poin_ter = (tcp_dot_urgent_poin_ter-731.1170044)/5442.049805
        scaled_tcp_dot_win_d_ow_size_value = (tcp_dot_win_d_ow_size_value-2558.040039)/7387.680176
        scaled_tcp_dot_reserved = (tcp_dot_reserved+0.111585997)/0.7446950078
        scaled_ip_dot_len = (ip_dot_len-539.8610229)/668.2030029
        scaled_ip_dot_id = (ip_dot_id-19986)/21359.69922
        scaled_ip_dot_tos = (ip_dot_tos-6.11853981)/30.89389992
        scaled_ip_dot_frag = (ip_dot_frag-195.246994)/984.5720215

        perceptron_layer_1_output_0 = NeuralNetwork.ReLU( 0.876258 + (scaled_udp_dot_srcpo_rt*0.0360303) + (scaled_udp_dot_dstpo_rt*1.10202) + (scaled_tcp_dot_srcpo_rt*-0.362282) + (scaled_tcp_dot_dstpo_rt*1.04768) + (scaled_tcp_dot_ack*-0.921645) + (scaled_tcp_dot_urgent_poin_ter*-0.886251) + (scaled_tcp_dot_win_d_ow_size_value*0.4356) + (scaled_tcp_dot_reserved*-0.429417) + (scaled_ip_dot_len*1.93875) + (scaled_ip_dot_id*0.00504839) + (scaled_ip_dot_tos*-0.420988) + (scaled_ip_dot_frag*-1.01476) )
        perceptron_layer_1_output_1 = NeuralNetwork.ReLU( 0.917276 + (scaled_udp_dot_srcpo_rt*-0.309223) + (scaled_udp_dot_dstpo_rt*-1.03782) + (scaled_tcp_dot_srcpo_rt*0.29557) + (scaled_tcp_dot_dstpo_rt*-0.907914) + (scaled_tcp_dot_ack*-0.557675) + (scaled_tcp_dot_urgent_poin_ter*0.379537) + (scaled_tcp_dot_win_d_ow_size_value*-1.18781) + (scaled_tcp_dot_reserved*0.237204) + (scaled_ip_dot_len*-0.267321) + (scaled_ip_dot_id*0.928384) + (scaled_ip_dot_tos*-1.95166) + (scaled_ip_dot_frag*-1.64979) )
        perceptron_layer_1_output_2 = NeuralNetwork.ReLU( 0.321028 + (scaled_udp_dot_srcpo_rt*0.219629) + (scaled_udp_dot_dstpo_rt*-1.09755) + (scaled_tcp_dot_srcpo_rt*-0.707354) + (scaled_tcp_dot_dstpo_rt*-0.153826) + (scaled_tcp_dot_ack*0.225461) + (scaled_tcp_dot_urgent_poin_ter*1.05072) + (scaled_tcp_dot_win_d_ow_size_value*-0.471033) + (scaled_tcp_dot_reserved*-0.742544) + (scaled_ip_dot_len*-1.73212) + (scaled_ip_dot_id*1.1621) + (scaled_ip_dot_tos*3.01774) + (scaled_ip_dot_frag*1.41498) )
        perceptron_layer_1_output_3 = NeuralNetwork.ReLU( 1.49703 + (scaled_udp_dot_srcpo_rt*0.0265269) + (scaled_udp_dot_dstpo_rt*-0.227563) + (scaled_tcp_dot_srcpo_rt*0.515486) + (scaled_tcp_dot_dstpo_rt*0.325887) + (scaled_tcp_dot_ack*0.737193) + (scaled_tcp_dot_urgent_poin_ter*-1.30848) + (scaled_tcp_dot_win_d_ow_size_value*-1.31684) + (scaled_tcp_dot_reserved*0.0778813) + (scaled_ip_dot_len*0.58356) + (scaled_ip_dot_id*0.751968) + (scaled_ip_dot_tos*-3.66646) + (scaled_ip_dot_frag*-1.32647) )
        perceptron_layer_1_output_4 = NeuralNetwork.ReLU( -0.385875 + (scaled_udp_dot_srcpo_rt*-0.0527497) + (scaled_udp_dot_dstpo_rt*0.109676) + (scaled_tcp_dot_srcpo_rt*0.616936) + (scaled_tcp_dot_dstpo_rt*0.385727) + (scaled_tcp_dot_ack*-0.310198) + (scaled_tcp_dot_urgent_poin_ter*-0.0650603) + (scaled_tcp_dot_win_d_ow_size_value*-0.112347) + (scaled_tcp_dot_reserved*-0.0461745) + (scaled_ip_dot_len*0.584613) + (scaled_ip_dot_id*-2.24907) + (scaled_ip_dot_tos*3.34077) + (scaled_ip_dot_frag*-0.268078) )
        perceptron_layer_1_output_5 = NeuralNetwork.ReLU( 0.939274 + (scaled_udp_dot_srcpo_rt*1.2727) + (scaled_udp_dot_dstpo_rt*0.448785) + (scaled_tcp_dot_srcpo_rt*-0.888859) + (scaled_tcp_dot_dstpo_rt*-1.16763) + (scaled_tcp_dot_ack*-0.763437) + (scaled_tcp_dot_urgent_poin_ter*1.44053) + (scaled_tcp_dot_win_d_ow_size_value*1.17913) + (scaled_tcp_dot_reserved*0.419321) + (scaled_ip_dot_len*-1.51593) + (scaled_ip_dot_id*-0.21525) + (scaled_ip_dot_tos*2.42987) + (scaled_ip_dot_frag*1.87016) )
        perceptron_layer_1_output_6 = NeuralNetwork.ReLU( 0.842286 + (scaled_udp_dot_srcpo_rt*0.600493) + (scaled_udp_dot_dstpo_rt*-1.10205) + (scaled_tcp_dot_srcpo_rt*0.206463) + (scaled_tcp_dot_dstpo_rt*0.733516) + (scaled_tcp_dot_ack*0.0500375) + (scaled_tcp_dot_urgent_poin_ter*0.0336364) + (scaled_tcp_dot_win_d_ow_size_value*0.12086) + (scaled_tcp_dot_reserved*-0.656984) + (scaled_ip_dot_len*2.49236) + (scaled_ip_dot_id*-0.22209) + (scaled_ip_dot_tos*-1.04764) + (scaled_ip_dot_frag*-1.17154) )

        perceptron_layer_2_output_0 = NeuralNetwork.ReLU( -0.189148 + (perceptron_layer_1_output_0*-2.96027) + (perceptron_layer_1_output_1*-1.21744) + (perceptron_layer_1_output_2*1.65952) + (perceptron_layer_1_output_3*-0.874926) + (perceptron_layer_1_output_4*5.24402) + (perceptron_layer_1_output_5*1.05734) + (perceptron_layer_1_output_6*-2.53906) )
        perceptron_layer_2_output_1 = NeuralNetwork.ReLU( 0.4134 + (perceptron_layer_1_output_0*-3.48883) + (perceptron_layer_1_output_1*-1.66328) + (perceptron_layer_1_output_2*-6.68607) + (perceptron_layer_1_output_3*0.655009) + (perceptron_layer_1_output_4*2.89037) + (perceptron_layer_1_output_5*-1.1717) + (perceptron_layer_1_output_6*-10.0879) )
        perceptron_layer_2_output_2 = NeuralNetwork.ReLU( 1.43613 + (perceptron_layer_1_output_0*4.173) + (perceptron_layer_1_output_1*0.523123) + (perceptron_layer_1_output_2*-1.26229) + (perceptron_layer_1_output_3*2.49017) + (perceptron_layer_1_output_4*-3.67674) + (perceptron_layer_1_output_5*-0.362162) + (perceptron_layer_1_output_6*2.0781) )

        probabilistic_layer_combinations_0 = -0.225905 +3.81198*perceptron_layer_2_output_0 +12.5112*perceptron_layer_2_output_1 -3.46981*perceptron_layer_2_output_2

        counter = 1.0/(1.0 + np.exp(-probabilistic_layer_combinations_0) )

        out = [None]*1

        out[0] = counter

        return out


    def calculate_batch_output(self, input_batch):
        output_batch = [None]*input_batch.shape[0]

        for i in range(input_batch.shape[0]):

            inputs = list(input_batch[i])

            output = self.calculate_outputs(inputs)

            output_batch[i] = output

        return output_batch
