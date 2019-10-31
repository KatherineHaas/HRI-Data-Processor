#Import all necessary libraries

#Data File Libraries
import csv
import pandas as pd
import glob
import os

#Math Function Libraries
import math
import statistics

#3D Graphing Libraries
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


#Define Necessary Functions

#Define function to calculate mode
#Returns the mode of the inputted data
def calculate_mode(input_list):
    count_dict = {}
    found_mode = []
    max_count = 0
    
    for value in input_list:
        if value not in count_dict:
            count_dict[value] = 0
        count_dict[value] += 1
        
        if count_dict[value] > max_count:
            max_count = count_dict[value]

    for value, count in count_dict.items():
        if count == max_count:
            found_mode = value
            
    return found_mode, max_count


#Define function to calculate mean
#Returns the mean of the inputted data
def calculate_mean(input_list):
    sum = 0
    count = len(input_list)
    for value in input_list:
        if math.isnan(value) == False:
            sum += value
    
    found_mean = sum / count

    return found_mean


#Define function to calculate median
#Returns the median of the inputted data
def calculate_median(input_list):
    found_median = statistics.median_low(input_list)
    
    return found_median


#Define function to calculate range
#Returns the range of the inputted data
def calculate_range(input_list):
    sorted_input_list = sorted(input_list)
    lowest_value = sorted_input_list[0]
    highest_value = sorted_input_list[-1]
    found_range = highest_value - lowest_value
    
    return found_range


#Define function to perform all calculations at once
#Returns final values from above 4 functions
def calculation_processor(input_list):
    found_mode, max_count = calculate_mode(input_list)
    found_mean = calculate_mean(input_list)
    found_median = calculate_median(input_list)
    found_range = calculate_range(input_list)
    
    return found_mode, found_mean, found_median, found_range


#Define function to present processed data
#Returns processed data in easy-to-read manner
def data_return(found_mode, found_mean, found_median, found_range, data_metric, data_file):
    print("\nYou analyzed the metric {data_metric} from the file {data_file}.".format(data_metric = data_metric, data_file = data_file))
    print("\nThe mode was {found_mode}".format(found_mode = found_mode))
    print("\nThe mean was {found_mean}".format(found_mean = found_mean))
    print("\nThe median was {found_median}".format(found_median = found_median))
    print("\nThe range was {found_range}".format(found_range = found_range))


#Define function to gather a list for a specific metric from all files in a folder (ASK ABOUT GLOB + PANDAS)
#Returns a list that serves as input for future functions
def multiple_file_panda_read(data_folder, data_metric):
    input_list = []
    
    os.chdir("/" + data_folder)
    filenames = [i for i in glob.glob('*.csv')]
    
    df_collection = (pd.read_csv(f) for f in filenames)
    concatenated_df = pd.concat(df_collection, ignore_index = True, sort = True)

    input_list = concatenated_df[data_metric]
    return input_list


#Define function to gather a list for a specific metric from a single file
#Returns a list that serves as input for future functions
def single_file_panda_read(data_folder, data_file, data_metric):
    file_storage_value = ''
    input_list = []
    
    os.chdir("/" + data_folder)
    filenames = [i for i in glob.glob('*.csv')]
    if data_file in filenames:
        file_storage_value = data_file

        df = pd.read_csv(file_storage_value)
        input_list = df[data_metric]

    return input_list


#Define function to return a plot of the XYZ scatter plot graph
#Returns a 3D scatter plot graph
def X_Y_Z_plot(data_folder, data_file, graph_parameters, pathname, save_graph):
    coordinate_dictionary = {}
    file_storage_value = ''
    os.chdir("/" + data_folder)
    
    filenames = [i for i in glob.glob('*.csv')]
    
    if (data_file == 'all.csv'):
        df_collection = (pd.read_csv(f) for f in filenames)
        concatenated_df = pd.concat(df_collection, ignore_index=True)
        dataframe = concatenated_df
    
    else:
        if data_file in filenames:
            file_storage_value = data_file
            dataframe = pd.read_csv(file_storage_value)
    
    fig = plt.figure()
    ax = plt.axes(projection="3d")
    
    ax.scatter3D(dataframe["X"], dataframe["Y"], dataframe["Z"], c = 'r', marker = 'o');
    
    ax.set_xlabel('X Axis')
    ax.set_ylabel('Y Axis')
    ax.set_zlabel('Z Axis')
    
    if save_graph == 1:
        plt.savefig(os.path.join(pathname, r'3D_Graph.png'), bbox_inches='tight')
        plt.show()
    else:
        plt.show()
        

#Define function to compose a 2Dimensional plot of X vs Y graphs
#Returns a 2D Scatter plot graph
def X_Y_plot(data_folder, data_file, graph_parameters, pathname, save_graph):
    coordinate_dictionary = {}
    file_storage_value = ''
    os.chdir("/" + data_folder)

    filenames = [i for i in glob.glob('*.csv')]
    
    if (data_file == 'all.csv'):
        df_collection = (pd.read_csv(f) for f in filenames)
        concatenated_df = pd.concat(df_collection, ignore_index = True, sort = True)
        dataframe = concatenated_df
    
    else:
        if data_file in filenames:
            file_storage_value = data_file
            dataframe = pd.read_csv(file_storage_value)
            
    x_list = list(dataframe["X"])
    y_list = list(dataframe["Y"])
    
    current_axis = plt.gca()
    current_axis.add_patch(Rectangle((calculate_mean(x_list) - .4, calculate_mean(y_list) - .4), (graph_parameters[1] - graph_parameters[0]), (graph_parameters[3] - graph_parameters[2]), facecolor = 'grey'))
    
    plt.plot(x_list, y_list, 'ro')
    
    x_list_sorted = sorted(x_list)
    y_list_sorted = sorted(y_list)
    
    parameters = [(x_list_sorted[0] - 1), (x_list_sorted[-1] + 1), (y_list_sorted[0] - 1), (y_list_sorted[-1] + 1)]
    
    plt.axis(parameters)
    plt.grid(axis = 'both')
    
    if save_graph == 1:
        plt.savefig(os.path.join(pathname, r'3D_Graph.png'), bbox_inches='tight')
        plt.show()
    else:
        plt.show()
        

#Define If-Else function to determine whether to use single file function or multiple file function
#Returns a list that serves as input for future functions
def single_or_multiple_panda_reader(data_folder, data_file, data_metric):

    if (data_file == "all.csv"):
        input_list = multiple_file_panda_read(data_folder, data_metric)
        return input_list

    else:
        input_list = single_file_panda_read(data_folder, data_file, data_metric)
            
        return input_list


#Define a function to clean the raw data into processable data
#Returns a clean input_list
def data_list_cleaner(input_list):
    input_list_clean = list(map(float, input_list))
    for element in input_list_clean:
    
        if (math.isnan(element) == False):
            continue
        else:
            element_index = input_list_clean.index(element)
            input_list_clean.pop(element_index) 
            
    return input_list_clean


#Define a function to translate a dictionary into a csv file at a predestined location
def dictionary_to_csv(input_dictionary, pathname):
    df = pd.DataFrame(input_dictionary, index = ["Mode", "Mean", "Median", "Range", "Data Range [Lower, Upper]", "Most Popular Option", "Most Popular Count"])

    df.to_csv(os.path.join(pathname, r'Processed_Data.csv'))


#Define a function to calculate where the data is most dense(Coordinate System)
#Returns a list of the upper and lower bounds
def variable_density(input_list):
    
    select_mad = np.mean(np.absolute(input_list - np.mean(input_list)))
    found_mean = calculate_mean(input_list)

    coordinate_limits = [(found_mean - select_mad), (found_mean + select_mad)]
    
    return coordinate_limits # lower bound then upper bound

    
#Define function to determine whether or not to continue the while loop based on input
#Returns a variable that stops while loop or continues it
def continue_loop(data_folder, data_file, data_metric):
    print("\n----------------------------------------------------------------------------------------------------------------------------------------------------")
    #Determines if user wants to analyze anything else (Gateways act as checkpoints)
    metric_gateway = input("\nWould you like to analyze another metric from the same data file(s)(y/n)? ")

    #Determines if user wants to analyze another file
    if (metric_gateway.lower() == "n"):
        file_gateway = input("\nWould you like to analyze data from a different data file(s)(y/n)? ")
 
        #Determines if user wants to access a different folder
        if (file_gateway.lower() == "n"):
            folder_gateway = input("\nWould you like to analyze data from another folder(y/n)? ")

            if (folder_gateway.lower() == "n"):
                placeholder = 0
#Asks user to enter new data based on previous answer
            else:
                data_folder = input("\nWhat folder would you like to analyze data from? ")
                data_file = input("\nWhat data file would you like to analyze? ")
                data_metric = input("\nWhich metric would you like to analyze from the above file(s)? ")
                print("\n----------------------------------------------------------------------------------------------------------------------------------------------------")

        else:
            data_file = input("\nWhat data file would you like to analyze? ")
            data_metric = input("\nWhich metric would you like to analyze from the above file(s)? ")
            print("\n----------------------------------------------------------------------------------------------------------------------------------------------------")

    else:
        data_metric = input("\nWhich metric would you like to analyze from the above file(s)? ")
        print("\n----------------------------------------------------------------------------------------------------------------------------------------------------")

    #Determines if loop should stop    
    if (metric_gateway.lower() == "n") and (file_gateway.lower() == "n") and (folder_gateway.lower() == "n"):
        stop = 1

    else:
        stop = 0

    return stop, data_folder, data_file, data_metric


#Define function to gather data_folder, data_file, and data_metric to be used from user
#Returns file(s) and metric to analyze
def specific_introduction_interface():
    print("\n----------------------------------------------------------------------------------------------------------------------------------------------------")
    data_folder = input("\nWhat is the name of the folder the file(s) are stored in? ")
    
    print("\nTo analyze all data files enter the keyword \"all\".")
    data_file = input("Which data file(s) would you like to analyze? ")
    
    print("\nTo create an XY and XYZ graph enter the keyword \"graph\".")
    data_metric = input("Which metric would you like to analyze from the above file(s)? ")
    
    print("\n----------------------------------------------------------------------------------------------------------------------------------------------------")
    data_file_correct = data_file + ".csv"
    
    return data_folder, data_file_correct, data_metric


#Specific Data Collection function, contains everything
def specific_file_and_metric():
    #Defining initial variables
    stop = 0
    graph_parameters = []
    save_graph = 0
    pathname = "N/A"

    #Find initial data acquisition area
    data_folder, data_file, data_metric = specific_introduction_interface()
    
    #While loop to repeat function as necessary
    while (stop == 0):

        #If data_metric = "graph", creates and returns a plot of the XYZ 3D graph and XY 2D graph, else normal data collection(0 = no parameters, 1 = special parameters)
        if data_metric == "graph":
        
            for letter in "XYZ":
                
                input_list = multiple_file_panda_read(data_folder, letter)
                
                data_range = variable_density(input_list)
            
                for value in data_range:
                    graph_parameters.append(value)
                
            X_Y_plot(data_folder, data_file, graph_parameters, pathname, save_graph)
            X_Y_Z_plot(data_folder, data_file, graph_parameters, pathname, save_graph)
            
            
        else:
            
            if (data_metric == "Button_active") or (data_metric == "Screen_mode"):
                #Gathers data to analyze
                input_list = multiple_file_panda_read(data_folder, data_metric)
            
                #Calculates all possible results given the available metric
                most_popular_option, popular_option_count = calculate_mode(input_list)
            
                #Returns the processed data to the user
                print("\nYou analyzed the metric {data_metric} from the file {data_file}.".format(data_metric = data_metric, data_file = data_file))
                print("\nThe most popular option was {most_popular_option}".format(most_popular_option = most_popular_option))
                print("\nThe most popular option occurred {popular_option_count} times".format(popular_option_count = popular_option_count))
            else:
            
                #Gathers a list of raw data
                input_list = single_or_multiple_panda_reader(data_folder, data_file, data_metric)

                #Cleans the raw data into processable data
                input_list = data_list_cleaner(input_list)
        
                #Processes data based off of raw data    
                found_mode, found_mean, found_median, found_range = calculation_processor(input_list)

                #Returns the processed data to the user    
                data_return(found_mode, found_mean, found_median, found_range, data_metric, data_file)

        #Determines whether or not to stop the while loop
        stop, data_folder, data_file, data_metric = continue_loop(data_folder, data_file, data_metric)


#Define a function that gathers a list of metrics to analyze
#Returns a list of data metrics
def metrics_to_analyze(data_folder):
    metric_list = []
    
    os.chdir("/" + data_folder)
    filenames = [i for i in glob.glob('*.csv')]
    
    for filename in filenames:

        with open(filename) as file_data:
            temp_dict = csv.DictReader(file_data)
            
            for row in temp_dict:
                temp_list_keys = list(row.keys())
                
                for element in temp_list_keys:
                    metric_list.append(element)

    metric_list_unique = sorted(list(set(metric_list)))

    return metric_list_unique
    

#Define a function to gather information on all metrics from all files
def default_data_processing():
    #Defining initial variables
    complete_data_dictionary = {}
    data_file = 'all.csv'
    graph_parameters = []
    save_graph = 1
    
    #Find folder to collect data from
    print("\n----------------------------------------------------------------------------------------------------------------------------------------------------")
    data_folder = input("What folder would you like to analyze data from? ")
    pathname = input("\nEnter the path for where you would like to save your data: ")
    
    #Gather a list of metrics to analyze
    metric_list = metrics_to_analyze(data_folder)
    
    
    #Loop to sort through each metric's data
    for data_metric in metric_list:
    
        #Determines if the data metric is valid for data analysis
        if (data_metric == "Button_active") or (data_metric == "Screen_mode"):
            
            #Gathers data to analyze
            input_list = multiple_file_panda_read(data_folder, data_metric)
            
            #Calculates all possible results given the available metric
            most_popular_option, popular_option_count = calculate_mode(input_list)
            
            #Attaches data to a dictionary
            complete_data_dictionary[data_metric] = ["N/A", "N/A", "N/A", "N/A", "N/A", most_popular_option, popular_option_count]
                
        else:
        
            #Determines if the data_metric is valid for data range analysis
            if (data_metric == "X") or (data_metric == "Y") or (data_metric == "Z"):
                
                #Gathers data to analyze
                input_list = multiple_file_panda_read(data_folder, data_metric)
                
                #Cleans the raw data into processable data
                input_list = data_list_cleaner(input_list)
            
                #Calculates all possible results given the available metric
                found_mode, found_mean, found_median, found_range = calculation_processor(input_list)
                
                #Calculates the data range
                data_range = variable_density(input_list)
                
                #Appends the  data_range to a parameter list to be used in a graph
                for value in data_range:
                    graph_parameters.append(value)
                
                #Attaches data to a dictionary
                complete_data_dictionary[data_metric] = [found_mode, found_mean, found_median, found_range, data_range, "N/A", "N/A"]
            
            else:
            
                #Gathers data to analyze
                input_list = multiple_file_panda_read(data_folder, data_metric)
                
                #Cleans the raw data into processable data
                input_list = data_list_cleaner(input_list)
            
                #Calculates all possible results given the available metric
                found_mode, found_mean, found_median, found_range = calculation_processor(input_list)
        
                #Attaches data to a dictionary
                complete_data_dictionary[data_metric] = [found_mode, found_mean, found_median, found_range, "N/A", "N/A", "N/A"]
            
    
    
    #Converts the full set of data into a csv file at a predestined location
    dictionary_to_csv(complete_data_dictionary, pathname)
    
    
    #Generates and saves the XY and XYZ graphs into a predestined location as pngs
    #Calls the graphing functions to graph the dataset with parameters above and without parameters
    X_Y_plot(data_folder, data_file, graph_parameters, pathname, save_graph)
    X_Y_Z_plot(data_folder, data_file, graph_parameters, pathname, save_graph)


#Define a function to giver the user an idea of how the function works and what it does
def function_description():
    print("\n----------------------------------------------------------------------------------------------------------------------------------------------------")
    print("\nThis function analyzes data and returns usable data in a csv file.")
    print("\nYour returned data is saved in the folder Data_Sorter_Test_Results.")


#Define a main function to decide between default or specific analysis mode
def main():
    #Initial Variables
    stop = 0
    
    #Describe the function and give default information
    function_description()
    
    #Ask user initializing questions
    print("\n----------------------------------------------------------------------------------------------------------------------------------------------------")
    print("\nThis program is case sensitive")
    print("Enter \"n\" if you would like to analyze a specific dataset.")
    default_or_specific = input("Would you like to analyze all metrics from all files(y/n)? ")
    
    #While loop determines which secondary function to call on
    while (stop == 0):
        
        if (default_or_specific == "y"):
            default_data_processing()
            stop = 1
            
        elif (default_or_specific == "n"):
            specific_file_and_metric()
            stop = 1
            
        else:
            default_or_specific = input("\nInvalid answer. Please enter a valid answer(y/n): ")
    
    #Is polite
    print("Have a nice day!")

#Call the main() function
main()
