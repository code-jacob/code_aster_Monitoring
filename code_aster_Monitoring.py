"""
Created on Sun Jan  7 14:43:53 2024
Author: Jakub Trušina
Name: code_aster_Monitoring.py
"""
import os
import subprocess
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import re
import shutil

# =============================================================================
# Ploting Force Convergence, Time Steps and Probe Monitoring
# =============================================================================
plt.close("all")
move_figure = 1 ;   mode_c = 1
def code_aster_monitoring(directory,file_name,file_number,open_file,application,file_auto,message_file,probe_position,print_files,mode,Unit,Language):
    
    if Language == "EN":
        current_step_name = 'Time of computation:'
    if Language == "FR":
        current_step_name = 'Instant de calcul:'
    
    global move_figure
    global mode_c       
    # print(mode_c, mode)
    if mode != mode_c:
        plt.close("all")
        mode_c = mode
        move_figure = 1
    
    found_paths = message_file
    if file_auto == 1:
        found_paths = [[]]
        for root, dirs, files in os.walk(directory):
            if file_name in files:
                full_path = os.path.join(root, file_name)
                found_paths.append(os.path.abspath(full_path))
                print(len(found_paths)-2,full_path)
        print()
        print(found_paths)
        message_file = found_paths[file_number+1]
        # print(message_file)
    else: file_number = 0 
    print(f"Message File: {found_paths.index(message_file)-1}\n", message_file )
    
    if open_file == 1:
        subprocess.Popen([application, message_file ])
    shutil.copy(message_file, "./code_aster_Monitoring_Data/message_file.txt" )
    
    pattern = r'[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?'
    swap_1 = 0 ; swap_2 = 0 ; contact = "NO" ; friction = "NO" ; line_search = "NO" ; end_ok = 0
    RESIDU_RELATIF_probe_position = 1
    RESI_GLOB_RELA = 1e-06
    with open(message_file, 'r', encoding='utf8') as file:
        for line in file:
            if "RESI_GLOB_RELA=" in line:
                RESI_GLOB_RELA_text = ( re.findall(pattern, line))
                RESI_GLOB_RELA = float(RESI_GLOB_RELA_text[0])
                print("RESI_GLOB_RELA =", str("%.1e"%(RESI_GLOB_RELA)))        
            if "Exécution du" in line:
                print(line.strip())
            if "DEFORMATION='" in line:
                index = line.find('DEFORMATION=') + len('DEFORMATION=')
                print("DEFORMATION = ",line[index:].strip())
            if "degrés de liberté:" in line:
                dof_text = ( re.findall(pattern, line))
                dof =  str("%.6e"%int(dof_text[0]))
                print("Degrees of Freedom =", (dof)) 
            if "noeuds du maillage" in line:
                nodes_text = ( re.findall(pattern, line))
                nodes = str("%.6e"%int(nodes_text[0]))
                print("Nodes =", (nodes)) 
            if "RECH.  LINE." in line:
                line_search = "YES"
                swap_2 = RESIDU_RELATIF_probe_position+2
                swap_1 = -1            
            if "* TOTAL_JOB" in line:
                TOTAL_JOB_text = ( re.findall(pattern, line))
                TOTAL_JOB = float(TOTAL_JOB_text[3]) 
                print("TOTAL JOB =", TOTAL_JOB, "s") 
                print("TOTAL JOB =", str("%.0f"%np.floor(TOTAL_JOB / 3600)) ,"hr", str("%.0f"%np.floor((TOTAL_JOB % 3600)/60)), "min", str("%.2f"%((((TOTAL_JOB % 3600)%60)))), "s" )    
            if "Temps CPU consommé dans le calcul" in line:
                index = line.find('Temps CPU consommé dans le calcul') + len('Temps CPU consommé dans le calcul')
                print("\nSolution Time" + line[index:].strip())
                end_ok = 1
            if "FIN D'EXECUTION LE" in line:
                print(line.strip())           
            if 'CRIT. GEOM.' in line:
                contact = "YES"
            if 'BCL. GEOM.' in line:
                contact = "YES"
                RESIDU_RELATIF_probe_position = 2 # contact
                swap_2 = RESIDU_RELATIF_probe_position+4
            if "CRIT. FROT." in line:
                friction = "YES"
                swap_2 = RESIDU_RELATIF_probe_position+5
                swap_1 = -1
    # print(RESIDU_RELATIF_probe_position)
    print("Contact =", contact)
    print("Friction =", friction)
    print("Line Search =", line_search , "\nUsing the line search with strains GROT_GDEP for COQUE_3D and in the presence of contact is not recommended.")
    if contact == "YES" and line_search == "YES":
        print("It is not recomended to use line search with contact")
    RESIDU_ABSOLU_probe_position = RESIDU_RELATIF_probe_position+1
    
    keywords_to_include = [ 'X |' , '|                |' , '|ELASTIQUE', '|TANGENTE', '|SECANTE' , current_step_name ]
    keywords_to_exclude = [ 'E |              X |' , '| RESI_GLOB_MAXI |' ]
    # keywords_to_exclude = [ '| RESI_GLOB_MAXI |' ]
    filtered_lines = []
    with open(message_file, 'r', encoding='utf8') as file:
        for line in file:
            if any(keyword in line for keyword in keywords_to_include) and not any(exclude_keyword in line for exclude_keyword in keywords_to_exclude):
                filtered_lines.append(line.strip())
    df_Lines = pd.DataFrame({'Filtered Lines': filtered_lines})
    # df_Lines.to_csv("Filtered Lines.txt",header=False, index=False)
    
    indices = df_Lines.index[df_Lines['Filtered Lines'].str.contains(current_step_name)].tolist()
    indices = np.delete(indices - np.arange(len(indices)) - np.ones(len(indices)), 0).astype(int) 
    # print("indices = ", indices)
    
    keywords_to_include.remove(current_step_name)
    filtered_lines = []
    with open(message_file, 'r', encoding='utf8') as file:
        for line in file:
            if any(keyword in line for keyword in keywords_to_include) and not any(exclude_keyword in line for exclude_keyword in keywords_to_exclude):
                filtered_lines.append(line.strip())
    df_Iterations = pd.DataFrame({'Filtered Lines': filtered_lines})
    # df_Iterations.to_csv("Iterations Lines.txt",header=False, index=False)
    
    Iterations = df_Iterations['Filtered Lines'].str.findall(pattern)
    
    Iterations = [[eval(row) for row in sublist] for sublist in Iterations]
    Iterations = pd.DataFrame(Iterations)
    
    # Iterations.iloc[:,swap_1], Iterations.iloc[:,swap_2] = np.where(Iterations.iloc[:,swap_1].notna(), [Iterations.iloc[:,swap_1], Iterations.iloc[:,swap_2]], [Iterations.iloc[:,swap_2], Iterations.iloc[:,swap_1]])
    for index, row in Iterations.iterrows():
        last_column_value = row.iloc[swap_1]
        if pd.isna(last_column_value):
            non_nan_values = row.dropna().tolist()
            if line_search == "NO":
                Iterations.loc[index] = non_nan_values[:swap_2] + [None] + non_nan_values[swap_2:]
            if line_search == "YES":
                Iterations.loc[index] = non_nan_values[:swap_2] + [None,None] + non_nan_values[swap_2:]           
            
    Iterations.fillna(0, inplace=True)
    df_Iterations_numbers = Iterations
    # df_Iterations_numbers.to_csv("Iterations.txt",header=False, index=False)
    Iterations = Iterations.to_numpy()
    
    end_iter = df_Iterations.iloc[indices]
    # end_iter.to_csv("End Iterations.txt", header=False, index=False)
    
    keywords_to_include = [ current_step_name ]
    filtered_lines = []
    with open(message_file, 'r', encoding='utf8') as file:
        for line in file:
            if any(keyword in line for keyword in keywords_to_include):
                filtered_lines.append(line.strip())
    Times = pd.DataFrame({'Filtered Lines': filtered_lines})
    Times = Times['Filtered Lines'].str.findall(pattern) #&.apply(pd.to_numeric).explode('0')
    Times = [[eval(row) for row in sublist] for sublist in Times]
    Times = pd.DataFrame(Times)
    Times = Times[0]
    df_Times = Times
    # df_Times.to_csv("Filtered Times.txt", header=False, index=False)
    Times = Times.to_numpy()
    print("Time Steps = ", Times)
    timesteps_converged = []
    timesteps_error = []
    steps_converged = []
    steps_error = []
    for kk in range(1,Times.size):
        # time = Times[kk]
        if Times[kk-1] < Times[kk]:
            # print(Times[kk-1])
            timesteps_converged.append(Times[kk-1])
            steps_converged.append(kk-1)
        else:   
            timesteps_error.append(Times[kk-1])
            steps_error.append(kk-1)
    
    # print("steps_converged", steps_converged)
    # print("steps_error", steps_error) 
    # print("timesteps_converged = ", timesteps_converged)
    # print("timesteps_error = ", timesteps_error)
    iter_converged = end_iter.iloc[steps_converged]
    iter_converged = iter_converged['Filtered Lines'].str.findall(pattern)
    iter_converged = np.array([[float(entry) for entry in sublist] for sublist in iter_converged])
    print("iter_converged = ", iter_converged)
    iter_converged_df= pd.DataFrame(iter_converged)
    # iter_converged_df.to_csv("Iterations Converged.txt", header=False, index=False)
    Iteration_number = np.arange(1,len(Iterations)+1)
    
    RESIDU_ABSOLU = Iterations[:,RESIDU_ABSOLU_probe_position]
    RESIDU_RELATIF = Iterations[:,RESIDU_RELATIF_probe_position]
    F = abs(RESIDU_ABSOLU/RESIDU_RELATIF)
    criterion = RESI_GLOB_RELA * F
    
    # plt.close("all")  
    if mode == 1:
        plt.style.use("dark_background")
        for param in ['text.color', 'axes.labelcolor', 'xtick.color', 'ytick.color']:
            plt.rcParams[param] = '0.9'  # very light grey
        for param in ['figure.facecolor', 'axes.facecolor', 'savefig.facecolor' ]:
            plt.rcParams[param] =  "#212946" #'#212946' # '#212946' "#003544" #"#052130"  "#1C2833"  "#19232D" "#00212B"  "#002B36" "#212E3B" 
        plt.rcParams['axes.edgecolor'] = "2A546D" #"053D5C" # '#2A546D'
        
    fig1 = plt.figure(num=0, figsize=(12, 8), dpi=80, )
    
    load_case = os.path.basename(os.path.dirname((os.path.dirname((os.path.dirname(os.path.dirname(message_file)))))) + " - " + os.path.basename(os.path.dirname(os.path.dirname(message_file))))
    fig1.canvas.manager.set_window_title("code_aster Convergence Monitoring - " + load_case )   
    fig1.clear()
    plt.subplot(2, 1, 1)
    # fnt = "Comic Sans MS"
    # fnt = "Segoe UI"
    fnt = "Century Gothic"
    # fnt = "Helvetica"
    # fnt = "Calibri Light"
    # fnt = "Abadi"
    # fnt ="Arial"
    plt.title( "FORCE CONVERGENCE" , fontsize=18, fontdict={"family": fnt} ) #, fontweight="bold")
    line_width = 2.0

    if mode == 1:
        color_force = "#003FFF" #"#094BDD" # "#652B91" #"#652B91" '#08F7FE' #
        color_criterion = "#A748EE"
        color_converged =  '#00ff41'#"#008E00"
        color_error = "r"
        color_timestep = '#00ff41' #"g" #"#1E981E"
        color_last_timestep = "w" # "#5E5C00"
        color_probe =  "r"  # "#FF4747" '#08F7FE' #
        color_monitoring = '#F5D300' #"#4D4D4D"
        color_grid = "#2A3459" #'#2A3459'# "#24485E" #  "#053D5C"  
    else:
        color_force = "#094BDD" # "#652B91" #"#652B91"
        color_criterion = "#6600FF"
        color_converged = "#008E00"
        color_error = "#CC0000"
        color_timestep = "g" #"#1E981E"
        color_last_timestep = "k" # "#5E5C00"
        color_probe = "r"
        color_monitoring = "#4D4D4D"       
    
    # "RESIDU_ABSOLU (Absolute Residue) = Force Convergence"
    # "RESIDU_RELATIF $\cdot$ $F_{ext}$ (Relative Residue $\cdot$ External Force) = Criterion"
    plt.plot(Iteration_number, RESIDU_ABSOLU, color_force, linewidth=line_width , label = "Absolute Residual (Force Convergence)" )
    plt.plot(Iteration_number, criterion, color_criterion, linewidth=line_width , label = "Relative Residual (Criterion)")
    
    for ii in steps_converged:
        plt.vlines(x= indices[ii]+1, ymin= 0 , ymax= max(RESIDU_ABSOLU)*2 , color= color_converged, linestyles="--", linewidth= 1)
        plt.text(indices[ii]+1, max(RESIDU_ABSOLU*2), str(int(indices[ii]+1)), color= color_converged, fontsize = 12)
    for ii in steps_error:
        plt.vlines(x= indices[ii]+1, ymin= 0 , ymax= max(RESIDU_ABSOLU)*2 , color= color_error, linestyles="--", linewidth= 1)
        plt.text(indices[ii]+1, max(RESIDU_ABSOLU*2), str(int(indices[ii]+1)), color= color_error, fontsize = 12)
    plt.vlines(x= Iteration_number[-1], ymin= 0 , ymax= max(RESIDU_ABSOLU)*2 , color=color_last_timestep, linestyles="--", linewidth= 1)
    plt.text(Iteration_number[-1], max(RESIDU_ABSOLU)*2, str("%.0f"%Iteration_number[-1]), color=color_last_timestep, fontsize = 12)  
    
    if mode == 1:
        n_shades = 10
        diff_linewidth = 1.05
        alpha_value = 0.2 / n_shades
        aa=0 
        for n in range(1, n_shades+1):
            plt.plot( Iteration_number, RESIDU_ABSOLU , color=color_force, linewidth=2+(diff_linewidth*n), alpha=alpha_value  ) 
        for n in range(1,n_shades):
            aa+=1
            y_0 = np.array(RESIDU_ABSOLU)*np.e**(aa/(n_shades*0.1))/np.e**10
            plt.fill_between(x=Iteration_number,y1=y_0,y2=RESIDU_ABSOLU,color=color_force,alpha=alpha_value*1.1)
            
        n_shades = 10
        diff_linewidth = 1.05
        alpha_value = 0.2 / n_shades
        aa=0 
        for n in range(1, n_shades+1):
            plt.plot( Iteration_number, criterion , color=color_criterion, linewidth=2+(diff_linewidth*n), alpha=alpha_value  ) 
        for n in range(1,n_shades):
            aa+=1
            y_0 = np.array(criterion)*np.e**(aa/(n_shades*0.1))/np.e**10
            plt.fill_between(x=Iteration_number,y1=y_0,y2=criterion,color=color_criterion,alpha=alpha_value*1.1)
    
    # plt.xticks(np.arange(0, max(Iteration_number)+1, 10))
    plt.ylabel('$Force$' + ' $[N]$ ', fontsize = 15)
    plt.xlabel(' $Iteration$ '+ '$[-]$ ', fontsize = 15)
    plt.grid(linestyle= '--', linewidth= 1)
    if mode == 1:
        plt.grid(linestyle= '-', linewidth= 1, color=color_grid )         
    plt.yscale('log')
    plt.plot( 1,1, "--", color= color_converged, linewidth= 1 , label="Time Step Converged")
    plt.plot( 1,1, "--", color= color_error, linewidth= 1 , label="Failure")
    plt.legend(loc='lower left', shadow= True,  ncol=2, fontsize= 13)
    
    
    plt.subplot(2, 1, 2) ; print(Times, Iteration_number)
    if len(Times) > 1:
        # plt.title(' Time Steps ', fontsize= 18)
        indices_time = np.append(0,indices)
        indices_time = np.diff(indices_time)
        Time = np.delete(Times, -1)
        Time = np.repeat(Time, indices_time)
        Time = np.append(Time[0],Time)
        end_time = Times[-1]*np.ones(len(Iteration_number) - len(Time))
        Time = np.append(Time,end_time)
        
        plt.plot( Iteration_number, Time ,  linestyle='-', linewidth=line_width , color=color_timestep, label = "Time Step = " + str(Time[-1]) )
        # plt.plot( Iteration_number, Time , "h", color=color_timestep, markersize=4 )
        # plt.text( Iteration_number[-1], Time[-1] , "[" + str(Iteration_number[-1]) + " ; " + str(Time[-1])+"]", color= color_timestep , weight="normal", horizontalalignment='right', verticalalignment='bottom', fontsize = 14)

        for ii in steps_converged:
            plt.vlines(x= indices[ii]+1, ymin= 0 , ymax= max(Time)*1.2 , color= color_converged, linestyles="--", linewidth= 1)
            plt.text(indices[ii]+1, max(Time)*1.2, str("%.3g"%Times[ii]), color= color_converged, fontsize = 12)
        for ii in steps_error:
            plt.vlines(x= indices[ii]+1, ymin= 0 , ymax= max(Time)*1.2 , color= color_error, linestyles="--", linewidth= 1)
            plt.text(indices[ii]+1, max(Time)*1.2, str("%.3g"%Times[ii]), color= color_error, fontsize = 12)
        plt.vlines(x= Iteration_number[-1], ymin= 0 , ymax= max(Time)*1.2 , color=color_last_timestep, linestyles="--", linewidth= 1)
        plt.text(Iteration_number[-1], max(Time)*1.2, str("%.3g"%Times[-1]), color=color_last_timestep, fontsize = 12)

        if mode == 1:
            n_shades = 20
            diff_linewidth = 1.05
            alpha_value = 0.2 / n_shades
            aa=0 
            for n in range(1, n_shades+1):
                plt.plot( Iteration_number, Time , color=color_timestep, linewidth=2+(diff_linewidth*n), alpha=alpha_value  ) 
            for n in range(1,n_shades):
                aa+=1
                y_0 = np.array(Time)*(aa/n_shades)
                plt.fill_between(x=Iteration_number,y2=y_0,y1=Time,color=color_timestep,alpha=alpha_value*1)
    else:
        plt.plot( Iteration_number[-1], Times[0] , "s" , color=color_timestep, label = "Time Step = " + str(Times[0]) )
        
    plt.rc('xtick', labelsize= 14)   
    plt.rc('ytick', labelsize= 14) 
    plt.ylabel('$Time$' + ' $[s]$ ', fontsize = 15)
    plt.xlabel(' $Iteration$ '+ '$[-]$ ', fontsize = 15)
    plt.grid(linestyle= '--', linewidth= 1)
    if mode == 1:
        plt.grid(linestyle= '-', linewidth= 1, color=color_grid )
    plt.legend(loc='lower left', shadow= True,  ncol=4, fontsize= 12)            
        
    plt.tight_layout()
    plt.show(block= False )  
    fig1.canvas.draw() 

    fig2 = plt.figure(num=1, figsize=(12, 8), dpi=80)
    fig2.canvas.manager.set_window_title("code_aster Probe Monitoring")
    fig2.clear()
    plt.subplot(2, 1, 1)
    plt.title('PROBE' , fontsize=18, fontdict={"family": fnt} )
    plt.plot( Iteration_number, Iterations[:,probe_position] ,  linestyle='-', linewidth=line_width , color=color_monitoring , label = "Monitoring = " + str(Iterations[-1,probe_position]))
    # plt.plot( Iteration_number, Iterations[:,probe_position] , "h", color="k", markersize=4 )
    # plt.text( Iteration_number[-1], max(Iterations[:,probe_position])*1.1  , "[" + str(Iteration_number[-1]) + " ; " + str(Iterations[-1,probe_position])+"]", color= 'k' , weight="normal", horizontalalignment='right', verticalalignment='bottom', fontsize = 14)
    
    if mode == 1:
        n_shades = 20
        diff_linewidth = 1.05
        alpha_value = 0.2 / n_shades
        aa=0 
        for n in range(1, n_shades+1):
            plt.plot( Iteration_number, Iterations[:,probe_position] , color=color_monitoring, linewidth=2+(diff_linewidth*n), alpha=alpha_value  ) 
        for n in range(1,n_shades):
            aa+=1
            y_0 = np.array(Iterations[:,probe_position])*(aa/n_shades)
            plt.fill_between(x=Iteration_number,y2=y_0,y1=Iterations[:,probe_position],color=color_monitoring,alpha=alpha_value*1)
    
    plt.rc('xtick', labelsize= 14)   
    plt.rc('ytick', labelsize= 14) 
    plt.ticklabel_format(axis='y', style='scientific', scilimits=(0, 0))
    plt.ylabel('$Probe$'+' $'+Unit+'$', fontsize = 15)
    plt.xlabel(' $Iteration$ '+ '$[-]$ ' , fontsize = 15)
    plt.grid(linestyle= '--', linewidth= 1)
    if mode == 1:
        plt.grid(linestyle= '-', linewidth= 1, color=color_grid )
    plt.legend(loc='lower left', shadow= True,  ncol=4, fontsize= 13)
    for ii in steps_converged:
        plt.vlines(x= indices[ii]+1, ymin= 0 , ymax= max(Iterations[:,probe_position])*1.1 , color= color_converged, linestyles="--", linewidth= 1)
        plt.text(indices[ii]+1, max(Iterations[:,probe_position])*1.1 , str(int(indices[ii]+1)), color= color_converged, fontsize = 12)
    for ii in steps_error:
        plt.vlines(x= indices[ii]+1, ymin= 0 , ymax= max(Iterations[:,probe_position])*1.1 , color= color_error, linestyles="--", linewidth= 1)
        plt.text(indices[ii]+1, max(Iterations[:,probe_position])*1.1 , str(int(indices[ii]+1)), color= color_error, fontsize = 12)
    plt.vlines(x= Iteration_number[-1], ymin= 0 , ymax= max(Iterations[:,probe_position])*1.1 , color=color_last_timestep, linestyles="--", linewidth= 1)
    plt.text(Iteration_number[-1], max(Iterations[:,probe_position])*1.1, str("%.0f"%Iteration_number[-1]), color=color_last_timestep, fontsize = 12)
    if len(timesteps_converged) >= 1:
        plt.subplot(2, 1, 2)
       
        if Times[-1] > Times[-2] and end_ok == 1:
            timesteps_converged.append(Times[-1])
            iter_converged = np.vstack([iter_converged, Iterations[-1]])
            
        print("Converged Time Steps = ", timesteps_converged)
        print("Error Time Steps = ", timesteps_error)
        print("Number of Time Steps = ", len(Times) )
        print("Number of Converged Time Steps = ", len(timesteps_converged) )
        print("Number of Failed Time Steps = ", len(timesteps_error) )
        
        plt.plot( np.append(0,iter_converged[:,probe_position]), np.append(0,timesteps_converged) ,  linestyle='-', linewidth=line_width , color=color_probe, label = "Probe = " + str(iter_converged[-1,probe_position]) + "\nTime = " + str(timesteps_converged[-1]) )
        plt.plot( iter_converged[:,probe_position], timesteps_converged  , "o", color=color_probe , markersize=5 )
        # plt.text( iter_converged[-1,probe_position], timesteps_converged[-1] , "[" + str(iter_converged[-1,probe_position]) + " ; " +str(timesteps_converged[-1]) +"]", color= color_probe , weight="normal", horizontalalignment='right', verticalalignment='bottom', fontsize = 14)
        
        if mode == 1:
            n_shades = 20
            diff_linewidth = 1.05
            alpha_value = 0.4 / n_shades
            aa=0 
            for n in range(1, n_shades+1):
                plt.plot( np.append(0,iter_converged[:,probe_position]), np.append(0,timesteps_converged) , color=color_probe, linewidth=2+(diff_linewidth*n), alpha=alpha_value  ) 
            for n in range(1,n_shades):
                aa+=1
                y_0 = np.array(np.append(0,timesteps_converged))*(aa/n_shades)
                plt.fill_between(x=np.append(0,iter_converged[:,probe_position]),y2=y_0,y1=np.append(0,timesteps_converged),color=color_probe,alpha=alpha_value*1)

        plt.rc('xtick', labelsize= 14)   
        plt.rc('ytick', labelsize= 14) 
        plt.ylabel('$Time$' + ' $[s]$ ', fontsize = 15)
        plt.xlabel('$Converged$'+" "+'$Probe$'+' $'+Unit+'$',  fontsize = 15)
        plt.grid(linestyle= '--', linewidth= 1)
        if mode == 1:
            plt.grid(linestyle= '-', linewidth= 1, color=color_grid )
        plt.legend(loc='upper left', shadow= True,  ncol=4, fontsize= 13)
        Probe = pd.DataFrame( (np.array([timesteps_converged,iter_converged[:,probe_position]] ).transpose()), columns=['Time', 'Probe',])
        if print_files == 1:
            Probe.to_csv("./code_aster_Monitoring_Data/Probe.txt", index=False)
    plt.tight_layout()
    plt.show(block= False )
    fig2.canvas.draw() 
    plt.figure(0) 
    plt.show(block= False )
    plt.style.use("default")
    
    # print(move_figure)
    if move_figure == 1:
        fig1.canvas.manager.window.move(300, 500)
        fig2.canvas.manager.window.move(1300, 500)
    move_figure+=1    
    
    if print_files == 1:
        df_Lines.to_csv("./code_aster_Monitoring_Data/Filtered Lines.txt",header=False, index=False)
        df_Iterations.to_csv("./code_aster_Monitoring_Data/Iterations Lines.txt",header=False, index=False)
        df_Iterations_numbers.to_csv("./code_aster_Monitoring_Data/Iterations.txt",header=False, index=False)
        end_iter.to_csv("./code_aster_Monitoring_Data/End Iterations.txt", header=False, index=False)
        df_Times.to_csv("./code_aster_Monitoring_Data/Filtered Times.txt", header=False, index=False)
        iter_converged_df.to_csv("./code_aster_Monitoring_Data/Iterations Converged.txt", header=False, index=False)
    
if __name__ == '__main__':
        
    # directory = r'Y:\tmp'  ;    file_name = 'fort.6'         # search for the file automatically
    directory = r"C:\Users\trusinja\Desktop\ASTER_WORK\AG_WORK"   
    file_name = "fort.6"
    file_number = 0        # set to row number that you want, if there is more than one message file found	
    
    open_file = 0           # activate - 1 , deactivate - 0
    # application = "notepad.exe"
    application = r"C:\Users\trusinja\AppData\Local\Programs\Microsoft VS Code\Code.exe"
    
    file_auto = 1         # use manually entered message path , activate - 0 , deactivate - 1
    message_file = r"C:\Users\trusinja\Desktop\ASTER_WORK\AG_WORK\OTHER\BALL_INDENTATION\STUDY\case\temporary\fort.6"
    
    probe_position = -1           # probe probe_position  , 7 for contact and friction , 6 for contact
    print_files = 1
    
    Unit = "[-]"
    Language = "FR"
    
    mode = 1
    
    
    code_aster_monitoring(directory,file_name,file_number,open_file,application,file_auto,message_file,probe_position,print_files,mode,Unit,Language)
    















