"""
This script is used to create Sprint Logs for each student in DTR, given a Sprint Log template, output directory, and
studio database with student and project information.
"""

import sys
import helpers.imports as helpers
import studio_db_to_json as studio_db
from copy_gdrive_file import copy_file


def generate_sprint_logs(studio_db_dict, gdrive_service, template_url, folder_url):
    """
    Generates a Sprint Log for each project.

    :param studio_db_dict: dict of each SIG with all student and project information.
    :param gdrive_service: Google Drive v3 authentication object.
    :param template_url: string url of original file to copy.
    :param folder_url: string url of folder to copy file to.
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
            curr_filename = "[{abb}] {proj}".format(abb=curr_sig_abb, proj=curr_proj_name)

            # copy original file for each project using curr_filename
            curr_copied_file = copy_file(gdrive_service, template_url, folder_url, curr_filename)

            # generate a file URL for copied file, and print out
            curr_file_id = curr_copied_file["id"]
            print("Sprint Log for {proj}: https://docs.google.com/spreadsheets/d/{id}/edit".format(proj=curr_filename,
                                                                                                   id=curr_file_id))


def main(template_file_url, folder_url, studio_db_url, sig_info_sheet_name, proj_info_sheet_name):
    """
    Fetches Studio Database information and uses it to generate Sprint Logs.

    :param template_file_url: string url of original file to copy.
    :param folder_url: string url of folder to copy file to.
    :param studio_db_url: string url of Studio Database Google Spreadsheet
    :param sig_info_sheet_name: string name of sheet where SIG information is stored.
    :param proj_info_sheet_name: string name of sheet where Project information is stored.
    :return:
    """
    # authenticate for Google Drive v3 and Google Spreadsheets APIs
    gdrive_service = helpers.auth_gdrive()
    gspreadsheets_service = helpers.auth_gsheets()

    # generate studio database
    studio_db_spreadsheet = gspreadsheets_service.open_by_url(studio_db_url)
    sig_info_list = studio_db.fetch_sig_info(studio_db_spreadsheet, sig_info_sheet_name)
    proj_info_list = studio_db.fetch_proj_info(studio_db_spreadsheet, proj_info_sheet_name)
    studio_db_dict = studio_db.main(studio_db_url, sig_info_sheet_name, proj_info_sheet_name)

    # generate sprint logs for each project
    generate_sprint_logs(studio_db_dict, gdrive_service, template_file_url, folder_url)


if __name__ == '__main__':
    # get command line args
    arg_count = len(sys.argv) - 1

    # check for correct number of arguments
    if arg_count != 5:
        raise Exception("Invalid number of arguments. Expected 5 "
                        "(Sprint Log template URL, Sprint Log folder URL, "
                        "Studio Database URL, SIG Info sheet name, Proj Info sheet name) got {}."
                        .format(arg_count))

    # inputs for creating Sprint Logs
    input_template_file_url = sys.argv[1]
    input_folder_url = sys.argv[2]

    # inputs for generating studio database
    input_studio_db_url = sys.argv[3]
    input_sig_info_sheet_name = sys.argv[4]
    input_proj_info_sheet_name = sys.argv[5]

    main(input_template_file_url, input_folder_url,
         input_studio_db_url, input_sig_info_sheet_name, input_proj_info_sheet_name)