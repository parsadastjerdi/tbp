from xlwt import Workbook
import pandas as pd
from datetime import datetime
import sys


def parse_names(names):
    '''
    Parses names in the format 'last, first middle' into an array with three elements. This list is appended 
    as an element to the formatted_names array and passed back. 
    Args:
        Name in the format 'last, first middle'
    Returns:
        Array with three elements, each element contains a name
    '''

    formatted_names = []

    for name in names:
        (last_name, first_middle) = name.split(',')
        (first_name, middle_name) = first_middle.split(' ', 1)
        formatted_names.append((first_name, middle_name, last_name))
    return formatted_names



def parse_majors(majors):
    '''
    Converts major from TAMU format to TBP format
    Args:
        A list of strings that contains the major in an acronym (ELEN, BMEN, MEEN, CHEN, ..)
    Returns:
        A list of strings that contains the TBP official representation for that major.
        If the major is unavailable, then the person is assigned "Safety Engineering".
    '''

    formatted_majors = []

    for major in majors:
        if major == 'AERO':
            formatted_majors.append('Aerospace engg')
        elif major == 'BAEN':
            formatted_majors.append('Biological & agricultural engg')
        elif major == 'BMEN':
            formatted_majors.append('Biomedical engg')
        elif major == 'CHEN':
            formatted_majors.append('Chemical engg')
        elif major == 'CVEN':
            formatted_majors.append('Civil engg')
        elif major == 'CECN' or major == 'CEEN' or major == 'CPSC':
            formatted_majors.append('Computer engg')
        elif major == 'ELEN' or major == 'ESET':
            formatted_majors.append('Electrical engg')
        elif major == 'ISEN' or major == 'INEN' or major == 'IDIS':
            formatted_majors.append('Industrial engg')
        elif major == 'MEEN':
            formatted_majors.append('Mechanical engg')
        elif major == 'MMET':
            formatted_majors.append('Materials science & engg')
        elif major == 'NUEN':
            formatted_majors.append('Nuclear engg')
        elif major == 'OCEN':
            formatted_majors.append('Ocean engg')
        elif major == 'PETE':
            formatted_majors.append('Petroleum engg')
        elif major == 'RHEN':
            formatted_majors.append('Radiological health engg')
        else:
            formatted_majors.append('Safety engg')
    
    return formatted_majors



def parse_class(class_list):
    '''
    Returns an array of classifications based on the input 
    Graduate students who intend to join need to have their information directly 
    Args:
    Returns:
    '''

    formatted_class = []

    for classification in class_list:
        if classification == 'U3':
            formatted_class.append('Junior')
        elif classification == 'U4':
            formatted_class.append('Senior')
    
    return formatted_class



def remove_members(candidates, members):
    '''
    Removes all current members from the candidate list using unique email address
    Args:
        candidates: Pandas Dataframe containing information on all candidates
        members: Pandas Dataframe of all current members
    Returns:
        Pandas Dataframe of all candidates with current members removed
    '''

    member_emails = []
    candidate_emails = []

    # removed domain names from email due to differences between email.tamu.edu and tamu.edu
    for email in members['Email']:
        if not pd.isnull(email):
            name, domain = email.split('@')
            if 'qatar' not in domain:
                member_emails.append(name)

    for email in candidates['Email']:
        if not pd.isnull(email):
            name, domain = email.split('@')
            if 'qatar' not in domain:
                candidate_emails.append(name)
        
    for i, email in enumerate(candidate_emails):
        if email in member_emails:
            candidates.drop(i, inplace=True)

    candidates.reset_index(inplace=True)
    return candidates



def get_grad_year(classification_list):
    '''
    Returns a graduation year based on what the candidates classification is
    Args:
    Returns:
    '''

    grad_years = []

    YEAR = datetime.today().year
    MONTH = datetime.today().month

    for classification in classification_list:
        # If junior in spring semester
        if classification == 'U3' and MONTH < 6:
            grad_years.append(YEAR + 1)

        # if junior in fall semester
        elif classification == 'U3' and MONTH >= 6:
            grad_years.append(YEAR + 2)

        # if senior in spring semester
        elif classification == 'U4' and MONTH < 6:
            grad_years.append(YEAR)

        # if senior in fall semester
        elif classification == 'U4' and MONTH >= 6:
            grad_years.append(YEAR + 1)

    return grad_years


def generate_xls(candidates, classification, **kwargs):
    '''
    Generates a new, formatted spreadsheet from the original spreadsheet (based on classification)
    Args:
    Returns:
    '''

    wb = Workbook()
    NUM_CANDIDATES = len(candidates['names'])

    sheet = wb.add_sheet(classification)

    sheet.write(0, 0, 'First Name')
    sheet.write(0, 1, 'Middle Name')
    sheet.write(0, 2, 'Last Name')
    sheet.write(0, 3, 'Class')
    sheet.write(0, 4, 'Grad Month')
    sheet.write(0, 5, 'Grad Year')
    sheet.write(0, 6, 'Major')
    sheet.write(0, 7, 'Present Member')
    sheet.write(0, 8, 'Email')

    # i + 1 so that the titles don't get overwritten
    for i in range(NUM_CANDIDATES):
        sheet.write(i + 1, 0, candidates['names'][i][0])
        sheet.write(i + 1, 1, candidates['names'][i][1])
        sheet.write(i + 1, 2, candidates['names'][i][2])
        sheet.write(i + 1, 3, candidates['class'][i])
        sheet.write(i + 1, 4, 'May')
        sheet.write(i + 1, 5, candidates['grad_year'][i])
        sheet.write(i + 1, 6, candidates['majors'][i])
        sheet.write(i + 1, 8, candidates['email'][i])

    path = '../results/' + classification + '.xls'
    wb.save(path)
    print('Candidate information saved in ', path)



if __name__ == '__main__':
    total_candidates = 0

    try:
        members = pd.read_csv('../spreadsheets/members.csv')
    except:
        print('Please copy over all current members into /spreadsheets/members.csv')
        sys.exit(1)
    
    try:
        junior = pd.read_csv('../spreadsheets/juniors.csv')
    except:
        print('Please place all juniors into /spreadsheets/juniors.csv')
        sys.exit(1)

    juniors = remove_members(junior, members)

    juniors = {
        'names': parse_names(juniors['Name']),
        'majors': parse_majors(juniors['Major']),
        'email': juniors['Email'],
        'class': parse_class(juniors['Class']),
        'grad_year': get_grad_year(juniors['Class'])
    }

    generate_xls(candidates=juniors, classification='juniors')  

    try:
        senior = pd.read_csv('../spreadsheets/seniors.csv')
    except:
        print('Please place all seniors into /spreadsheets/seniors.csv')
        sys.exit(1)

    seniors = remove_members(senior, members)

    seniors = {
        'names': parse_names(seniors['Name']),
        'majors': parse_majors(seniors['Major']),
        'email': seniors['Email'],
        'class': parse_class(seniors['Class']),
        'grad_year': get_grad_year(seniors['Class'])
    }    

    generate_xls(candidates=seniors, classification='seniors')    
    print('Eligible seniors:', len(seniors['email']), '/', len(seniors['email']) * 5)
    print('Eligible juniors:', len (juniors['email']), '/', len(juniors['email']) * 8)
    print('Total number of candidates:', len(seniors['email']) + len(juniors['email']))
    print('Total number of current members:', len(members['Email']))            
