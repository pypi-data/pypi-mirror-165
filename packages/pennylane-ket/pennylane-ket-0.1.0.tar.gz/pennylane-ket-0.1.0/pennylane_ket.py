from pennylane import QubitDevice
from pennylane import numpy as np
from ket import base as libket


def _ctrl(p, c, t, gate, param=0.0):
    p.ctrl_push(*libket.from_list_to_c_vector(c))
    p.apply_gate(gate, param, t)
    p.ctrl_pop()


def _swap(p, a, b):
    _ctrl(p, [a], b, libket.PAULI_X)
    _ctrl(p, [b], a, libket.PAULI_X)
    _ctrl(p, [a], b, libket.PAULI_X)


def _cswap(p, c, a, b):
    p.ctrl_push(*libket.from_list_to_c_vector([c]))
    _ctrl(p, [a], b, libket.PAULI_X)
    _ctrl(p, [b], a, libket.PAULI_X)
    _ctrl(p, [a], b, libket.PAULI_X)
    p.ctrl_pop()


def _toffoli(p, c0, c1, t):
    p.ctrl_push(*libket.from_list_to_c_vector([c0, c1]))
    p.apply_gate(libket.PAULI_X, 0.0, t)
    p.ctrl_pop()


def _mcx(p, control_values, *qubits):
    *ctr, trg = qubits
    for c, q in zip(control_values, ctr):
        if c == '0':
            p.apply_gate(libket.PAULI_X, 0.0, q)
    p.ctrl_push(*libket.from_list_to_c_vector(ctr))

    p.apply_gate(libket.PAULI_X, 0.0, trg)

    p.ctrl_pop()
    for c, q in zip(control_values, ctr):
        if c == '0':
            p.apply_gate(libket.PAULI_X, 0.0, q)


def _rxx(p, theta, a, b):
    p.apply_gate(libket.HADAMARD, 0.0, a)
    p.apply_gate(libket.HADAMARD, 0.0, b)
    _ctrl(p, [a], b, libket.PAULI_X)
    p.apply_gate(libket.RZ, theta, b)
    _ctrl(p, [a], b, libket.PAULI_X)
    p.apply_gate(libket.HADAMARD, 0.0, b)
    p.apply_gate(libket.HADAMARD, 0.0, a)


def _rzz(p, theta, a, b):
    _ctrl(p, [a], b, libket.PAULI_X)
    p.apply_gate(libket.RZ, theta, b)
    _ctrl(p, [a], b, libket.PAULI_X)


def _ryy(p, theta, a, b):
    p.apply_gate(libket.RX, np.pi/2, a)
    p.apply_gate(libket.RX, np.pi/2, b)
    _ctrl(p, [a], b, libket.PAULI_X)
    p.apply_gate(libket.RZ, theta, b)
    _ctrl(p, [a], b, libket.PAULI_X)
    p.apply_gate(libket.RX, np.pi/2, b)
    p.apply_gate(libket.RX, np.pi/2, a)


KET_OPERATION_MAP = {
    'Identity': lambda p, q: None,
    'Hadamard': lambda p, q: p.apply_gate(libket.HADAMARD, 0.0, q),
    'PauliX': lambda p, q: p.apply_gate(libket.PAULI_X, 0.0, q),
    'PauliY': lambda p, q: p.apply_gate(libket.PAULI_Y, 0.0, q),
    'PauliZ': lambda p, q: p.apply_gate(libket.PAULI_Z, 0.0, q),
    'S': lambda p, q: p.apply_gate(libket.PHASE, np.pi/2, q),
    # SX
    'T': lambda p, q: p.apply_gate(libket.PHASE, np.pi/4, q),
    'CNOT': lambda p, c, t: _ctrl(p, [c], t, libket.PAULI_X),
    'CZ': lambda p, c, t: _ctrl(p, [c], t, libket.PAULI_Z),
    'CY': lambda p, c, t: _ctrl(p, [c], t, libket.PAULI_Y),
    'SWAP': _swap,
    # ISWAP
    # ECR
    # SISWAP
    # SQISW
    'CSWAP': _cswap,
    'Toffoli': _toffoli,
    'MultiControlledX': _mcx,
    # Barrier
    # WireCut
    # Rot
    'RX': lambda p, theta, q: p.apply_gate(libket.RX, theta, q),
    'RY': lambda p, theta, q: p.apply_gate(libket.RY, theta, q),
    'RZ': lambda p, theta, q: p.apply_gate(libket.RZ, theta, q),
    # MultiRZ
    # PauliRot
    'PhaseShift': lambda p, theta, q: p.apply_gate(libket.PHASE, theta, q),
    'ControlledPhaseShift': lambda p, theta, c, t: _ctrl(p, [c], t, libket.PHASE, theta),
    'CPhase': lambda p, theta, c, t: _ctrl(p, [c], t, libket.PHASE, theta),
    'CRX': lambda p, theta, c, t: _ctrl(p, [c], t, libket.RX, theta),
    'CRY': lambda p, theta, c, t: _ctrl(p, [c], t, libket.RY, theta),
    'CRZ': lambda p, theta, c, t: _ctrl(p, [c], t, libket.RZ, theta),
    # CRot
    'U1': lambda p, theta, q: p.apply_gate(libket.PHASE, theta, q),
    # U2
    # U3
    'IsingXX': _rxx,
    # IsingXY
    'IsingYY': _ryy,
    'IsingZZ': _rzz,
}


class KetDevice(QubitDevice):
    name = 'Ket PennyLane plugin'
    short_name = 'ket'
    pennylane_requires = ">=0.25.0"
    version = "0.1.0"
    author = 'Quantuloop'
    operations = KET_OPERATION_MAP.keys()
    observables = {
        'Identity',
        'PauliX',
        'PauliY',
        'PauliZ',
    }

    def __init__(self, wires=1, shots=None):
        super().__init__(wires=wires, shots=shots)
        self._probabilities = None
        self._process_count = 0

    def _apply(self, op):
        if op.name == 'MultiControlledX':
            _mcx(self._process,
                 op.control_values,
                 *[self._qubits[self.wire_map[i]] for i in op.wires])
        else:
            KET_OPERATION_MAP[op.name](
                self._process,
                *op.parameters,
                *[self._qubits[self.wire_map[i]] for i in op.wires]
            )

    def apply(self, operations, rotations=None):
        self._probabilities = None
        self._process = libket.process(self._process_count)
        self._process_count += 1
        self._qubits = [
            libket.qubit(self._process.allocate_qubit(False)) for _ in range(self.num_wires)
        ]
        for op in operations:
            if op.inverse:
                self._process.adj_begin()
                self._apply(op)
                self._process.adj_end()
            else:
                self._apply(op)

        if rotations:
            for op in rotations:
                if op.inverse:
                    self._process.adj_begin()
                    self._apply(op)
                    self._process.adj_end()
                else:
                    self._apply(op)

    def analytic_probability(self, wires=None):
        if self._probabilities is None:
            from ket.base import quantum_execution_target

            dump = libket.libket_dump(
                self._process.dump(
                    *libket.from_list_to_c_vector(self._qubits)
                )
            )

            self._process.prepare_for_execution()

            quantum_execution_target(self._process)

            self._probabilities = np.zeros(2**self.num_wires, dtype=float)

            size = dump.states_size().value
            real, _ = dump.amplitudes_real()
            imag, _ = dump.amplitudes_imag()
            for i in range(size):
                state, state_size = dump.state(i)
                index = int(''.join(f'{state[j]:064b}'
                                    for j in range(state_size.value)), 2)
                self._probabilities[index] = np.abs(real[i]+imag[i]*1j) ** 2

        return self.marginal_prob(self._probabilities, wires)
