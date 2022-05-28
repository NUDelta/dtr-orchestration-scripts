"""
This script is used to create End-of-Quarter Checklists for each project in DTR, given a checklist template, output directory, and
studio database with student and project information.
"""

import sys
import helpers.imports as helpers
import studio_db_to_json as studio_db
from copy_gdrive_file import copy_file


def generate_eoq_checklist(studio_db_dict, gdrive_service, template_url, folder_url, qtr):
    """
    Generates a End-of-Quarter Checklist for each project.

    :param studio_db_dict: dict of each SIG with all student and project information.
    :param gdrive_service: Google Drive v3 authentication object.
    :param template_url: string url of original file to copy.
    :param folder_url: string url of folder to copy file to.
    :param qtr: string name of quarter to generate End-of-Quarter Checklists for.
    :return: None
    """
    # iterate over each SIG, and generate file names
    for sig_name, sig_info in studio_db_dict.items():
        # hold SIG abbreviation for file names
        curr_sig_abb = sig_info["abbreviation"]

        # iterate over projects
        for proj in sig_info["projects"]:
            # generate filename
            curr_proj_name = proj["project_name"]
            curr_filename = "[{abb}] {proj} {qtr} End-of-Quarter Checklist".format(abb=curr_sig_abb, proj=curr_proj_name, qtr=qtr)

            # copy original file for each project using curr_filename
            curr_copied_file = copy_file(gdrive_service, template_url, folder_url, curr_filename)

            # generate a file URL for copied file, and print out
            curr_file_id = curr_copied_file["id"]
            print("{filename}: https://docs.google.com/spreadsheets/d/{id}/edit".format(filename=curr_filename,
                                                                                        id=curr_file_id))


def main(template_file_url, folder_url, qtr_str, studio_db_url, sig_info_sheet_name, proj_info_sheet_name):
    """
    Fetches Studio Database information and uses it to generate End-of-Quarter Checklists.

    :param template_file_url: string url of original file to copy.
    :param folder_url: string url of folder to copy file to.
    :param studio_db_url: string url of Studio Database Google Spreadsheet
    :param qtr_str: string name of quarter to generate End-of-Quarter Checklists for.
    :param sig_info_sheet_name: string name of sheet where SIG information is stored.
    :param proj_info_sheet_name: string name of sheet where Project information is stored.
    :return:
    """
    # authenticate for Google Drive v3 and Google Spreadsheets APIs
    gdrive_service = helpers.auth_gdrive()
    gspreadsheets_service = helpers.auth_gsheets()

    # generate studio database
    studio_db_dict = studio_db.main(studio_db_url, sig_info_sheet_name, proj_info_sheet_name)

    # generate End-of-Quarter Checklists for each project
    generate_eoq_checklist(studio_db_dict, gdrive_service, template_file_url, folder_url, qtr_str)


if __name__ == '__main__':
    # get command line args
    arg_count = len(sys.argv) - 1

    # check for correct number of arguments
    if arg_count != 6:
        raise Exception("Invalid number of arguments. Expected 5 "
                        "(End-of-Quarter Checklist template URL, End-of-Quarter Checklist folder URL, Quarter Name, "
                        "Studio Database URL, SIG Info sheet name, Proj Info sheet name) got {}."
                        .format(arg_count))

    # inputs for creating End-of-Quarter Checklists
    input_template_file_url = sys.argv[1]
    input_folder_url = sys.argv[2]
    input_qtr_str = sys.argv[3]

    # inputs for generating studio database
    input_studio_db_url = sys.argv[4]
    input_sig_info_sheet_name = sys.argv[5]
    input_proj_info_sheet_name = sys.argv[6]

    main(input_template_file_url, input_folder_url, input_qtr_str,
         input_studio_db_url, input_sig_info_sheet_name, input_proj_info_sheet_name)