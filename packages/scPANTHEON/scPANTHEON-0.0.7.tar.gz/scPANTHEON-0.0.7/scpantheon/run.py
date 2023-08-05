import os
 
command = "bokeh serve --show main.py" #command to be executed
 
res = os.system(command)
#the method returns the exit status
 
print("Returned Value: ", res)