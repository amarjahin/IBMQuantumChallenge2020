import matplotlib.pyplot as plt
import numpy as np
from qiskit import QuantumCircuit, execute
from qiskit import IBMQ, Aer
from qiskit.tools.visualization import plot_histogram

def week3_ans_func(problem_set):
    ##### build your quantum circuit here
    ##### In addition, please make it a function that can solve the problem even with different inputs (problem_set). We do validation with different inputs. 
    qram_qr = [*range(4)]
    board_qr = [*range(4, 4+16)]
    oracle_qr = [4+16]
    cr = [*range(4)]
    qc = QuantumCircuit(len(qram_qr)+len(board_qr) + len(oracle_qr), len(cr))
    qc.h(qram_qr)
    qc.x(oracle_qr[0])
    qc.barrier()
    #### Code for Grover's algorithm with iterations = 1 will be as follows. 


    for i in range(1):
        # oracle()
        for i in range(16): 
            i_bin = f"{i:04b}"
            # if the board number is something do
            for x in range(len(i_bin)):
                if i_bin[x] == '0':
                    qc.x(qram_qr[-x-1])
            # endoce the initial conditions 
            for coordinates in problem_set[i]: 
                pos = 4*int(coordinates[1]) +int(coordinates[0])
                qc.mcx(qram_qr, board_qr[pos])
            # restore board number
            for x in range(len(i_bin)):
                if i_bin[x] == '0':
                    qc.x(qram_qr[-x-1])
        qc.barrier()
        for x1 in range(4):
            x_list = [0,1,2,3]
            x_list.remove(x1)
            for x2 in x_list:
                x_list = [0,1,2,3]
                x_list.remove(x1)
                x_list.remove(x2)
                for x3 in x_list:
                    x_list = [0,1,2,3]
                    x_list.remove(x1)
                    x_list.remove(x2)
                    x_list.remove(x3)
                    for x4 in x_list:
                        qc.h(oracle_qr[0])
                        qc.mcx([board_qr[x1]] + [board_qr[4 + x2]] + [board_qr[2*4 + x3]] + [board_qr[3*4 + x4]], oracle_qr[0])
                        qc.h(oracle_qr[0])
        qc.barrier()
        for i in range(16-1, -1, -1): 
            i_bin = f"{i:04b}"
            # if the board number is something do
            for x in range(len(i_bin)-1, -1, -1):
                if i_bin[x] == '0':
                    qc.x(qram_qr[-x-1])
            # endoce the initial conditions 
            for coordinates in problem_set[i]: 
                pos = 4*int(coordinates[1]) +int(coordinates[0])
                qc.mcx(qram_qr, board_qr[pos])
            # restore board number
            for x in range(len(i_bin)-1 , -1, -1):
                if i_bin[x] == '0':
                    qc.x(qram_qr[-x-1])
        qc.barrier()
        # diffusion()   
        qc.h(qram_qr)
        qc.x(qram_qr)
        qc.barrier()
        qc.h(qram_qr[3])
        qc.mcx(qram_qr[0:3], qram_qr[3] )
        qc.h(qram_qr[3])
        qc.barrier()
        qc.x(qram_qr)
        qc.h(qram_qr)
        qc.barrier()
    

    qc.measure(qram_qr, cr)
    return qc

problem_set = \
    [[['0', '2'], ['1', '0'], ['1', '2'], ['1', '3'], ['2', '0'], ['3', '3']],
    [['0', '0'], ['0', '1'], ['1', '2'], ['2', '2'], ['3', '0'], ['3', '3']],
    [['0', '0'], ['1', '1'], ['1', '3'], ['2', '0'], ['3', '2'], ['3', '3']],
    [['0', '0'], ['0', '1'], ['1', '1'], ['1', '3'], ['3', '2'], ['3', '3']],
    [['0', '2'], ['1', '0'], ['1', '3'], ['2', '0'], ['3', '2'], ['3', '3']],
    [['1', '1'], ['1', '2'], ['2', '0'], ['2', '1'], ['3', '1'], ['3', '3']],
    [['0', '2'], ['0', '3'], ['1', '2'], ['2', '0'], ['2', '1'], ['3', '3']],
    [['0', '0'], ['0', '3'], ['1', '2'], ['2', '2'], ['2', '3'], ['3', '0']],
    [['0', '3'], ['1', '1'], ['1', '2'], ['2', '0'], ['2', '1'], ['3', '3']],
    [['0', '0'], ['0', '1'], ['1', '3'], ['2', '1'], ['2', '3'], ['3', '0']],
    [['0', '1'], ['0', '3'], ['1', '2'], ['1', '3'], ['2', '0'], ['3', '2']],
    [['0', '0'], ['1', '3'], ['2', '0'], ['2', '1'], ['2', '3'], ['3', '1']],
    [['0', '1'], ['0', '2'], ['1', '0'], ['1', '2'], ['2', '2'], ['2', '3']],
    [['0', '3'], ['1', '0'], ['1', '3'], ['2', '1'], ['2', '2'], ['3', '0']],
    [['0', '2'], ['0', '3'], ['1', '2'], ['2', '3'], ['3', '0'], ['3', '1']],
    [['0', '1'], ['1', '0'], ['1', '2'], ['2', '2'], ['3', '0'], ['3', '1']]]



qc = week3_ans_func(problem_set)

print(qc.draw())
backend = Aer.get_backend('qasm_simulator')
job = execute(qc, backend=backend, shots=1000, seed_simulator=12345, backend_options={"fusion_enable":True})
result = job.result()
count = result.get_counts()
# print(count)
plot_histogram(count)
plt.show()



