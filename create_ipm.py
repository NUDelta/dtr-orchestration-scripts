"""
This script is used to create Individual Progress Maps for each student in DTR, given a IPM template,
output directory and a list of student names.
"""

import sys
import json
import helpers.imports as helpers
from copy_gdrive_file import copy_file


def generate_ipm(student_list, gdrive_service, template_url, folder_url):
    """
    Generates an Individual Progress Map for each student.

    :param student_list: list of students names to generate IPM for.
    :param gdrive_service: Google Drive v3 authentication object.
    :param template_url: string url of original file to copy.
    :param folder_url: string url of folder to copy file to.
    :return: None
    """
    # iterate over student list and create an IDP for each student
    for student in student_list:
        # generate a filename using the student's first name and last initial
        student_name_split = student.split(" ")
        student_filename = "{first} {lasti}. -- Individual Progress Map".format(first=student_name_split[0],
                                                                               lasti=student_name_split[-1][0])

        # copy original file for each project using student_filename
        curr_copied_file = copy_file(gdrive_service, template_url, folder_url, student_filename)

        # generate a file URL for copied file, and print out
        curr_file_id = curr_copied_file["id"]
        print("{filename}: https://docs.google.com/spreadsheets/d/{id}/edit".format(filename=student_filename,
                                                                                    id=curr_file_id))


def main(template_file_url, folder_url, student_name_list):
    """
    Fetches Studio Database information and uses it to generate Sprint Logs.

    :param template_file_url: string url of original file to copy.
    :param folder_url: string url of folder to copy file to.
    :param student_name_list: list of student names to create files for.
    :return: None
    """
    # authenticate for Google Drive v3 and Google Spreadsheets APIs
    gdrive_service = helpers.auth_gdrive()
    gspreadsheets_service = helpers.auth_gsheets()

    # generate IPMs for each student
    generate_ipm(student_name_list, gdrive_service, template_file_url, folder_url)


if __name__ == '__main__':
    # get command line args
    arg_count = len(sys.argv) - 1

    # check for correct number of arguments
    if arg_count != 3:
        raise Exception("Invalid number of arguments. Expected 3 "
                        "(IPM template URL, IPM folder URL, "
                        "Student List) got {}."
                        .format(arg_count))

    # inputs for creating IPMs
    input_template_file_url = sys.argv[1]
    input_folder_url = sys.argv[2]
    input_student_list = json.loads(sys.argv[3])

    main(input_template_file_url, input_folder_url, input_student_list)
