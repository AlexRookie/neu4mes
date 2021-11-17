from neu4mes import *
import pprint

#Vehicle example
model_def = {
    'SampleTime':0.05,
    'Input':{
        'gear':{
            'Distrete':[1,2,3,4,5,6,7,8]
        },
        'engine':{},
        'brake':{},
        'altitude':{},
        'velocity':{}
    },
    'State':{
        'omega':{}
    },
    'Output':{
        'acceleration':{}
    },
    'Relations':{
        'gravity_force':{
            'Linear':[('altitide',1)]
        },
        'motor_force':{
            'LocalModel':[('engine',1.25),'gear']
        },
        'lin_brake':{
            'Linear':[('brake',1.25)],
        },
        'relu_brake':{
            'Relu':['lin_brake'],
        },
        'brake_force':{
            'Minus':['relu_brake'],
        },
        'omega':{
            'Prova':['velocity']
        },
        'acceleration': {
            'Sum':['gravity_force','motor_force','brake_force'],
            'Square':['velocity']
        }
    }
}
#Create the motor trasmission
gear = Input('gear', values=[1,2,3,4,5,6,7,8])

my_relation = lambda tw: Linear(brake.tw(tw))

engine = Input('engine')
motor_force = LocalModel(engine.tw(2), gear)

#Create the concept of the slope
altitude = Input('altitude')
gravity_force = Linear(altitude.tw(2))

#Create the brake force contribution
brake = Input('brake')
brake_force = my_relation(2)+Linear(brake.tw(0.4))+Linear(brake.tw(0.4)) #-Relu(Linear(brake.tw(1.25)))

#Create the areodinamic drag contribution
velocity = Input('velocity')
drag_force = Linear(velocity)+my_relation(0.5)

#The state is a well established variable, so if it used inside two different outputs
#will not be duplicated.
# omega = State('omega',brake_force+drag_force)
#    'States':{
#        'omega':{}
#    },
#   'Relations:{
#       'omega':{
#           'Linear':[brake_force,drag_force]
#       }
#   }
#The State can be added in the back propagation schema is needed.
# omega = Input('omega') 
# omega_estimator = State('omega', brake_force+drag_force, out = omega.z(-1))
    # 'States':{
    #     'omega':{}
    # },
    # 'Outputs':{
    #     'omega':{}
    # },
# lat_acc = Input('lat_acc')
# lat_acc_estimator = Output(lat_acc.z(1), omega+drag_force+gravity_force+motor_force)

#Longitudinal acceleration
long_acc = Input('accleration')

#Definition of the next acceleration predict 

vai = brake_force+drag_force#+brake_force
long_acc_estimator = Output(long_acc.z(-1), vai)
#pprint.pprint(long_acc_estimator.json)
# long_acc_estimator = Output(long_acc.z(-1), motor_force+gravity_force+brake_force)
long_acc_estimator2 = Output(altitude.z(-1), drag_force+gravity_force+brake_force)
# pprint.pprint(long_acc_estimator2.json)

#pprint.pprint(long_acc_estimator.json)
#pprint.pprint(long_acc_estimator2.json)

mymodel = Neu4mes()
mymodel.addModel(long_acc_estimator)
# pprint.pprint(mymodel.model_def)
mymodel.addModel(long_acc_estimator2)
pprint.pprint(mymodel.model_def)
mymodel.neuralizeModel(0.05)
pprint.pprint(mymodel.model_used)
# nn = Neu4mes()
# nn.addModel(mymodel.model_used)
# nn.neuralizeModel(0.05)
# pprint.pprint(nn.model_used)

data_struct = ['time','altitude','brake','accleration','velocity','gear']
data_folder = './data/data-linear-oscillator-a/'
mymodel.loadData(data_struct, folder = data_folder)
mymodel.trainModel(validation_percentage = 30)

#definisco che long_acc è l'integrale di velocity
# long_acc.s(-1) = velocity 
#sono uguali 
# velocity.s(1) = long_acc
#così dico che voglio mettere degli stati per fare il training ricorrente
# mymodel.trainModel(validation_percentage = 30, states = [long_acc_estimator])

#data_struct = ['time','velocity','accleration','engine','gear','altitude','brake']
#data_folder = './data/vehicle_data/'
#mymodel.loadData(data_struct, folder = data_folder)
#mymodel.trainModel(validation_percentage = 30)