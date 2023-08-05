



import validators
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


def validate_revisions(revisions):

  for k,v in revisions.items():

    if k == 'version':
        pattern = r'^([0-9]+)\.([0-9]+)\.([0-9]+)$'
        result = regex_match(pattern, v)

    if k == 'url':
      result = isinstance(v, str) and validators.url(v)


def check_revisions(df, schema_df):
  

  # print(df.keys())
  # print("df: ", df)
  
  # revisions = df['summary'].iloc[2]['revisions']
  revisions = df['revisions']

  validate_revisions(revisions)
      # if isinstance(v, str) and check_length(v, 2, 80):
        # result = True
