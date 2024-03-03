# Load a GDSII file into a new library.
import re

import gdspy
import gdstk
import pathlib
import os
import numpy
from matplotlib import pyplot as plt

# from readFloorplan import rotate
# import pcell
import readNetlist

filename = 'floorplan_test(3).gds'


def readinitJson():
    jsonname = 'gdsData(4).json'
    path = pathlib.Path(__file__).parent.absolute()

    # Check library units. In this case it is using the default units.
    units = gdstk.gds_units(path / filename)
    print(f"Using unit = {units[0]}, precision = {units[1]}")
    for i in units:
        print(i)

    # Load the library as a dictionary of RawCell
    pdk = gdstk.read_rawcells(path / filename)

    # Cell holding a single device (MZI)
    dev_cell = gdstk.Cell("Device")
    with open(jsonname, 'r', encoding="utf-8") as f:
        target_char = '        "MM'  # 目标字符
        line = f.readline()
        while line:
            if target_char in line:
                b = re.findall(r'-?\d+\.?\d*', line)
                ModuleNum = b
                for i in range(3):
                    line = f.readline().strip()
                X = int(line.replace(",", ''))
                line = f.readline().strip()
                Y = int(line.replace(",", ''))
                print(X, Y)
                for i in range(4):
                    line = f.readline().strip()
                b = re.findall(r'-?\d+\.?\d*', line)
                print(b)
                print(ModuleNum)
                if len(b) != 0:
                    dev_cell.add(gdstk.Reference(pdk["MM" + ModuleNum[0]], (int(X), int(Y)),
                                                 rotation=float(b[0]) / 180 * numpy.pi))
                else:
                    dev_cell.add(gdstk.Reference(pdk["MM" + ModuleNum[0]], (int(X), int(Y))))

            line = f.readline()
    f.close()
    main = gdstk.Cell("Main")
    main.add(
        # gdstk.Reference(dev_cell, (250, 250)),
        gdstk.Reference(dev_cell, (0, 0))
    )
    lib = gdstk.Library(unit=1e-9)
    lib.add(main, *main.dependencies(True))
    lib.write_gds(path / "layout.gds")


def read():
    path = pathlib.Path(__file__).parent.absolute()

    # Check library units. In this case it is using the default units.
    units = gdstk.gds_units(path / filename)
    print(f"Using unit = {units[0]}, precision = {units[1]}")

    # Load the library as a dictionary of RawCell
    pdk = gdstk.read_rawcells(path / filename)

    # Cell holding a single device (MZI)
    dev_cell = gdstk.Cell("Device")
    dev_cell.add(gdstk.Reference(pdk["MM1"], (3800, 50100)))
    dev_cell.add(gdstk.Reference(pdk["MM2"], (36600, 0)))

    # Main cell with 2 devices and lithography alignment marks
    main = gdstk.Cell("Main")
    main.add(
        # gdstk.Reference(dev_cell, (250, 250)),
        gdstk.Reference(dev_cell, (0, 0))
    )
    lib = gdstk.Library(unit=1e-9)
    lib.add(main, *main.dependencies(True))
    lib.write_gds(path / "layout.gds")


def read_gds2(all_port, rate, num, f, gds_path):
    cell_name = [gds_path.replace(".gds", "")]  # 要处理的单元格的名称
    units = gdstk.gds_units("gds/" + gds_path)
    # # 读取GDS文件
    library = gdstk.read_gds("gds/" + gds_path, unit=1e-9)
    # 查找要修改位置的单元格
    cell = None
    maxx = -1e10
    maxy = -1e10
    minx = 1e10
    miny = 1e10
    port = []
    for i, lib_cell in enumerate(library.cells):
        cell = lib_cell
        new_cell = cell
        # 修改单元格中的元件位置
        if cell_name[0].startswith(readNetlist.pre_name+"_R"):
            bounding_box = cell.bounding_box()
            minx = min(bounding_box[0][0], minx)
            miny = min(bounding_box[0][1], miny)
            maxx = max(bounding_box[1][0], maxx)
            maxy = max(bounding_box[1][1], maxy)
        else:
            # if '33e2r' in new_cell.name:
            #     bounding_box = cell.bounding_box()
            #     minx = min(bounding_box[0][0], minx)
            #     miny = min(bounding_box[0][1], miny)
            #     maxx = max(bounding_box[1][0], maxx)
            #     maxy = max(bounding_box[1][1], maxy)
            if new_cell.name == 'toplevel':
                ref_cell_top = cell
                ref_002 = ref_cell_top.references[0]

                origin_002 = ref_002.origin
                rotation_002 = ref_002.rotation
                ref_cell_top002 = ref_002.cell
                # ref_cell_top002.name = cell.name + ref_cell_top002.name
                ref_list = []
                for ref in ref_cell_top002.references:
                    t_cell = ref.cell
                    if '33e2r' in t_cell.name:
                        bounding_box = cell.bounding_box()
                        minx = min(bounding_box[0][0], minx)
                        miny = min(bounding_box[0][1], miny)
                        maxx = max(bounding_box[1][0], maxx)
                        maxy = max(bounding_box[1][1], maxy)
                        # minx += ref.origin[0]
                        # maxx += ref.origin[0]
                        # miny += ref.origin[1]
                        # maxy += ref.origin[1]

                    # t_cell.name = cell.name + t_cell.name
                    # cell_reference = gdspy.CellReference(t_cell, ref.origin, ref.rotation)
                    # ref_list.append(cell_reference)
                # ref_cell_top002.references = []
                # ref_cell_top002.references = ref_list
                # ref_cell_top.references[0] = gdspy.CellReference(ref_cell_top002, origin_002, rotation_002)

        if new_cell.name == "toplevel002":
            for ref in new_cell.references:
                # print(ref.cell_name)
                if ref.cell_name.startswith("M2_M1"):
                    bounding = ref.bounding_box()
                    port1 = []
                    port1.append((bounding[0][0], bounding[0][1]))
                    port1.append((bounding[0][0], bounding[1][1]))
                    port1.append((bounding[1][0], bounding[1][1]))
                    port1.append((bounding[1][0], bounding[0][1]))
                    port.append(port1)

        if cell_name[0].startswith(readNetlist.pre_name+"_R"):
            if new_cell.name == "toplevel":
                for ref in new_cell.references:
                    if ref.cell_name.startswith("M2_M1"):
                        bounding = ref.bounding_box()
                        port1 = []
                        port1.append((bounding[0][0], bounding[0][1]))
                        port1.append((bounding[0][0], bounding[1][1]))
                        port1.append((bounding[1][0], bounding[1][1]))
                        port1.append((bounding[1][0], bounding[0][1]))
                        port.append(port1)

        if i == len(library.cells)-1:
            f.writelines("Module:M" + str(num + 1) + '\n')
            f.writelines("Boundary:(" + str(minx / rate) + ', ' + str(miny / rate) + ')'
                         + "(" + str(minx / rate) + ', ' + str(maxy / rate) + ')'
                         + "(" + str(maxx / rate) + ', ' + str(maxy / rate) + ')'
                         + "(" + str(maxx / rate) + ', ' + str(miny / rate) + ');GATE\n')
            # port = all_port[cell_name]
            for number, po in enumerate(port):
                f.writelines("Port:")
                for p in po:
                    f.writelines("(" + str(float(p[0]) / rate) + ", " + str(float(p[1]) / rate) + ")")
                if number % 2 == 0:
                    f.writelines(";SD\n")
                else:
                    f.writelines(";GATE\n")
            # 提取边界框的宽度和高度
            # width = bounding_box[2] - bounding_box[0]
            # height = bounding_box[3] - bounding_box[1]
            for reference in cell.references:
                # 这里示例简单地将元件位置移动了(10, 10)个单位
                new_reference = reference.copy()
                new_reference.origin = (reference.origin[0] + 10, reference.origin[1] + 10)
                new_cell.add(new_reference)
            # 创建一个新的Library来存储修改后的单元格
            new_library = gdstk.Library()
            new_library.add(new_cell)


def read_gds(all_port, rate, num, f, gds_path):
    cell_name = [gds_path.replace(".gds", "")]  # 要处理的单元格的名称
    units = gdstk.gds_units("gds/" + gds_path)
    # # 读取GDS文件
    library = gdstk.read_gds("gds/" + gds_path, unit=1e-9)
    # 查找要修改位置的单元格
    cell = None
    for lib_cell in library.cells:
        if lib_cell.name in cell_name:
            cell = lib_cell
            break
    if cell is not None:
        new_cell = cell
        # 修改单元格中的元件位置
        bounding_box = cell.bounding_box()
        f.writelines("Module:M" + str(num + 1) + '\n')
        f.writelines("Boundary:(" + str(bounding_box[0][0] / rate) + ', ' + str(bounding_box[0][1] / rate) + ')'
                     + "(" + str(bounding_box[0][0] / rate) + ', ' + str(bounding_box[1][1] / rate) + ')'
                     + "(" + str(bounding_box[1][0] / rate) + ', ' + str(bounding_box[1][1] / rate) + ')'
                     + "(" + str(bounding_box[1][0] / rate) + ', ' + str(bounding_box[0][1] / rate) + ');GATE\n')
        if all_port[cell.name] is not None:
            print(cell_name, True)
        else:
            print(False)
        port = all_port[cell.name]
        for number, po in enumerate(port):
            f.writelines("Port:")
            for p in po:
                f.writelines("(" + str(float(p[0]) / rate) + ", " + str(float(p[1]) / rate) + ")")
            if number % 2 == 0:
                f.writelines(";SD\n")
            else:
                f.writelines(";GATE\n")
        for reference in cell.references:
            # 这里示例简单地将元件位置移动了(10, 10)个单位
            new_reference = reference.copy()
            new_reference.origin = (reference.origin[0] + 10, reference.origin[1] + 10)
            new_cell.add(new_reference)
        # 创建一个新的Library来存储修改后的单元格
        new_library = gdstk.Library()
        new_library.add(new_cell)
    else:
        print("未找到指定名称的单元格:", cell_name)


def read_file():
    # 指定文件夹路径
    folder_path = './gds'

    # 使用os.listdir()列出文件夹下的所有文件和子文件夹
    file_list = os.listdir(folder_path)

    # 过滤出文件，排除子文件夹
    file_names = [file for file in file_list if os.path.isfile(os.path.join(folder_path, file))]

    return file_names


def read_pin():
    f1 = open(readNetlist.pre_name+'.pin', 'r', encoding="utf-8")
    f1.readline()
    line = f1.readline()
    all_port = {}
    while line:
        a = re.split(" ", line.strip())
        if a[0] == '-1':
            line = f1.readline()
            continue

        module_name = a[0]

        port_set = []
        for i in range(int(a[1])):
            line = f1.readline()
            a = re.split(" ", line.strip())
            if a[0] == '-1':
                continue
            port_list = []
            port_list.append((a[0], a[1]))
            port_list.append((a[0], a[3]))
            port_list.append((a[2], a[3]))
            port_list.append((a[2], a[1]))
            port_set.append(port_list)
        all_port[module_name] = port_set
        line = f1.readline()
    print(all_port)
    return all_port

def write_gdspy(num_name, ModuleResult):
    import gdspy
    import ParticleTest_SYM
    layout = gdspy.GdsLibrary()
    ParticleTest_SYM.initialize()
    ParticleTest_SYM.read_and_init(ModuleResult)
    num_origin = []
    rotate_list = []
    f = open("Module_Origin_Cord.txt", 'r', encoding='utf-8')
    line = f.readline()
    while line:
        a = re.split(' ', line)
        num_origin.append((a[0], a[1]))
        rotate_list.append(a[2])
        line = f.readline()
    print(num_name)
    file_names = read_file()
    new_cell = gdspy.Cell('NewCell')
    for n, file_name in enumerate(file_names):
        cell_name = file_name.replace(".gds", '')
        print(file_name)
        num1 = [key1 for key1, value in num_name.items() if value == cell_name]
        layout.read_gds("gds/" + file_name)
        existing_cell = layout.cells[cell_name]
        x_offset, y_offset = float(num_origin[int(num1[0])-1][0])*rate/1000, float(num_origin[int(num1[0])-1][1])*rate/1000
        rotate_angel = rotate_list[int(num1[0]) - 1].strip()
        rotate_angel = re.findall(r'-?\d+\.?\d*', rotate_angel)
        if rotate_angel:
            print(rotate_angel)
            rotate_angel = int(rotate_angel[0])
        else:
            rotate_angel = 0
        existing_cell_reference = gdspy.CellReference(existing_cell, (x_offset, y_offset), rotate_angel)
        new_cell.add(existing_cell_reference)
    layout.add(new_cell)
    layout.write_gds('layout.gds')

def write_gdspy2(num_name, ModuleResult):
    import gdspy
    import ParticleTest_SYM
    layout = gdspy.GdsLibrary()
    layout1 = gdspy.GdsLibrary()
    ParticleTest_SYM.initialize()
    ParticleTest_SYM.read_and_init(ModuleResult)
    num_origin = []
    rotate_list = []
    f = open("Module_Origin_Cord.txt", 'r', encoding='utf-8')
    line = f.readline()
    while line:
        a = re.split(' ', line)
        num_origin.append((a[0], a[1]))
        rotate_list.append(a[2])
        line = f.readline()
    print(num_name)
    file_names = read_file()
    new_cell = gdspy.Cell('NewCell')
    main_cell = gdspy.Cell("main")
    cell_dict = {}
    ref_list = []
    for n, file_name in enumerate(file_names):
        cell_name = file_name.replace(".gds", '')
        print(file_name)
        num1 = [key1 for key1, value in num_name.items() if value == cell_name]
        # new_cell = gdspy.Cell(cell_name)  # 创建一个新的单元格
        # layout.add(new_cell)  # 将新单元格添加到布局中
        layout1 = gdspy.GdsLibrary()
        layout1.read_gds("gds/" + file_name)

        x_offset, y_offset = float(num_origin[int(num1[0])-1][0])*rate/1000, float(num_origin[int(num1[0])-1][1])*rate/1000
        rotate_angel = rotate_list[int(num1[0]) - 1].strip()
        rotate_angel = re.findall(r'-?\d+\.?\d*', rotate_angel)
        if rotate_angel:
            rotate_angel = int(rotate_angel[0])
        else:
            rotate_angel = 0
        # mid_cell = gdspy.Cell(cell_name)
        subcell_references = []
        big_cell = gdspy.Cell('bigcell'+"_"+cell_name)
        for ref_name in layout1.cells:
            # if ref_name == 'toplevel' or ref_name == 'toplevel002':
            #     continue

            if ref_name == 'toplevel':
                cell = layout1.cells[ref_name]
                cell.name = cell_name + "_" + ref_name
                rename_sub_cell(cell, cell_name, ref_name)
                big_cell.add(gdspy.CellReference(cell, (x_offset, y_offset), rotate_angel))
            else:
                continue
            cell = layout1.cells[ref_name]
            cell.name = cell_name + "_" + ref_name
            # big_cell.add(cell)
            if cell_name in cell_dict:
                existing_cell = cell_dict[cell_name]
            else:
                existing_cell = gdspy.Cell(cell_name)
                cell_dict[cell_name] = existing_cell

            # existing_cell_reference = gdspy.CellReference(cell, (x_offset, y_offset), rotate_angel)
            # subcell_references.append(gdspy.CellReference(cell))
            # ref_list.append(existing_cell_reference)
            # new_cell.add(existing_cell_reference)

            # mid_cell.add(new_cell)
        integrated_cell = gdspy.Cell(cell_name+'_new')
        for subcell_reference in subcell_references:
            integrated_cell.add(subcell_reference)
        # main_cell.add(gdspy.CellReference(integrated_cell, (x_offset, y_offset), rotate_angel))
        main_cell.add(big_cell)

    test_cell = gdspy.Cell('test')
    test_cell.add(ref_list)
    # layout.add(test_cell)
    layout.add(main_cell)
    layout.write_gds('layout.gds')


def rename_sub_cell(cell, name_prefix, ref_name):
    if isinstance(cell, gdspy.Cell):
        cell.name = cell.name + name_prefix
    # if hasattr(cell, 'references'):
    #     for sub_cell in cell.references:
    #         rename_sub_cell(sub_cell, name_prefix, ref_name)
    if ref_name == 'toplevel':
        ref_cell_top = cell
        ref_002 = ref_cell_top.references[0]
        origin_002 = ref_002.origin
        rotation_002 = ref_002.rotation
        ref_cell_top002 = ref_002.ref_cell
        ref_cell_top002.name = cell.name + ref_cell_top002.name
        ref_list = []
        for ref in ref_cell_top002.references:
            t_cell = ref.ref_cell
            t_cell.name = cell.name + t_cell.name
            cell_reference = gdspy.CellReference(t_cell, ref.origin, ref.rotation)
            ref_list.append(cell_reference)
        ref_cell_top002.references = []
        ref_cell_top002.references = ref_list
        ref_cell_top.references[0] = gdspy.CellReference(ref_cell_top002, origin_002, rotation_002)





def add_cell_with_references(layout, file_name, cell_name, x_offset, y_offset, rotate_angle):
    new_cell = gdspy.Cell(cell_name)
    layout.add(new_cell)
    layout.read_gds("gds/" + file_name)

    def add_reference(existing_cell, offset, rotation):
        for ref in existing_cell.references:
            ref_name = ref.ref_cell.name
            new_ref_name = f"{cell_name}_{ref_name}"
            new_ref = gdspy.CellReference(ref.ref_cell, offset=ref.origin + offset, rotation=ref.rotation + rotation, magnification=ref.magnification)
            new_cell.add(new_ref)
            add_reference(ref.ref_cell, offset, rotation)  # 递归处理嵌套references

    add_reference(new_cell, (x_offset, y_offset), rotate_angle)

rate = 20   # 40


def main():
    # firstprogram()
    # read()

    # readinitJson()
    # import readNetlist

    # readNetlist.read_hspice('ota1.sp', "Core_test_flow", num_name=)
    file_names = read_file()
    f1 = open('ModuleGDS.txt', 'w', encoding="utf-8")
    f1.writelines("Area:(0, 0)(850.5, 0)(850.5, 901.02)(0, 901.02)\n")
    f1.writelines("Rule:GATE(5,5);SD(5,5);GATE_SD(0.5);GATE_ITO(0.5);SD_ITO(0.5)\n")

    all_port = read_pin()
    num_name = {}
    for n, file_name in enumerate(file_names):
        print(file_name)
        num_name[n+1] = file_name.replace(".gds", '')
        read_gds(all_port, rate, n, f1, file_name)   #中大readgds2()  magical_readgds()
    print(num_name)
    return num_name


if __name__ == '__main__':
    write_gdspy(main(), ModuleResult='ModuleResult2.txt')
