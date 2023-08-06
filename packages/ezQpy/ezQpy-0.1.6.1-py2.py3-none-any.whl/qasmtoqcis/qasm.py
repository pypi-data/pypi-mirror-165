import os
import json
import re
import random
from const import Const


class BaseUtil():
    def __init__(self, qasm, qubit_list):
        self.qasm2qcis = self.json_file()
        self.single_gate = self.qasm2qcis.get('single_gate')
        self.couper_gate = self.qasm2qcis.get('couper_gate')
        self.qasm = qasm
        self.qubit_list = qubit_list

    def json_file(self):
        self.const = Const()
        return self.const.qasm2qcis

    def find_qubit_by_qasm(self):
        qubit_idx = re.findall(r'q\[(\d+)\]', self.qasm)
        # print('qasm:', self.qasm)
        # print('qubit_list:', self.qubit_list)
        # print('qubit_idx:', qubit_idx)
        qubit_idx = [self.qubit_list[int(idx)] for idx in qubit_idx]
        return qubit_idx

    def find_param_by_qasm(self):
        """qasm门操作的参数, 比如：
           rx(0) q[0]; 找到括号中的内容['0']
           u(0.124, 0.562. -0.86) q[0]; 找到括号中的内容['0.124, 0.562. -0.86']

        Returns:
            list: 返回查找到的内容
        """
        param_result = re.findall(r'\((.*)\)', self.qasm)
        return param_result

    def find_param_index_by_qasm(self, single_qasm):
        """根据json中转换后的qcis,找到填参数索引的数据
           比如：
           RZ [1];找到对应的['1']
           RZ [1] [2];找到对应的['1', '2']

        Args:
            single_qasm (str): 单条json中转换的qcis

        Returns:
            list: 返回查找到的内容
        """
        param_index = re.findall(r'\[(\d+)\]', single_qasm)
        return param_index

    def find_after_param_gate(self, coupler_qasm):
        gate_result = re.findall(r'(.+(?=\())', coupler_qasm)
        return gate_result

    def check_gate(self, class_name):
        if class_name in self.single_gate:
            return True
        else:
            return False

    def __str__(self):
        qcis = ''
        class_name = self.__class__.__name__
        check_result = self.check_gate(class_name)
        param_result = self.find_param_by_qasm()
        if len(param_result) > 0:
            param_result = param_result[0].split(',')
            param_result = [str(eval(param.strip())) for param in param_result]
        if check_result:
            qcis_gate = self.single_gate.get(class_name)
            qubit_idx = self.find_qubit_by_qasm()
            if class_name == 'barrier':
                if not qubit_idx:
                    qubit_idx = ' '.join([f'Q{i}' for i in self.qubit_list])
                else:
                    qubit_idx = ' '.join([f'Q{i}' for i in qubit_idx])
                qcis += f'''B {qubit_idx}\n'''
            elif isinstance(qcis_gate, str):
                param_index = self.find_param_index_by_qasm(qcis_gate)
                if len(param_index) > 0:
                    gate = qcis_gate.split(' ')[0]
                    qcis += f'{gate} Q{qubit_idx[0]} ' +\
                            f'{param_result[int(param_index[0])]}\n'
                else:
                    qcis += f'{qcis_gate} Q{qubit_idx[0]}\n'
            elif isinstance(qcis_gate, dict):
                new_qcis = qcis_gate.get(random.sample(qcis_gate.keys(), 1)[0])
                for q in new_qcis:
                    qcis += f'{q} Q{qubit_idx[0]}\n'
            elif isinstance(qcis_gate, list):
                for q in qcis_gate:
                    param_index = self.find_param_index_by_qasm(q)
                    if len(param_index) > 0:
                        gate = q.split(' ')[0]
                        qcis += f'{gate} Q{qubit_idx[0]} ' +\
                                f'{param_result[int(param_index[0])]}\n'
                    else:
                        qcis += f'{q} Q{qubit_idx[0]}\n'
        else:
            qcis_gate = self.couper_gate.get(class_name)
            qubit_idx = self.find_qubit_by_qasm()
            coupler_list = [f'Q{idx}' for idx in qubit_idx]
            for q in qcis_gate:
                if isinstance(q, str):
                    param_index = self.find_param_index_by_qasm(q)
                    if len(param_index) > 0:
                        q_index = q.split(' ')[1]
                        gate = q.split(' ')[0]
                        for param in param_index:
                            q = q.replace(
                                f'[{param}]', param_result[int(param)])
                        qcis_param = q.split(' ')[2]
                        qcis += f'{gate} Q{qubit_idx[int(q_index)]} ' +\
                                f'{eval(qcis_param)}\n'
                    else:
                        gate = q.split(' ')[:1]
                        idx = q.split(' ')[1:]
                        for i in idx:
                            gate.append(coupler_list[int(i)])
                        gate = ' '.join(gate)
                        qcis += f'{gate}\n'
                elif isinstance(q, dict):
                    if 'single_gate' in q:
                        qcis_gate = q.get('single_gate')
                    else:
                        qcis_gate = q.get('couper_gate')
                    param_index = self.find_param_index_by_qasm(qcis_gate)
                    if len(param_index) > 0:
                        gate = qcis_gate.split(' ')[0]
                        for param in param_index:
                            qcis_gate = qcis_gate.replace(
                                f'[{param}]', param_result[int(param)])
                        q_gate = re.findall(r'([a-z]+)', qcis_gate)[0]
                    else:
                        q_gate = qcis_gate.split(' ')[0]
                    gate = qcis_gate.split(' ')[:1]

                    idx_list = re.findall(r'q\[\d+\]', self.qasm)
                    idx = qcis_gate.split(' ')[1:]
                    for i in idx:
                        gate.append(idx_list[int(i)])
                    gate = ' '.join(gate)
                    g = globals().get(q_gate)(gate, self.qubit_list)
                    qcis += str(g)
        return qcis


class measure(BaseUtil):
    def __str__(self):
        qubit_idx = self.find_qubit_by_qasm()
        qcis = f'M Q{qubit_idx[0]}\n'
        return qcis


def create_instruction_class(name, load_to_scope=False):
    cls = type(name, (BaseUtil,), {})
    if load_to_scope:
        scope = globals()
        if name not in scope:
            scope[name] = cls
    return cls


def load_qasm_classes():
    qcis_instructions = [
        'x', 'y', 'z', 'h', 'sx', 'sxdg', 'h_sx_h', 'h_sxdg_h',
        's', 'sdg', 't', 'tdg', 'rx', 'ry', 'rz', 'u', 'u2', 'u1',
        'cx', 'cz', 'cy', 'ch', 'swap', 'crz', 'cp', 'ccx', 'cu3', 'barrier']

    class_list = []
    for name in qcis_instructions:
        cls = create_instruction_class(name)
        class_list.append(cls)
    return class_list, qcis_instructions


(x, y, z, h, sx, sxdg,
 h_sx_h, h_sxdg_h,
 s, sdg, t, tdg,
 rx, ry, rz, u, u2, u1,
 cx, cz, cy, ch,
 swap, crz, cp, ccx, cu3, barrier), _QCIS_INSTRUCTIONS = load_qasm_classes()


# x1  = x('x q[0];', [1, 2, 3])
# print('x:\n', x1)

# y1  = y('y q[0];', [1, 2, 3])
# print('y:\n', y1)

# z1  = z('z q[0];', [1, 2, 3])
# print('z:\n', z1)

# h1 = h('h q[1]', [1, 2, 3])
# print('h:\n', h1)

# sx1 = sx('sx q[2]', [1, 2, 3, 4])
# print('sx:\n', sx1)

# sx1 = sxdg('sxdg q[2]', [1, 2, 3, 4])
# print('sxdg:\n', sx1)

# sx1 = h_sx_h('h q[2]\nsx q[2]\nh q[2]', [1, 2, 3, 4])
# print('h_sx_h:\n', sx1)

# sx1 = h_sxdg_h('h q[2]\nsxdg q[2]\nh q[2]', [1, 2, 3, 4])
# print('h_sxdg_h:\n', sx1)

# sx1 = s('s q[3]', [1, 2, 3, 4])
# print('s:\n', sx1)

# sx1 = sdg('sdg q[3]', [1, 2, 3, 4])
# print('sdg:\n', sx1)

# sx1 = t('t q[3]', [1, 2, 3, 4])
# print('t:\n', sx1)

# sx1 = tdg('tdg q[3]', [1, 2, 3, 4])
# print('tdg:\n', sx1)

# sx1 = rx('rx(-0.8734873) q[3]', [1, 2, 3, 4])
# print('rx:\n', sx1)

# sx1 = ry('ry(3.452154) q[3]', [1, 2, 3, 4])
# print('ry:\n', sx1)

# sx1 = rz('rz(1.2546) q[3]', [1, 2, 3, 4])
# print('rz:\n', sx1)

# sx1 = u('u(0.12343, -0.31323245, 0.8786834) q[3]', [1, 2, 3, 4])
# print('u:\n', sx1)

# sx1 = u2('u2(0.5624, -0.12334) q[3]', [1, 2, 3, 4])
# print('u2:\n', sx1)

# sx1 = u1('u1 q[3]', [1, 2, 3, 4])
# print('u1:\n', sx1)

# cx1 = cx('cx q[0] q[1]', [1, 2, 3, 4])
# print('cx:\n', cx1)

# cz1 = cz('cz q[0] q[1]', [1, 2, 3, 4])
# print('cz:\n', cz1)

# cy1 = cy('cy q[1] q[2]', [1, 2, 3, 4])
# print('cy:\n', cy1)

# ch1 = ch('ch q[1] q[2]', [1, 2, 3, 4])  # Q2 Q3
# print('ch:\n', ch1)

# swap1 = swap('swap1 q[1] q[2]', [1, 2, 3, 4])
# print('swap:\n', swap1)

# crz1 = crz('crz(2.343) q[1],q[2] ;', [1, 2, 3, 4])
# print('crz:\n', crz1)

# cp1 = cp('cp(3.01234) q[1],q[2];', [1, 2, 3, 4])
# print('cp:\n', cp1)

# ccx1 = ccx('ccx q[1],q[2],q[3];', [1, 2, 3, 4])
# print('ccx:\n', ccx1)

# cu31 = cu3('cu3(3.01234, 0.25, 1.8456) q[1],q[2];', [1, 2, 3, 4])
# print('cu3:\n', cu31)

# measure1 = measure('measure q[0] -> c[0];', [1, 2, 3, 4])
# print('measure:\n', measure1)

# measure1 = measure('measure q[1] -> c[1];', [1, 2, 3, 4])
# print('measure:\n', measure1)
# print(globals())

# barrier1 = barrier('barrier q;', [1, 2, 3, 4, 5])
# print('barrier1:\n', barrier1)
