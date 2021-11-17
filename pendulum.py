from neu4mes import *

pendolo = Neu4mes()

theta = Input('theta')
T     = Input('torque')

lin_theta = Linear(theta.tw(1.5))
sin_theta = LinearBias(Sin(theta))
torque = Linear(T)

theta_z = Output(theta.z(-1), lin_theta+sin_theta+torque)

pendolo.addModel(theta_z)

pendolo.neuralizeModel(0.05)
pendolo.prova(np.array([1,1,2]))

data_struct = ['time','theta','theta_s','cos_theta','sin_theta','torque']
data_folder = './data/data-linear-oscillator-a/'
pendolo.loadData(data_struct, folder = data_folder)

pendolo.trainModel(validation_percentage = 30, show_results = True)