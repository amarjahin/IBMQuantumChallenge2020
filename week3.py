import matplotlib.pyplot as plt
import numpy as np
from qiskit import QuantumCircuit, execute
from qiskit import IBMQ, Aer
from qiskit.tools.visualization import plot_histogram



def week3_ans_func(problem_set):
    
    ##### build your quantum circuit here
    ##### In addition, please make it a function that can solve the problem even with different inputs (problem_set). We do validation with different inputs. 
    # Convert str input to int
    for i in range(16):
        for j in range(6):
            problem_set[i][j][0] = int(problem_set[i][j][0])
            problem_set[i][j][1] = int(problem_set[i][j][1])
    # rearrange the boards to put one asteroid on the at the (0,0) and if possible the rest of the rwo is empty.
    for i in range(16):
        ast = [*range(6)]
        for j in ast:
            ast = [*range(6)]
            ast.remove(j)
            for k in ast:
                problem_set[i][k][0] = (problem_set[i][k][0] - problem_set[i][j][0]) % 4
                problem_set[i][k][1] = (problem_set[i][k][1] - problem_set[i][j][1]) % 4
            problem_set[i][j][0]=0
            problem_set[i][j][1]=0
            if np.count_nonzero(np.array(problem_set)[i,:,1] == 0) == 1:
                # print(f'success{i}')
                break

    # define quantum and classical registers
    qram_qr = [*range(4)]
    board_qr = [*range(4, 4+16)]
    oracle_qr = [4+16]
    ancillary_qr = [*range(4+16+1, 4+16+1+4)]
    cr = [*range(4)]

    qc = QuantumCircuit(len(qram_qr)+len(board_qr) + len(oracle_qr) + len(ancillary_qr), len(cr))
    qc.h(qram_qr)
    qc.x(oracle_qr[0])
    qc.barrier()
    #### Code for Grover's algorithm with iterations = 1 will be as follows. 
    for i in range(1):
        # oracle()
        for i in range(16): 
            pos = []
            i_bin = f"{i:04b}"
            # if the board number is something do
            for x in range(len(i_bin)):
                if i_bin[x] == '0':
                    qc.x(qram_qr[-x-1])
            # endoce the initial conditions 
            for coordinates in problem_set[i]: 
                pos.append(board_qr[4*coordinates[1] + coordinates[0]])
                
            for i in range(1,6,1):
                qc.cx(pos[0], pos[i])
            qc.mct(qram_qr, pos[0], ancillary_qr, mode='basic')
            for i in range(1,6,1):
                qc.cx(pos[0], pos[i])
                
            # restore board number
            for x in range(len(i_bin)):
                if i_bin[x] == '0':
                    qc.x(qram_qr[-x-1])
        qc.barrier()
        qc.h(oracle_qr[0])
        for x1 in [0]:
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
                        qc.mct([board_qr[4 + x2]] + [board_qr[2*4 + x3]] + [board_qr[3*4 + x4]], oracle_qr[0], ancillary_qr, mode='basic')
        qc.h(oracle_qr[0])
        qc.barrier()
        for i in range(16-1, -1, -1): 
            pos=[]
            i_bin = f"{i:04b}"
            # if the board number is something do
            for x in range(len(i_bin)-1, -1, -1):
                if i_bin[x] == '0':
                    qc.x(qram_qr[-x-1])
            # endoce the initial conditions 
            for coordinates in problem_set[i]: 
                pos.append(board_qr[4*coordinates[1] +coordinates[0]])
                
            for i in range(1,6,1):
                qc.cx(pos[0], pos[i])
            qc.mct(qram_qr, pos[0], ancillary_qr, mode='basic')
            for i in range(1,6,1):
                qc.cx(pos[0], pos[i])
                
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
        qc.mct(qram_qr[0:3], qram_qr[3], ancillary_qr, mode='basic')
        qc.h(qram_qr[3])
        qc.barrier()
        qc.x(qram_qr)
        qc.h(qram_qr)
        qc.barrier()

    qc.measure(qram_qr, cr)
    # qc = qc.reverse_bits()

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
