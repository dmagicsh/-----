# -*- coding: utf-8 -*-
# UTF-8 编码格式
# 引用GUI模块
import sys
from PyQt5 import uic
from PyQt5.QtGui import QScreen
from PyQt5.QtWidgets import QApplication
from PyQt5.uic import loadUi


class Window:
    def __init__(self):
        super(Window, self).__init__()
        # 加载UI文件
        self.model = None
        ui_file = r"ui\端口整合工具.ui"
        # 从UI定义中动态创建一个相应的窗口对象
        self.ui = uic.loadUi(ui_file)
        if not self.ui:
            print(loadUi().errorString())
            sys.exit(-1)
        self.center()
        # 信号处理
        self.ui.btn_check.clicked.connect(self.check)

    # 窗口居中
    def center(self):
        # Get Screen geometry
        src_size = QScreen.availableGeometry(QApplication.primaryScreen())
        # Set X Position Center
        frm_x = int((src_size.width() - self.ui.width()) / 2)
        # Set Y Position Center
        frm_y = int((src_size.height() - self.ui.height()) / 2)
        # Set Form's Center Location
        self.ui.move(frm_x, frm_y)

    def check(self):
        source_list = list(set(self.ui.s_port_list.toPlainText().split("\n")))
        print("source_list: ", source_list, "\nType(source_list): ", type(source_list))
        k = []
        ks = []
        for i in range(0, len(source_list)):
            try:
                k.append(int(source_list[i]))
            except Exception:
                ks.append(source_list[i])
        while "" in ks:
            ks.remove("")
        tmp_ks = []
        # 将范围转为list
        for item in ks:
            be_item = item.split('-')
            tmp_item = list(range(int(be_item[0]), int(be_item[1])+1, 1))
            tmp_ks.extend(tmp_item)
        k.extend(tmp_ks)
        tmp_k = sorted(set(k))
        mg_l = mg_str_lst(split_num_l(tmp_k))
        while "" in mg_l:
            mg_l.remove("")
        output_list = sorted(mg_l)
        output_str = '\n'.join(output_list)
        print('output_str=\n', output_str)
        self.ui.r_port_list.setPlainText(output_str)


def split_num_l(num_lst):
    """merge successive num, sort lst(ascending or descending): 'as' or 'des'
    eg: [1, 3,4,5,6, 9,10] -> [[1], [3, 4, 5, 6], [9, 10]]
    """
    num_lst_tmp = [int(n) for n in num_lst]
    sort_lst = sorted(num_lst_tmp)  # ascending
    len_lst = len(sort_lst)
    i = 0
    split_lst = []

    tmp_lst = [sort_lst[i]]
    while True:
        if i + 1 == len_lst:
            break
        next_n = sort_lst[i + 1]
        if sort_lst[i] + 1 == next_n:
            tmp_lst.append(next_n)
        else:
            split_lst.append(tmp_lst)
            tmp_lst = [next_n]
        i += 1
    split_lst.append(tmp_lst)
    return split_lst


def mg_str_lst(my_lst):
    """[[1], [3, 4, 5, 6], [9, 10]] -> ['1', '3-6', '9-10']
    """
    mg_l = []
    for num_l in my_lst:
        if len(num_l) == 1:
            mg_l.append(str(num_l[0]))
        else:
            mg_l.append(str(num_l[0]) + '-' + str(num_l[-1]))
    return mg_l


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.ui.show()
    sys.exit(app.exec())
