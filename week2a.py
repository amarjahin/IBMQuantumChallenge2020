import matplotlib.pyplot as plt
import numpy as np
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, execute
from qiskit import IBMQ, Aer
from qiskit.tools.visualization import plot_histogram

backend = Aer.get_backend('qasm_simulator')

def week2a_ans_func(lights):
    light_qr = [*range(len(lights), len(lights)+len(lights))]
    solution = [*range(len(lights))]
    oracle = [len(lights) + len(lights)]
    cr =   [*range(9)]
    qc = QuantumCircuit(len(light_qr) + len(oracle)+ len(solution), len(cr))
    qc.x(oracle[0])
    # endoce the initial conditions 
    for i in range(9): 
        if lights[i] == 1: 
            qc.x(light_qr[i])

    # Checking all possible solutions
    qc.barrier()
    qc.h(solution) 
    qc.barrier()

    qc.barrier()
    for x in range(22):
        # Apply oracle 
        # Apply solution to lights 
        for j in range(3):
            for i in range(3): 
                k =  i + 3*j
                ku = i + 3*(j-1)
                kd = i + 3*(j+1)
                kl = i - 1 + 3*(j)
                kr = i + 1 + 3*(j)

                qc.cx(k,len(lights) + k)

                if ku >= 0 : 
                    qc.cx(k,len(lights) + ku)

                if kd <= 8 : 
                    qc.cx(k,len(lights) + kd)

                if kl >= 3*j and kl < 3*(j+1): 
                    qc.cx(k,len(lights) + kl)

                if kr >= 3*j and kr < 3*(j+1): 
                    qc.cx(k,len(lights) + kr)
        
        qc.x(light_qr)
        qc.h(oracle[0])
        qc.mcx(light_qr, oracle)
        qc.h(oracle[0])
        qc.x(light_qr)
        qc.barrier()
        
        # restore lights 
        for j in range(3):
            for i in range(3): 
                k =  i + 3*j
                ku = i + 3*(j-1)
                kd = i + 3*(j+1)
                kl = i - 1 + 3*(j)
                kr = i + 1 + 3*(j)

                qc.cx(k,len(lights) + k)

                if ku >= 0 : 
                    qc.cx(k,len(lights) + ku)

                if kd <= 8 : 
                    qc.cx(k,len(lights) + kd)

                if kl >= 3*j and kl < 3*(j+1): 
                    qc.cx(k,len(lights) + kl)

                if kr >= 3*j and kr < 3*(j+1): 
                    qc.cx(k,len(lights) + kr)


        # Apply dispersion 
        qc.h(solution)
        qc.x(solution)
        qc.barrier()
        qc.h(solution[len(lights) - 1])
        qc.mcx(solution[0:len(lights) - 1], solution[len(lights) - 1] )
        qc.h(solution[len(lights) - 1])
        qc.barrier()
        qc.x(solution)
        qc.h(solution)
        qc.barrier()

    qc.measure(solution, cr)

    qc = qc.reverse_bits()
    # print(qc.draw())
    return qc

lights = [0, 1, 1, 1, 0, 0, 1, 1, 1]
lightsout4=[[1, 1, 1, 0, 0, 0, 1, 0, 0],[1, 0, 1, 0, 0, 0, 1, 1, 0],[1, 0, 1, 1, 1, 1, 0, 0, 1],[1, 0, 0, 0, 0, 0, 1, 0, 0]]

qc = week2a_ans_func(lightsout4[1])

job = execute(qc, backend=backend, shots=1000, seed_simulator=12345, backend_options={"fusion_enable":True})
result = job.result()
count = result.get_counts()

print(count)
# plot_histogram(count)
# plt.show()