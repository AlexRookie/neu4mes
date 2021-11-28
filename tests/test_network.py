import unittest, logging
from neu4mes import *

class Neu4mesNetworkBuildingTest(unittest.TestCase):
    def test_network_building_simple(self):
        input1 = Input('in1')
        input2 = Input('in2')
        output = Input('out')
        rel1 = Linear(input1.tw(0.05))
        rel2 = Linear(input1.tw(0.01))
        fun = Output(output.z(-1),rel1+rel2)

        test = Neu4mes()
        test.addModel(fun)
        test.neuralizeModel(0.01)

        self.assertEqual(test.max_n_samples, 5) # 5 samples
        self.assertEqual({'in1': 5} , test.input_n_samples)
        
        self.assertEqual([None,5] ,list(test.inputs_for_model['in1'].shape))
        self.assertEqual([None,None,5] ,list(test.inputs_for_rnn_model['in1'].shape))

    def test_network_building_complex1(self):
        input1 = Input('in1')
        input2 = Input('in2')
        output = Input('out')
        rel1 = Linear(input1.tw(0.05))
        rel2 = Linear(input1.tw(0.01))
        rel3 = Linear(input2.tw(0.05))
        rel4 = Linear(input2.tw([0.02,-0.02]))
        fun = Output(output.z(-1),rel1+rel2+rel3+rel4)

        test = Neu4mes()
        test.addModel(fun)
        test.neuralizeModel(0.01)

        self.assertEqual(test.max_n_samples, 7) # 5 samples + 2 samples of the horizon
        self.assertEqual({'in1': 5, 'in2': 7} , test.input_n_samples)
        
        self.assertEqual([None,5] ,list(test.inputs_for_model['in1'].shape))
        self.assertEqual([None,7] ,list(test.inputs_for_model['in2'].shape))
        self.assertEqual([None,None,5] ,list(test.inputs_for_rnn_model['in1'].shape))
        self.assertEqual([None,None,7] ,list(test.inputs_for_rnn_model['in2'].shape))
        self.assertEqual([None,5] ,list(test.inputs['in1'].shape))
        self.assertEqual([None,7] ,list(test.inputs['in2'].shape))    
        self.assertEqual([None,5] ,list(test.inputs[('in1',5)].shape))
        self.assertEqual([None,1] ,list(test.inputs[('in1',1)].shape))
        self.assertEqual([None,5] ,list(test.inputs[('in2',5)].shape))
        self.assertEqual([None,4] ,list(test.inputs[('in2',(2,2))].shape))

        in1 = [[0,1,2,3,4]]
        test_layer = Model(inputs=test.inputs_for_model['in1'], outputs=test.inputs[('in1',5)])
        self.assertEqual([[0,1,2,3,4]],test_layer.predict(in1).tolist())

        test_layer = Model(inputs=test.inputs_for_model['in1'], outputs=test.inputs[('in1',1)])
        self.assertEqual([[4]],test_layer.predict(in1).tolist())

        in2 = [[0,1,2,3,4,5,6]]
        test_layer = Model(inputs=test.inputs_for_model['in2'], outputs=test.inputs[('in2',5)])
        self.assertEqual([[0,1,2,3,4]],test_layer.predict(in2).tolist())

        test_layer = Model(inputs=test.inputs_for_model['in2'], outputs=test.inputs[('in2',(2,2))])
        self.assertEqual([[3,4,5,6]],test_layer.predict(in2).tolist())

    def test_network_building_complex2(self):
        input2 = Input('in2')
        output = Input('out')
        rel3 = Linear(input2.tw(0.05))
        rel4 = Linear(input2.tw([0.02,-0.02]))
        rel5 = Linear(input2.tw([0.03,-0.03]))
        fun = Output(output.z(-1),rel3+rel4+rel5)

        test = Neu4mes()
        test.addModel(fun)
        test.neuralizeModel(0.01)

        self.assertEqual(test.max_n_samples, 8) # 5 samples + 3 samples of the horizon
        self.assertEqual({'in2': 8} , test.input_n_samples)
        
        self.assertEqual([None,8] ,list(test.inputs_for_model['in2'].shape))
        self.assertEqual([None,None,8] ,list(test.inputs_for_rnn_model['in2'].shape))
        self.assertEqual([None,8] ,list(test.inputs['in2'].shape))    
        self.assertEqual([None,5] ,list(test.inputs[('in2',5)].shape))
        self.assertEqual([None,4] ,list(test.inputs[('in2',(2,2))].shape))
        self.assertEqual([None,6] ,list(test.inputs[('in2',(3,3))].shape))

        in2 = [[0,1,2,3,4,5,6,7]]
        test_layer = Model(inputs=test.inputs_for_model['in2'], outputs=test.inputs[('in2',5)])
        self.assertEqual([[0,1,2,3,4]],test_layer.predict(in2).tolist())

        test_layer = Model(inputs=test.inputs_for_model['in2'], outputs=test.inputs[('in2',(2,2))])
        self.assertEqual([[3,4,5,6]],test_layer.predict(in2).tolist())

        test_layer = Model(inputs=test.inputs_for_model['in2'], outputs=test.inputs[('in2',(3,3))])
        self.assertEqual([[2,3,4,5,6,7]],test_layer.predict(in2).tolist())

    def test_network_building_complex3(self):
        input2 = Input('in2')
        output = Input('out')
        rel3 = Linear(input2.tw(0.05))
        rel4 = Linear(input2.tw([0.01,-0.03]))
        rel5 = Linear(input2.tw([0.04,-0.01]))
        fun = Output(output.z(-1),rel3+rel4+rel5)

        test = Neu4mes()
        test.addModel(fun)
        test.neuralizeModel(0.01)

        self.assertEqual(test.max_n_samples, 8) # 5 samples + 3 samples of the horizon
        self.assertEqual({'in2': 8} , test.input_n_samples)
        
        self.assertEqual([None,8] ,list(test.inputs_for_model['in2'].shape))
        self.assertEqual([None,None,8] ,list(test.inputs_for_rnn_model['in2'].shape))
        self.assertEqual([None,8] ,list(test.inputs['in2'].shape))    
        self.assertEqual([None,5] ,list(test.inputs[('in2',5)].shape))
        self.assertEqual([None,4] ,list(test.inputs[('in2',(1,3))].shape))
        self.assertEqual([None,5] ,list(test.inputs[('in2',(4,1))].shape))

        in2 = [[0,1,2,3,4,5,6,7]]
        test_layer = Model(inputs=test.inputs_for_model['in2'], outputs=test.inputs[('in2',5)])
        self.assertEqual([[0,1,2,3,4]],test_layer.predict(in2).tolist())

        test_layer = Model(inputs=test.inputs_for_model['in2'], outputs=test.inputs[('in2',(1,3))])
        self.assertEqual([[4,5,6,7]],test_layer.predict(in2).tolist())

        test_layer = Model(inputs=test.inputs_for_model['in2'], outputs=test.inputs[('in2',(4,1))])
        self.assertEqual([[1,2,3,4,5]],test_layer.predict(in2).tolist())


