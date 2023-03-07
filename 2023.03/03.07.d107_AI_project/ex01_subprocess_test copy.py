import os 
import subprocess as sp

root_path = "./2023.03/03.07.d107_AI_project"
exe_name = "sample_dashboard.pbix"

program = os.path.join(root_path, exe_name)
 
# program_name = "notepad.exe"
program_name = "C:/Program Files/Microsoft Power BI Desktop/bin/PBIDesktop.exe"

sp.Popen([program_name])