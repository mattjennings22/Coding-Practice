### Library Imports
import os
import sys
import glob
import datacompy
import pandas as pd

# these functions can be used to compare files within a folder to ensure they are matching
# this is helpful for QA when testing out a new process that generates data outputs

def compare_file_count_and_names(new_report_export_file_path, old_report_export_file_path):

    new_report_list = []

    for file_name in glob.glob(new_report_export_file_path+'/*.csv'):
        new_report_list.append(os.path.basename(file_name))

    old_report_list = []

    for file_name in glob.glob(old_report_export_file_path+'/*.csv'):
        old_report_list.append(os.path.basename(file_name))

    # check if report list is equal, sort to ensure they're in the same order
    new_report_list.sort()
    old_report_list.sort()
    if (len(new_report_list) == len(old_report_list)) & (new_report_list == old_report_list):
        print('Hooray! The new and old script process generated the same reports')
    else:
        print('Uh oh, looks like there is a mismatch in reports generated by the new and old script processes')
        print('the new report process generated {} reports'.format(len(new_report_list)))
        print('the old report process generated {} reports'.format(len(old_report_list)))
        print('reports in new script list but not in old script list')
        print(list(set(new_report_list) - set(old_report_list)))
        print('reports in old script list but not in new script list')
        print(list(set(old_report_list) - set(new_report_list)))
        sys.exit()


def compare_all_reports(new_report_export_file_path, old_report_export_file_path):

    final_report_list = []

    # can use either file path since we confirmed above that they have the same files
    for file_name in glob.glob(new_report_export_file_path+'/*.csv'):
        final_report_list.append(os.path.basename(file_name))
        print(os.path.basename(file_name))

    final_report_list.sort()

    # run through all reports
    for file_name in final_report_list:

        old_script_path = old_report_export_file_path + '/' + file_name
        old_script_report = pd.read_csv(old_script_path, low_memory=False)

        new_script_path = new_report_export_file_path + '/' + file_name
        new_script_report = pd.read_csv(new_script_path, low_memory=False)
            
        
        compare = datacompy.Compare(
                old_script_report,
                new_script_report,
                on_index=True,
                abs_tol=0.001, # there are some strange rounding errors, but nothing that affects the output to the 3nd decimal place
                rel_tol=0.001, # there are some strange rounding errors, but nothing that affects the output to the 3nd decimal place
                df1_name='Old Script Report', 
                df2_name='New Script Report'
            )
        
        if  compare.matches() and pd.DataFrame(compare.all_mismatch()).empty and compare.all_rows_overlap() and pd.Series(compare.df1_unq_columns(),dtype=object).empty and pd.Series(compare.df2_unq_columns(),dtype=object).empty:
            print('Hooray! Files {} are matching!'.format(file_name))

        else:
            print(compare.report())
            print('Files {} are not matching, please see compare output'.format(file_name))
            continue_input = input("\n\n Would you like to compare the next report? Hit enter to continue, any other value to exit \n\n")

            if continue_input == '':
                pass
            else:
                exit()



if __name__ == '__main__':

    ## default values for testing
    new_report_export_file_path = ''
    old_report_export_file_path = ''

    compare_file_count_and_names(new_report_export_file_path, old_report_export_file_path)

    compare_all_reports(new_report_export_file_path, old_report_export_file_path)