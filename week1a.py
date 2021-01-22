from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit import IBMQ, Aer, execute

qc = QuantumCircuit(5,2)

qc.x(0)
qc.x(2)



qc.cx(0,3)
qc.cx(1,3)
qc.cx(2,3)
qc.ccx(0,1,4)
qc.ccx(1,2,4)
qc.ccx(0,2,4)

qc.barrier()

qc.measure(3, 0)
qc.measure(4, 1)



print(qc.draw())


backend = Aer.get_backend('qasm_simulator')
job = execute(qc, backend, shots=1000)
result = job.result()
count =result.get_counts()
print(count)
# qc.draw(output='mpl')