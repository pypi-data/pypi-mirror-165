
import re



def regex_match(pattern, string):
  pattern = re.compile(pattern)
  if re.fullmatch(pattern, string):
    return True
  return False


def check_version(version, schema_df):
  """checks if version conforms to hdruk schema

  Args:
      version (str): version of metadata
      schema_df (pandas df): hdruk schema

  Returns:
      boolean: 
  """
  version_pattern = schema_df['definitions.semver.pattern'].values[0]
  is_version = regex_match(version_pattern, version)
  return is_version