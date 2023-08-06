import json
import numpy as np
import os
import reconstruction as rct
from file_reader import roiread
import time

'''
    A colections of points Point() are correlated in a manner that creates
    a perimeter Perimeter(). Every perimeter should be nice, i.e.:
        1) Not self-intersecting;
        2) No overlaping points;
        3) Have a prefered orientation.
    If we can garantee this properties, than we proceed to stitch a colection
    of perimeters in a surface Surface().
'''
with open('main.json', 'r') as settings:
    data = settings.read()
Data = json.loads(data)
FileDir = Data["FileDir"]
OutputDir = Data["OutputDir"]

try:
    os.makedirs(OutputDir)
except:
    0
opt_par_list = ["Name","FileType","Thickness","Super Resolusition","Start"]
name = "NONAME"
filetype = "OSIRIXJSON"
thickness = 1
new_res = 0
start_points = {}
for opt in opt_par_list:
    if not opt in Data.keys():
        continue
    if opt=="Name":
        name = Data[opt]
    if opt=="FileType":
        filetype = Data[opt]
    if opt=="Thickness":
        thickness = float(Data[opt])
    if opt=="Super Resolusition":
        new_res = Data[opt]
    if opt=="Start":
        start_points = Data[opt][0]

print("Loading files\n\n")
print(FileDir)

def island_init(file_dir,f,subdivision=3):
    arq = roiread(file_dir+"/"+f,filetype,thickness)
    I = rct.Perimeter(arq,full_init=True)
    I.remove_overlap(delta=0.01)
    I.area_vec()
    #I.fix_distance(subdivision=1)
    return I

for block in Data["Stitches3D"]:
    for section in block:
        try:
            close_list = Data["CloseSurface"][0][str(section)]
        except:
            close_list = []
        S = rct.Surface()
        for file in block[section]:
            try:
                if isinstance(file,list):
                    I = 0
                    for f in file:
                        I_s = island_init(FileDir,f,3)
                        if I == 0:
                            I = I_s
                        else:
                            I.islands_ensemble(I_s)
                            #I.fix_distance(subdivision=1)
                else:
                    I = island_init(FileDir,file,3)
                I.area_vec()
                #I.fix_intersection()
                #I.points=np.flip(I.points)
                #I.area=-1*I.area
                S.add_island(I)
            except Exception:
                if isinstance(file,list):
                    print(f"Failed to load pack:{file}, single:{f}")
                else:
                    print(f"Failed to load:{file}")

        print("\nBuilding surface: ",section)
        S._intersection_range = 100
        S.super_resolution(parcelation=new_res,seed=1)
        for idx,c in enumerate(close_list):
            if not new_res:
                break
            if c:
                close_list[idx] = len(block[section])*2-3

        ##Starting points conditions
        if section in start_points.keys():
            start_pass = start_points[section]
        else:
            start_pass = {}

        S.estimate_geometric_values()
        print(f"Lateral Area estimation: {S.area_est:.2f}\nSlab Volume estimation: {S.vol_est:.2f}".replace(".",","))
        #continue
        S.build_surface(close_list,start_pass)

        ## Closing the bridges created by merge island algorithm
        try: #Data["CloseBifurcation"] doesnt allways have a section
            for file_index in Data["CloseBifurcation"][0][str(section)]:
                bif_list = block[section][file_index]
                S.closebif(file_index, bif_list)
        except:
            0
        ## Extra lids that might be needed
        ## So rare that dont even need to be optmized
        ## Leave as is
        try:
            S_extra = rct.Surface()
            for file_colection in Data["CloseExtra"][0][str(section)]:
                get = file_colection[0]
                for file_index in file_colection[1]:
                    contours = Data["Stitches3D"][0][str(section)][get][file_index]
                    S_extra.close_extra(island_init(FileDir,contours,3))
                    with open(OutputDir+"/Extra_"+name+"_"+section+"_"+str(file_index)+".obj", "w") as out_file:
                        out_file.write(S_extra.surfaceV_extra)
                        out_file.write(S_extra.surfaceE_extra)
        except:
            0
        with open(OutputDir+"/"+name+"_"+section+".obj", "w") as out_file:
            out_file.write(S.surfaceV)
            out_file.write(S.surfaceE)
        print(f"\nDone building: {section}")
time.process_time()
