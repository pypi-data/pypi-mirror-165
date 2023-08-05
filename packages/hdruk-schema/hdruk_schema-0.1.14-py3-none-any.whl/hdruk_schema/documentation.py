
import validators
from termcolor import colored
import re





def check_length(property, min_length, max_length):
  """checks the length of a property

  Args:
      property (str): hdruk property to check
      min_length (int): minimum acceptable length of the property
      max_length (int): maximum acceptable length of the property

  Returns:
      boolean: 
  """
  if len(property) >= min_length and len(property) <= max_length:
    return True
  return False

def is_in_list(item, list):
  if item in list:
    return True
  return False

def regex_match(pattern, string):
  pattern = re.compile(pattern)
  if re.fullmatch(pattern, string):
    return True
  return False


def validate_documentation(documentation):
  """validates documentation property of hdruk

  Args:
      documentation (dict): hdruk property

  Returns:
      dict: 
  """

  not_available = 'NA'
  is_valid = {}

  for k,v in documentation.items():

    if k == 'description':
      result = isinstance(v, str) and check_length(v, 2, 3000)
      if result:
        is_valid[k] = True
      else:
        is_valid[k] = False
    # else:
    #   is_valid['description'] = not_available


    if k == 'associatedMedia':
      result = isinstance(v, list) and validators.url(v[0])
      if result:
        is_valid[k] = True
      else:
        is_valid[k] = False
    # else:
    #   is_valid['associatedMedia'] = not_available



    if k == 'isPartOf':
      result = isinstance(v, str) and check_length(v, 2, 80)
      if result:
        is_valid[k] = True
      else:
        is_valid[k] = False
    # else:
    #   is_valid['isPartOf'] = not_available


  return is_valid
    
def check_documentation(documentation, schema_df):
  """compares the documentation property to hdruk schema

  Args:
      documentation (dict): 
      schema_df (pandas df): 

  Returns:
      dict: 
  """
  

  is_valid = validate_documentation(documentation)

  # print(u'\u2713')
  return is_valid
      # if isinstance(v, str) and check_length(v, 2, 80):
        # result = True
