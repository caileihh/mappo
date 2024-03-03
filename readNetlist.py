import os
import re

filename = 'netlist_3_27'


class MOSFET:
    def __init__(self, source, drain, gate, bulk, model, width, length, fingers):
        self.source = source
        self.drain = drain
        self.gate = gate
        self.bulk = bulk
        self.model = model
        self.width = width
        self.length = length
        self.fingers = fingers

    def get_source(self):
        return self.source

    def get_drain(self):
        return self.drain

    def get_gate(self):
        return self.gate

    def get_bulk(self):
        return self.bulk

    def get_model(self):
        return self.model

    def get_width(self):
        return self.width

    def get_length(self):
        return self.length

    def get_fingers(self):
        return self.fingers


def read_netlist(sp_name, pre_name, num_name):
    f = open(sp_name, 'r', encoding="utf-8")
    f1 = open('connect.txt', 'w', encoding="utf-8")
    mostfetList = []
    net_list = []
    line = f.readline()
    while line:
        a = re.split(" ", line.strip())
        if a[0].startswith('//') or a[0] == '' or a[0] == 'topckt' or a[0] == 'ends' or a[0] == 'subckt':
            line = f.readline()
            continue
        if a[len(a) - 1] == '\\':
            line = line + f.readline().strip()
            a = re.split(" ", line.strip())

        # if re.search(r'MM\d+', a[0]):
        #     mosfet = MOSFET(a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8].strip())
        #     mostfetList.append(mosfet)
        if a[0].startswith('C') or a[0].startswith('R'):
            for i in range(1, 3):
                a[i] = a[i].replace('(', '')
                a[i] = a[i].replace(')', '')
                if a[i] not in net_list:
                    net_list.append(a[i])
        else:
            print(a, len(a))
            for i in range(1, 4):
                a[i] = a[i].replace('(', '')
                a[i] = a[i].replace(')', '')
                if a[i] not in net_list:
                    net_list.append(a[i])
        line = f.readline()

    link_set = [[] for _ in range(len(net_list))]
    f.seek(0)
    line = f.readline()
    count = 0
    while line:
        a = re.split(" ", line.strip())
        if a[0] == '//' or a[0] == '' or a[0] == 'topckt' or a[0] == 'ends' or a[0].startswith('//') or a[
            0] == 'subckt':
            line = f.readline()
            continue
        if a[len(a) - 1] == '\\':
            line = line + f.readline().strip()
            a = re.split(" ", line.strip())

        # if re.search(r'MM\d+', a[0]):
        #     mosfet = MOSFET(a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8].strip())
        #     mostfetList.append(mosfet)
        now_name = pre_name + "_" + a[0]
        found_keys = [key for key, value in num_name.items() if value == now_name]

        if a[0].startswith('C') or a[0].startswith('R'):
            for i in range(1, 3):
                a[i] = a[i].replace('(', '')
                a[i] = a[i].replace(')', '')
                net_index = net_list.index(a[i])
                dictionary = [found_keys[0], i]
                link_set[net_index].append(dictionary)
        else:
            for i in range(1, 4):
                a[i] = a[i].replace('(', '')
                a[i] = a[i].replace(')', '')
                net_index = net_list.index(a[i])
                dictionary = [found_keys[0], i]
                link_set[net_index].append(dictionary)
        count += 1
        line = f.readline()
    # print(mostfetList[0].model)
    # for mosfet in mostfetList:
    print(net_list)
    print(link_set)
    for n, i in enumerate(link_set):
        f1.writelines('Link' + str(n + 1) + ':\n')
        for j in i:
            f1.writelines('M' + str(j[0]) + ' ')
        f1.writelines('\n')
        for j in i:
            f1.writelines(str(j[1]) + ' ')
        f1.writelines("\n")
    f.close()
    f1.close()


def read_hspice(sp_name, pre_name, num_name):
    # sp_name = 'ota1.sp'
    f = open(os.path.dirname(os.path.abspath(__file__))+"\\"+sp_name, 'r', encoding="utf-8")
    f1 = open(os.path.dirname(os.path.abspath(__file__))+"\\"+'connect.txt', 'w', encoding="utf-8")
    mostfetList = []
    net_list = []
    line = f.readline()
    while line:
        a = re.split(" ", line.strip())
        if a[0].startswith('//') or a[0] == '' or a[0] == 'topckt' or a[0] == 'ends' or a[0] == 'subckt' \
                or a[0].startswith('*') or a[0].startswith("."):
            line = f.readline()
            continue
        if a[len(a) - 1] == '\\':
            line = line + f.readline().strip()
            a = re.split(" ", line.strip())

        # if re.search(r'MM\d+', a[0]):
        #     mosfet = MOSFET(a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8].strip())
        #     mostfetList.append(mosfet)
        if a[0].startswith('C') or a[0].startswith('R'):
            for i in range(1, 3):
                a[i] = a[i].replace('(', '')
                a[i] = a[i].replace(')', '')
                if a[i] not in net_list:
                    net_list.append(a[i])
        else:
            print(a, len(a))
            for i in range(1, 4):
                a[i] = a[i].replace('(', '')
                a[i] = a[i].replace(')', '')
                if a[i] not in net_list:
                    net_list.append(a[i])
        line = f.readline()

    link_set = [[] for _ in range(len(net_list))]
    f.seek(0)
    line = f.readline()
    count = 0
    while line:
        a = re.split(" ", line.strip())
        if a[0] == '//' or a[0] == '' or a[0] == 'topckt' or a[0] == 'ends' or a[0].startswith('//') or a[0] == 'subckt'\
                or a[0].startswith('*') or a[0].startswith("."):
            line = f.readline()
            continue
        if a[len(a) - 1] == '\\':
            line = line + f.readline().strip()
            a = re.split(" ", line.strip())

        # if re.search(r'MM\d+', a[0]):
        #     mosfet = MOSFET(a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8].strip())
        #     mostfetList.append(mosfet)
        now_name = pre_name + "_" + a[0]
        found_keys = [key for key, value in num_name.items() if value == now_name]

        if a[0].startswith('C') or a[0].startswith('R'):
            for i in range(1, 3):
                a[i] = a[i].replace('(', '')
                a[i] = a[i].replace(')', '')
                net_index = net_list.index(a[i])
                dictionary = [found_keys[0], i]
                link_set[net_index].append(dictionary)
        else:
            for i in range(1, 4):
                a[i] = a[i].replace('(', '')
                a[i] = a[i].replace(')', '')
                net_index = net_list.index(a[i])
                dictionary = [found_keys[0], i]
                link_set[net_index].append(dictionary)
        count += 1
        line = f.readline()
    # print(mostfetList[0].model)
    # for mosfet in mostfetList:
    print(net_list)
    print(link_set)
    for n, i in enumerate(link_set):
        f1.writelines('Link' + str(n + 1) + ':\n')
        for j in i:
            f1.writelines('M' + str(j[0]) + ' ')
        f1.writelines('\n')
        for j in i:
            f1.writelines(str(j[1]) + ' ')
        f1.writelines("\n")
    f.close()
    f1.close()


def read_sym(sym_name):
    f = open(os.path.dirname(os.path.abspath(__file__))+"\\"+sym_name, 'r', encoding="utf-8")
    sym_list = {}
    line = f.readline()
    while line:
        if line == '':
            line = f.readline()
            continue
        a = re.split(" ", line.strip())
        if len(a) == 2:
            sym_list[a[0]] = a[1]
        elif len(a) == 1:
            sym_list[a[0]] = 'self_symmetry'
        line = f.readline()
    return sym_list


def read_gds():
    gds_name = 'Core_test_flow_M0.gds'
    print()


pre_name = "COMPARATOR_PRE_AMP_2018_Modify_test_flow" ################################


def main():
    import gdstkProcess
    num_name = gdstkProcess.main()
    read_hspice("comp.sp", pre_name, num_name) ###################################
    return read_sym(pre_name + ".sym")
    # read_gds()


if __name__ == '__main__':
    print(main())
