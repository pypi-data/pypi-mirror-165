from .accessibility import check_accessibility
from .documentation import check_documentation
from .identifier import check_identifier
from .revisions import check_revisions
from .summary import check_summary
from .version import check_version
from .issued import check_issued
from .modified import check_modified
from .observations import check_observations
from collections import defaultdict
import pandas as pd
import json
from termcolor import colored
from prettytable import PrettyTable




def parse_series(series):
    """preprocess and cleans a hdruk property (column) 

    Args:
        series (pandas series): 

    Returns:
        pandas dataframe: clean hdruk property
    """
    df_list = defaultdict(list)
    nrows = series.shape[0]

    for i in range(nrows):
        try:
            # if not series.iloc[i].keys():
            for k, v in zip(series.iloc[i].keys(), series.iloc[i].values()):
                df_list[k].append(v)
        except:
            pass
            # df_list.append('NA') 
    
    df = pd.DataFrame.from_dict(dict(df_list.items()), orient='index').T
    
    return df



def parse_json_file(metadata_path, data_model_col='dataModels'):
    """loads a hdruk schema metadata json file 

    Args:
        metadata_path (str): filepath to hdruk metadata (has to be a json file)
        data_model_col (str, optional): column that contains the hdruk property. Defaults to 'dataModels'.

    Returns:
        pandas dataframe: 
    """

    df_json = pd.read_json(metadata_path)

    data_models = df_json[data_model_col]
    df_list = defaultdict(list)
    nrows = data_models.shape[0]

    for i in range(nrows):
      for k, v in zip(data_models.iloc[i].keys(), data_models.iloc[i].values()):
        df_list[k].append(v)
    
    df = pd.DataFrame.from_dict(dict(df_list.items()), orient='index').T
    
    return df

# df = parse_json_file(metadata_path)

def load_schema(schema_file_path):
    """loads hdruk schema json file into a dataframe

    Args:
        schema_file_path (str): file path to hdruk schema json file

    Returns:
        pandas dataframe: hdruk schema
    """
    # schema_path = "dataset.schema.json"

    with open(schema_file_path, 'r') as j:
        schema_contents = json.loads(j.read())

    schema_df = pd.json_normalize(schema_contents)

    return schema_df


def validate_property(df, schema_df, col, validator):
        """

        Args:
            df (pandas dataframe): hdruk metadata
            schema_df (pandas dataframe): hdruk schema
            col (str): column name (hdruk property) to validate
            validator (function): python function to use to validate the property

        Returns:
            dict: 
        """
        
        print()
        print()
        print(colored(f'Checking {col} for conformity with hdruk schema', 'blue'))

        result = df[col].apply((lambda x: validator(x, schema_df)))

        print(colored(f"Checking {col} complete", 'green'), colored(u'\u2713', 'green'))
      
        return result




def schema_validator(metadata_path, schema_file_path):
     """compares hdruk metadata to hdruk schema 

        Args:
            metadata_path (str): file path to hdruk metadata
            schema_file_path (str): file path to hdruk schema

        Returns:
            dict: result of validation
     """
     df = parse_json_file(metadata_path)
     schema_df = load_schema(schema_file_path)
     checklist = list(df.columns)
     validated_dict = {}

     for col in checklist:
        

        if col == 'identifier':
            result = validate_property(df, schema_df, col, check_identifier)
            validated_dict[col] = result
            na_list = result[result!=True].index.tolist()
            
            my_table = PrettyTable()
            my_table.field_names = ["Property", "No of non-conforming rows"]

            if len(na_list) == 0:
                my_table.add_row(["identifier", "None"])
            else:
                my_table.add_row(["identifier", len(na_list)])

            print(my_table)



        if col == 'version':
            result = validate_property(df, schema_df, col, check_version)
            validated_dict[col] = result

            my_table = PrettyTable()
            my_table.field_names = ["Property", "No of non-conforming rows"]

            if len(na_list) == 0:
                my_table.add_row(["version", "None"])
            else:
                my_table.add_row(["version", len(na_list)])

            print(my_table)


        if col == 'documentation':
            result = validate_property(df, schema_df, col, check_documentation)
            validated_dict[col] = result
            documentation = parse_series(result)
            na_dict ={}
            for i in documentation.columns:
                # print(i)
                na_list = documentation[documentation[i]!=True].index.tolist()
                na_dict[i] = na_list
            # print(na_dict.keys())
            description_list = na_dict['description']
            associatedMedia_list = na_dict['associatedMedia']
            isPartOf_list = na_dict['isPartOf']
            
            my_table = PrettyTable()
            my_table.field_names = ["Property", "No of non-conforming rows"]
            my_table.add_row(["description", len(description_list)])
            my_table.add_row(["associatedMedia", len(associatedMedia_list)])
            my_table.add_row(["isPartOf", len(isPartOf_list)])
            print(my_table)
                        



        if col == 'accessibility':
            result = validate_property(df, schema_df, col, check_accessibility)
            validated_dict[col] = result 


            accessibility = parse_series(result)
            usage = parse_series(accessibility['usage'])
            formatAndStandards = parse_series(accessibility['formatAndStandards'])
            access = parse_series(accessibility['access'])

            na_dict ={}
            for i in usage.columns:
                # print(i)
                na_list = usage[usage[i]!=True].index.tolist()
                na_dict[i] = na_list

            for i in formatAndStandards.columns:
                # print(i)
                na_list = formatAndStandards[formatAndStandards[i]!=True].index.tolist()
                na_dict[i] = na_list

            for i in access.columns:
                # print(i)
                na_list = access[access[i]!=True].index.tolist()
                na_dict[i] = na_list

            
            my_table = PrettyTable()
            my_table.field_names = ["Property", "No of non-conforming rows"]

            for i in na_dict.keys():
                # print(len(na_dict[i]))
                my_table.add_row([i, len(na_dict[i])])

                # print(na_dict[i]) 
            print(my_table)      

     return validated_dict


























        # if col == 'issued':
        #     result = validate_property(df, schema_df, col, check_issued)
        #     validated_dict[col] = result
        #     na_list = result[result!=True].index.tolist()
            
        #     my_table = PrettyTable()
        #     my_table.field_names = ["Property", "No of non-conforming rows"]

        #     if len(na_list) == 0:
        #         my_table.add_row(["issued", "None"])
        #     else:
        #         my_table.add_row(["issued", len(na_list)])

        #     print(my_table)


        # if col == 'modified':
        #     result = validate_property(df, schema_df, col, check_modified)
        #     validated_dict[col] = result
        #     na_list = result[result!=True].index.tolist()
            
        #     my_table = PrettyTable()
        #     my_table.field_names = ["Property", "No of non-conforming rows"]

        #     if len(na_list) == 0:
        #         my_table.add_row(["modified", "None"])
        #     else:
        #         my_table.add_row(["modified", len(na_list)])

        #     print(my_table)

        # if col == 'revisions':
        #     result = validate_property(df, schema_df, col, check_revisions)
        #     validated_dict[col] = result
        #     na_list = result[result!=True].index.tolist()
            
        #     my_table = PrettyTable()
        #     my_table.field_names = ["Property", "No of non-conforming rows"]

        #     if len(na_list) == 0:
        #         my_table.add_row(["revisions", "None"])
        #     else:
        #         my_table.add_row(["revisions", len(na_list)])

        #     print(my_table)

