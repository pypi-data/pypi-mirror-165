
import re
import validators
from validate_email import validate_email




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


def validate_summary_title(title, schema_df):
    """checks if title property conforms to hdruk schema 

    Args:
        title (str): title of metadata
        schema_df (pandas df): hdruk schema

    Returns:
        boolean: 
    """
    # title_min_length = schema_df['definitions.eightyCharacters.minLength'].iloc[0]
    # title_type = schema_df['definitions.eightyCharacters.type'].iloc[0]
    # title_max_length = schema_df['definitions.eightyCharacters.maxLength'].iloc[0]
    if isinstance(title, str) and check_length(title, 2, 80):
        return True
    return False


  
def validate_summary_abstract(df, schema_df): #row
  """checks if abstract property conforms to hdruk schema 

    Args:
        abstract (str): abstract of metadata
        schema_df (pandas df): hdruk schema

    Returns:
        boolean: 
  """
  abstract = df['summary'].iloc[0]['abstract']
  # title = row['title']
  abstract_min_length = schema_df['definitions.abstractText.minLength'].iloc[0]
  abstract_type = schema_df['definitions.abstractText.type'].iloc[0]
  abstract_max_length = schema_df['definitions.abstractText.maxLength'].iloc[0]
  if isinstance(abstract, str) and check_length(abstract, abstract_min_length, abstract_max_length):
    return True
  return False


def validate_summary_publisher(publisher, schema_df):
  """checks if publisher property conforms to hdruk schema 

    Args:
        publisher (str): publisher of metadata
        schema_df (pandas df): hdruk schema

    Returns:
        dict: 
  """

  for k,v in publisher.items():
    if k in ['identifier', 'logo', 'accessRights']:
      result = validators.url(v)
    if k == 'name':
      result = isinstance(v, str) and check_length(v, 2, 80)
    if k == 'description':
      result = isinstance(v, str) and check_length(v, 2, 3000)
    if k == 'contactPoint':
      result = validate_email(v) # validate_email('example@example.com',verify=True)

    if k == 'memberOf':
      memberOfList = schema_df['definitions.memberOf.enum']
      result = is_in_list(v, memberOfList)
    if k == 'deliveryLeadTime':
      deliveryLeadTimeList = schema_df['definitions.deliveryLeadTime.enum']
      result = is_in_list(v, deliveryLeadTimeList)
    if k == 'accessService':
      result = isinstance(v, str) and check_length(v, 2, 5000)

    if k == 'accessRequestCost':
      result = isinstance(v, str) and check_length(v, 2, 1000)

    if k in ['dataUseLimitation', 'dataUseRequirements']:
      pattern = r'([^,]+)'
      result = regex_match(pattern, v)

def validate_summary_keywords(keywords, schema_df):
    """checks if keywords property conforms to hdruk schema 

      Args:
          keywords (str): keywords of metadata
          schema_df (pandas df): hdruk schema

      Returns:
          boolean: 
    """

    # keywords = df['summary'].iloc[2]['keywords']

    if isinstance(keywords, list):
      return True

    if isinstance(keywords, str):
      pattern = r'([^,]+)'
      result = regex_match(pattern, keywords)
      if result:
        return True


def validate_summary_alternateIdentifiers(alternateIdentifiers, schema_df):
    """checks if alternateIdentifiers property conforms to hdruk schema 

        Args:
            alternateIdentifiers (str): alternateIdentifiers of metadata
            schema_df (pandas df): hdruk schema

        Returns:
            boolean: 
    """

    # alternateIdentifiers = df['summary'].iloc[2]['alternateIdentifiers']

    if isinstance(alternateIdentifiers, list):
      return True

    if isinstance(alternateIdentifiers, str):
      pattern = r'([^,]+)'
      result = regex_match(pattern, alternateIdentifiers)
      if result:
        return True


def validate_summary_doiName(doiName, schema_df):
    """checks if doiName property conforms to hdruk schema 

        Args:
            doiName (str): doiName of metadata
            schema_df (pandas df): hdruk schema

        Returns:
            boolean: 
    """
    # alternateIdentifiers = df['summary'].iloc[2]['alternateIdentifiers']

    if isinstance(doiName, str):
      pattern = r'^10.\d{4,9}/[-._;()/:a-zA-Z0-9]+$'
      result = regex_match(pattern, doiName)
      if result:
        return True



def validate_summary(summary, schema_df):
    """checks if summary property conforms to hdruk schema 

        Args:
            summary (str): summary of metadata
            schema_df (pandas df): hdruk schema

        Returns:
            dict: 
    """
    for k,v in summary.items():

      if k == 'title':
        title = summary['title']
        validate_summary_title(title, schema_df)

      if k == 'abstract':
        abstract = summary['abstract']
        validate_summary_abstract(abstract, schema_df)


    if k == 'publisher':
      publisher = summary['publisher']

      validate_summary_publisher(publisher, schema_df)


    if k == 'contactPoint':
        contactPoint = summary['contactPoint']
        is_valid = validate_email(contactPoint)

    #   validate_summary_contactPoint(contactPoint)


    if k == 'keywords':
      keywords = summary['keywords']

      validate_summary_keywords(keywords, schema_df)


    if k == 'alternateIdentifiers':
      alternateIdentifiers = summary['alternateIdentifiers']

      validate_summary_alternateIdentifiers(alternateIdentifiers, schema_df)

    if k == 'doiName':
      doiName = summary['doiName']

      validate_summary_doiName(doiName)



    
def check_summary(df, schema_df):
  """checks if summary property conforms to hdruk schema 

        Args:
            df (pandas df): metadata df
            schema_df (pandas df): hdruk schema

        Returns:
            boolean: 
    """ 

  summary = df['summary'].iloc[2]['summary']

  validate_summary(summary)






# def check_summary_publisher(df, schema_df):

#   publisher = df['summary'].iloc[2]['publisher']

#   validate_publisher(publisher)

      # if isinstance(v, str) and check_length(v, 2, 80):
        # result = True
