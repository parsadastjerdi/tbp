from xlwt import Workbook
import pandas as pd
from datetime import datetime

# TODO: don't include grad students if they're included in the spreadsheet

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
        formatted_names.append((last_name, first_name, middle_name))
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



def generate_xlsx(candidates, **kwargs):
    '''
    Generates a new, formatted spreadsheet from the original spreadsheet
    Args:
    Returns:
    '''
    wb = Workbook()
    NUM_CANDIDATES = len(candidates['names'])

    sheet = wb.add_sheet('Candidates')

    sheet.write(0, 0, 'First Name')
    sheet.write(0, 1, 'Middle Name')
    sheet.write(0, 2, 'Last Name')
    sheet.write(0, 3, 'Classification')
    sheet.write(0, 4, 'Grad Month')
    sheet.write(0, 5, 'Grad Year')
    sheet.write(0, 6, 'Major')
    sheet.write(0, 7, 'Email')

    # i + 1 so that the titles don't get overwritten
    for i in range(NUM_CANDIDATES):
        sheet.write(i + 1, 0, candidates['names'][i][1])
        sheet.write(i + 1, 1, candidates['names'][i][2])
        sheet.write(i + 1, 2, candidates['names'][i][0])
        sheet.write(i + 1, 3, candidates['class'][i])
        sheet.write(i + 1, 4, 'May')
        sheet.write(i + 1, 5, candidates['grad_year'][i])
        sheet.write(i + 1, 6, candidates['majors'][i])
        sheet.write(i + 1, 7, candidates['email'][i])

    path = '../results/candidates.xls'
    wb.save(path)
    print('Candidate information saved in ', path)


if __name__ == '__main__':
    candidates = pd.read_csv('../tests/juniors.csv')

    cand = {
        'names': parse_names(candidates['Name']),
        'majors': parse_majors(candidates['Major']),
        'email': candidates['Email'],
        'class': parse_class(candidates['Class']),
        'grad_year': get_grad_year(candidates['Class'])
    }

    generate_xlsx(candidates=cand)                    
