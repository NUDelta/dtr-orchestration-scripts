"""
This script is used to extract information from the Studio Database Google Spreadsheet for other scripts and tools.
"""

import sys
import json
import helpers.imports as helpers


def fetch_sig_info(spreadsheet, sheet_name):
    """
    Fetches SIG information from Studio Database.

    :param spreadsheet: gspread spreadsheet object for the Studio Database.
    :param sheet_name: string name of sheet where SIG information is stored.
    :return: list of parsed SIG information.
    """
    # open correct worksheet and get all values to parse
    studio_info_worksheet = spreadsheet.worksheet(sheet_name)
    values = studio_info_worksheet.get_all_values()

    # create header mapping object
    header = values[0]
    header_mapping = {
        "SIG Name": "sig_name",
        "SIG Abbreviation": "abbreviation",
        "SIG Heads": "sig_heads",
        "Faculty Mentors": "faculty_mentors",
        "SIG Time": "sig_time",
        "SIG Office Hours Time": "sig_oh_time"
    }

    # create a header index to lookup header_mapping keys by index number
    # track any header vals not including in mapping
    exclude_list = []
    header_index = {}

    for curr_index, curr_val in enumerate(header):
        if curr_val in header_mapping:
            header_index[curr_index] = curr_val
        else:
            exclude_list.append(curr_val)

    if len(exclude_list) > 0:
        print("The following columns were included in the Studio Database Spreadsheet, but not in the header_mapping. "
              "They will not be included in the parsed Studio Database: {}".format(exclude_list))

    # iterate over each row and parse data
    output = []
    for sig in values[1:]:
        # setup an object for holding current sig information
        curr_sig = {
            "sig_name": "",
            "abbreviation": "",
            "sig_heads": [],
            "faculty_mentors": [],
            "sig_time": "",
            "sig_oh_time": ""
        }

        # parse each individual info field
        for index, sig_info in enumerate(sig):
            # check if index is in header_index before proceeding
            if index not in header_index:
                continue

            # if SIG Heads or Faculty Mentors, parse list of people
            if header_index[index] == "SIG Heads" or header_index[index] == "Faculty Mentors":
                person_list = [person_name.strip() for person_name in sig_info.split(",")]
                curr_sig[header_mapping[header_index[index]]].extend(person_list)
            # else, add to appropriate field
            else:
                curr_sig[header_mapping[header_index[index]]] = sig_info.strip()

        # add to output
        output.append(curr_sig)

    # output data
    return output


def fetch_proj_info(spreadsheet, sheet_name):
    """
    Fetches project information from Studio Database.

    :param spreadsheet: gspread spreadsheet object for the Studio Database.
    :param sheet_name: string name of sheet where Project information is stored.
    :return: list of parsed project information.
    """
    # open correct worksheet and get all values to parse
    studio_info_worksheet = spreadsheet.worksheet(sheet_name)
    values = studio_info_worksheet.get_all_values()

    # create header mapping object
    header = values[0]
    header_mapping = {
        "SIG Name": "sig_name",
        "Students": "students",
        "Project Name": "project_name",
        "Sprint Log Link": "sprint_log",
        "PRC Link": "practical_research_canvas",
        "RRC Link": "research_research_canvas"
    }

    # create a header index to lookup header_mapping keys by index number
    # track any header vals not including in mapping
    exclude_list = []
    header_index = {}

    for curr_index, curr_val in enumerate(header):
        if curr_val in header_mapping:
            header_index[curr_index] = curr_val
        else:
            exclude_list.append(curr_val)

    if len(exclude_list) > 0:
        print("The following columns were included in the Studio Database Spreadsheet, but not in the header_mapping. "
              "They will not be included in the parsed Studio Database: {}".format(exclude_list))

    # iterate over each row and parse data
    output = []
    for proj in values[1:]:
        # setup an object for holding current project information
        curr_proj = {
            "sig_name": "",
            "students": [],
            "project_name": "",
            "sprint_log": "",
            "practical_research_canvas": "",
            "research_research_canvas": ""
        }

        # parse each individual info field
        for index, proj_info in enumerate(proj):
            # check if index is in header_index before proceeding
            if index not in header_index:
                continue

            # if Students, parse list of people
            if header_index[index] == "Students":
                person_list = [person_name.strip() for person_name in proj_info.split(",")]
                curr_proj[header_mapping[header_index[index]]].extend(person_list)
            # else, add to appropriate field
            else:
                curr_proj[header_mapping[header_index[index]]] = proj_info.strip()

        # add to output
        output.append(curr_proj)

    # output data
    return output


def create_studio_db_dict(sig_info_list, proj_info_list):
    """
    Creates a studio database dict that combines the parsed SIG and Project info worksheets.

    :param sig_info_list: list of parsed SIG information from Studio Database.
    :param proj_info_list: list of parsed Project information from Studio Database.
    :return: dict of each SIG with all student and project information.
    """
    # create a placeholder output object
    output = {}
    for sig in sig_info_list:
        # add placeholder for all students in SIG and projects
        sig["students"] = []
        sig["projects"] = []

        # get current SIG name and remove from SIG object
        curr_sig_name = sig.pop("sig_name", None)

        # add to output dict
        output[curr_sig_name] = sig

    # add project information
    for proj in proj_info_list:
        # create some local vars
        curr_sig_name = proj["sig_name"]
        curr_proj = {
            "project_name": proj["project_name"],
            "students": proj["students"],
            "documents": {
                "sprint_log": proj["sprint_log"],
                "practical_research_canvas": proj["practical_research_canvas"],
                "research_research_canvas": proj["research_research_canvas"]
            }
        }

        # add students and project
        output[curr_sig_name]["students"].extend(proj["students"])
        output[curr_sig_name]["projects"].append(curr_proj)

    # output studio database dict
    return output


def export_studio_db_as_json(studio_db_dict, output_file):
    """
    Exports Studio Database dict as a json object for other tools.
    To support other tools, the exported json uses a list of SIGs rather than a dictionary where each SIG is a key.

    :param studio_db_dict: dict containing all information for the studio database
    :param output_file: string filepath to output json to.
    :return: json string of studio database dict with correct formatting for external tools.
    """
    # create output object
    output = []

    for sig_name, sig_info in studio_db_dict.items():
        # hold data for current sig
        curr_sig = {
            "name": sig_name,
            "abbreviation": sig_info["abbreviation"],
            "sig_time": sig_info["sig_time"],
            "sig_oh_time": sig_info["sig_oh_time"],
            "sig_heads": sig_info["sig_heads"],
            "faculty_mentors": sig_info["faculty_mentors"],
            "students": sig_info["students"],
            "projects": [{
                "project_name": proj["project_name"],
                "students": proj["students"],
                "documents": {
                    "Sprint Log": proj["documents"]["sprint_log"],
                    "Practical Research Canvas": proj["documents"]["practical_research_canvas"],
                    "Research Research Canvas": proj["documents"]["research_research_canvas"],
                }
            } for proj in sig_info["projects"]]
        }

        # add to output
        output.append(curr_sig)

    # output json to specified file
    with open(output_file, "w") as outfile:
        json.dump(output, outfile, indent=4)

    # return json string
    return json.dumps(output, indent=4)


def main(spreadsheet_url, sig_info_sheet_name, proj_info_sheet_name):
    """
    Generates a Studio Database dict, given a Studio Database spreadsheet.

    :param spreadsheet_url: string url of Studio Database Google Spreadsheet
    :param sig_info_sheet_name: string name of sheet where SIG information is stored.
    :param proj_info_sheet_name: string name of sheet where Project information is stored.
    :return: dict of parsed studio database.
    """
    # authenticate gspread
    gc = helpers.auth_gsheets()

    # get spreadsheet
    curr_spreadsheet = gc.open_by_url(spreadsheet_url)

    # fetch SIG and Project info
    curr_sig_info = fetch_sig_info(curr_spreadsheet, sig_info_sheet_name)
    curr_proj_info = fetch_proj_info(curr_spreadsheet, proj_info_sheet_name)

    # create and output a studio database dict
    return create_studio_db_dict(curr_sig_info, curr_proj_info)


if __name__ == '__main__':
    # get command line args
    arg_count = len(sys.argv) - 1

    # check for correct number of arguments
    if arg_count != 3:
        raise Exception("Invalid number of arguments. Expected 3 "
                        "(Studio Database URL, SIG Info sheet name, Proj Info sheet name) got {}."
                        .format(arg_count))

    # parse each argument
    input_spreadsheet_url = sys.argv[1]
    input_sig_info_sheet_name = sys.argv[2]
    input_proj_info_sheet_name = sys.argv[3]
    json_output_filepath = "studio_db.json"

    # generate studio database dict
    studio_database_dict = main(input_spreadsheet_url, input_sig_info_sheet_name, input_proj_info_sheet_name)

    # export as json and print exported json
    export_studio_db_as_json(studio_database_dict, json_output_filepath)
    print("Studio Database successfully parsed and exported to {}".format(json_output_filepath))
