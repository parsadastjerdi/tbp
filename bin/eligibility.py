import csv
import xlwt
from xlwt import Workbook

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
        full_name = name.split(',').split(' ')
        formatted_names.append(full_name.strip())

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


def generate_xlsx(names, majors, email, classification):
    '''
    Generates a new, formatted spreadsheet from the original spreadsheet
    Args:
    Returns:
    '''
    wb = Workbook()

    juniors = wb.add_sheet('Juniors')
    # seniors = wb.add_sheet('Seniors')

    juniors.a


def generate_csv(names, majors, email, classification):
    '''
    Generates a CSV with all candidates
    Args:
    Returns:
    '''


'''
if __name__ == '__main__':
    # juniors = open('../tests/juniors.csv', 'r')
    # seniors = open('../tests/seniors.csv', 'r')
    # grads = open('../tests/graduates.csv', 'r')

    outfile = open('../tests/students.csv', 'a')

    with open('../tests/juniors.csv','r') as juniors: 
        # print(majors)
        # sheet = EligibilitySheet(juniors=juniors, seniors=seniors, graduates=grads, outfile=outfile)
'''



