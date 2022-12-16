# -*- coding: utf-8 -*-

import os
import sys
file_path = os.path.join(os.path.dirname(__file__), '..')
file_dir = os.path.dirname(os.path.realpath('__file__'))
sys.path.insert(0, os.path.abspath(file_path))
data_dir = file_dir + '\\Data\\'
ter_size = os.get_terminal_size()
clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')
install=lambda x : os.system( f"py -m pip install {x}")
try:
    ter_size=os.get_terminal_size()
    os.system(f"py -m pip list > {file_dir}/Docs/local_libs.txt") 
    libs={"prettytable", "pandas", "folium"}

    def install_reqs():
        with open(file_dir+"/Docs/local_libs.txt", "r", encoding="utf-8") as file:        
            file.readline()
            file.readline()
            words=set([i.split(" ")[0] for i in file])
            if len(libs & words) >= 0 and len(libs & words) < len(libs):
                for i in libs-words:
                    install(i) 
    install_reqs()
except Exception as err:
    print(err)