import matplotlib.pyplot as plt
import numpy as np
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, execute
from qiskit import IBMQ, Aer
from qiskit.tools.visualization import plot_histogram

backend = Aer.get_backend('qasm_simulator')

def solve_board_qc(lights, solution):
    light_qr = [*range(solution, solution + lights)]
    solution_qr = [*range(solution)]

    oracle = [lights + solution]
    qc = QuantumCircuit(lights + 1 + solution, name='solver')
    qc.h(solution_qr) 

    qc.barrier()
    for x in range(17):
        # Apply oracle 
        # Apply solution to lights 
        for j in range(3):
            for i in range(3):
                k =  i + 3*j
                ku = i + 3*(j-1)
                kd = i + 3*(j+1)
                kl = i - 1 + 3*(j)
                kr = i + 1 + 3*(j)

                qc.cx(k,len(light_qr) + k)

                if ku >= 0 : 
                    qc.cx(k,len(light_qr) + ku)

                if kd <= 8 : 
                    qc.cx(k,len(light_qr) + kd)

                if kl >= 3*j and kl < 3*(j+1): 
                    qc.cx(k,len(light_qr) + kl)

                if kr >= 3*j and kr < 3*(j+1): 
                    qc.cx(k,len(light_qr) + kr)
        
        qc.barrier()
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

                qc.cx(k,len(light_qr) + k)

                if ku >= 0 : 
                    qc.cx(k,len(light_qr) + ku)

                if kd <= 8 : 
                    qc.cx(k,len(light_qr) + kd)

                if kl >= 3*j and kl < 3*(j+1): 
                    qc.cx(k,len(light_qr) + kl)

                if kr >= 3*j and kr < 3*(j+1): 
                    qc.cx(k,len(light_qr) + kr)

        

        # Apply dispersion 
        qc.h(solution_qr)
        qc.x(solution_qr)
        qc.barrier()
        qc.h(solution_qr[len(light_qr) - 1])
        qc.mcx(solution_qr[0:len(light_qr) - 1], solution_qr[len(light_qr) - 1] )
        qc.h(solution_qr[len(light_qr) - 1])
        qc.barrier()
        qc.x(solution_qr)
        qc.h(solution_qr)
        qc.barrier()
    return qc

def inv_solve_board_qc(lights, solution):
    light_qr = [*range(solution, solution + lights)]
    solution_qr = [*range(solution)]

    oracle = [lights + solution]
    qc = QuantumCircuit(lights + 1 + solution, name='inv_solver')
    for x in range(17):
        # Apply dispersion 
        qc.h(solution_qr)
        qc.x(solution_qr)
        qc.barrier()
        qc.h(solution_qr[len(light_qr) - 1])
        qc.mcx(solution_qr[0:len(light_qr) - 1], solution_qr[len(light_qr) - 1] )
        qc.h(solution_qr[len(light_qr) - 1])
        qc.barrier()
        qc.x(solution_qr)
        qc.h(solution_qr)
        qc.barrier()

        # Apply oracle 
        # Apply solution to lights 
        for j in range(3):
            for i in range(3):
                k =  i + 3*j
                ku = i + 3*(j-1)
                kd = i + 3*(j+1)
                kl = i - 1 + 3*(j)
                kr = i + 1 + 3*(j)

                qc.cx(k,len(light_qr) + k)

                if ku >= 0 : 
                    qc.cx(k,len(light_qr) + ku)

                if kd <= 8 : 
                    qc.cx(k,len(light_qr) + kd)

                if kl >= 3*j and kl < 3*(j+1): 
                    qc.cx(k,len(light_qr) + kl)

                if kr >= 3*j and kr < 3*(j+1): 
                    qc.cx(k,len(light_qr) + kr)
        
        qc.barrier()
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

                qc.cx(k,len(light_qr) + k)

                if ku >= 0 : 
                    qc.cx(k,len(light_qr) + ku)

                if kd <= 8 : 
                    qc.cx(k,len(light_qr) + kd)

                if kl >= 3*j and kl < 3*(j+1): 
                    qc.cx(k,len(light_qr) + kl)

                if kr >= 3*j and kr < 3*(j+1): 
                    qc.cx(k,len(light_qr) + kr)

    qc.h(solution_qr) 
    return qc



def week2b_ans_func(lightsout4):
    num_of_boards = int(np.shape(lightsout4)[0])
    num_of_boards_bits = int(np.ceil(np.log2(num_of_boards)))
    num_of_lights = int(np.shape(lightsout4)[1])
    num_of_lights_bits = int(np.ceil(np.log2(num_of_lights)))

    board_num_qr = [*range(num_of_boards_bits)]
    solution_qr = [*range(num_of_boards_bits, num_of_lights + num_of_boards_bits ) ]
    light_qr = [*range(num_of_lights + num_of_boards_bits, num_of_lights + num_of_boards_bits + num_of_lights)]
    num_switches_qr = [*range(num_of_lights + num_of_boards_bits + num_of_lights, num_of_lights + num_of_boards_bits + num_of_lights + num_of_lights_bits)]
    oracle = [num_of_lights + num_of_boards_bits + num_of_lights + num_of_lights_bits]

    cr =   [*range(num_of_boards_bits)]
    # cr =   [*range(9)]
    # cr_s = [*range(9, 9+4)]


    qc = QuantumCircuit(len(board_num_qr) + len(solution_qr) + len(light_qr) + len(num_switches_qr) + len(oracle), len(cr) )
    qc.x(oracle[0])
    # superimpose all boards
    qc.h(board_num_qr)
    qc.barrier()

    for x in range(1):
        # translate boards num in qRAM to actual boards config
        for i in range(num_of_boards):
            i_bin = f"{i:02b}"
            # if the board number is something do
            for x in range(len(i_bin)):
                if i_bin[x] == '0':
                    qc.x(board_num_qr[-x-1])
            # endoce the initial conditions 
            for l_n in range(num_of_lights): 
                if lightsout4[i][l_n] == 1:
                    qc.mcx(board_num_qr, light_qr[l_n])
            # restore board number
            for x in range(len(i_bin)):
                if i_bin[x] == '0':
                    qc.x(board_num_qr[-x-1])
            qc.barrier()
        qc.append(solve_board_qc(lights=num_of_lights, solution=num_of_lights), qargs=solution_qr+light_qr+oracle)
        # Add num of switches
        for i in range(num_of_lights): 
            qc.mcx([solution_qr[i]] + num_switches_qr[0:3], num_switches_qr[3])
            qc.mcx([solution_qr[i]] + num_switches_qr[0:2], num_switches_qr[2])
            qc.mcx([solution_qr[i]] + num_switches_qr[0:1], num_switches_qr[1])
            qc.cx(solution_qr[i], num_switches_qr[0])

        # Apply oracle
        qc.barrier()
        qc.x(num_switches_qr[2:4])
        qc.h(oracle)
        qc.mcx(num_switches_qr, oracle)
        qc.h(oracle)
        qc.x(num_switches_qr[2:4])

        qc.x(num_switches_qr[2:4]+num_switches_qr[0:1])
        qc.h(oracle)
        qc.mcx(num_switches_qr, oracle)
        qc.h(oracle)
        qc.x(num_switches_qr[2:4]+num_switches_qr[0:1])

        qc.x(num_switches_qr[1:4])
        qc.h(oracle)
        qc.mcx(num_switches_qr, oracle)
        qc.h(oracle)
        qc.x(num_switches_qr[1:4])

        qc.x(num_switches_qr)
        qc.h(oracle)
        qc.mcx(num_switches_qr, oracle)
        qc.h(oracle)
        qc.x(num_switches_qr)
        qc.barrier()

        # reverse add switch
        for i in range(num_of_lights): 
            qc.cx(solution_qr[-i-1], num_switches_qr[0])
            qc.mcx([solution_qr[-i-1]] + num_switches_qr[0:1], num_switches_qr[1])
            qc.mcx([solution_qr[-i-1]] + num_switches_qr[0:2], num_switches_qr[2])
            qc.mcx([solution_qr[-i-1]] + num_switches_qr[0:3], num_switches_qr[3])
        qc.barrier()

        qc.append(inv_solve_board_qc(lights=num_of_lights, solution=num_of_lights), qargs=solution_qr+light_qr+oracle)

        for i in range(num_of_boards-1, -1, -1):
            i_bin = f"{i:02b}"
            # if the board number is something do
            for x in range(len(i_bin)-1, -1, -1):
                if i_bin[x] == '0':
                    qc.x(board_num_qr[-x-1])
            # endoce the initial conditions 
            for l_n in range(num_of_lights-1, -1, -1): 
                if lightsout4[i][l_n] == 1:
                    qc.mcx(board_num_qr, light_qr[l_n])
            # restore board number
            for x in range(len(i_bin)-1, -1, -1):
                if i_bin[x] == '0':
                    qc.x(board_num_qr[-x-1])
            qc.barrier()
        # Apply dispersion
        qc.h(board_num_qr)
        qc.x(board_num_qr)
        qc.barrier()
        qc.h(board_num_qr[num_of_boards_bits - 1])
        qc.mcx(board_num_qr[0:num_of_boards_bits - 1], board_num_qr[num_of_boards_bits - 1] )
        qc.h(board_num_qr[num_of_boards_bits - 1])
        qc.barrier()
        qc.x(board_num_qr)
        qc.h(board_num_qr)
        qc.barrier()


    # qc.measure(solution_qr, cr)
    # qc.measure(num_switches_qr, cr_s)

    qc.measure(board_num_qr, cr)
    # qc.measure_all()
    return qc


# sample problems and answers for week-2B
# problem_name = [[board0], [board1],[board2],[board3],'answer']
#Pushes Q1:[1,4,5,6], Q2[5,6,2,4], Q3:[6,5,4,3]
Q1 = [[0,0,0, 0,0,1, 0,1,1], [0,1,0, 1,0,1, 0,1,0], [0,1,1, 1,0,1, 0,1,0], [1,1,1, 0,1,0, 1,1,0]]
Q2 = [[1,0,1, 1,0,1, 0,0,1], [0,1,0, 0,0,1, 1,1,1], [0,1,1, 1,0,0, 1,0,0],[1,0,0, 1,0,0, 1,0,0]]
Q3 = [[0,0,0, 0,1,1, 0,0,1], [0,1,0, 1,1,0, 0,0,0], [0,1,1, 1,0,0, 0,0,1], [1,0,0, 0,0,0, 1,0,1]]
lightsout4=[[1, 1, 1, 0, 0, 0, 1, 0, 0],[1, 0, 1, 0, 0, 0, 1, 1, 0],[1, 0, 1, 1, 1, 1, 0, 0, 1],[1, 0, 0, 0, 0, 0, 1, 0, 0]]
# lightsout4=[[1, 1, 1, 0, 0, 0, 1, 0, 0],[0, 1, 0, 1, 1, 1, 0, 1, 0],[1, 0, 1, 1, 1, 1, 0, 0, 1],[1, 0, 0, 0, 0, 0, 1, 0, 0]]


qc = week2b_ans_func(Q3)

print(qc.draw())
job = execute(qc, backend=backend, shots=1000, seed_simulator=12345, backend_options={"fusion_enable":True})
result = job.result()
count = result.get_counts()
# print(count)
plot_histogram(count)
plt.show()


# 110110111 ok
# 001110000 ok
# 100011111 ok
# 011000011 ok