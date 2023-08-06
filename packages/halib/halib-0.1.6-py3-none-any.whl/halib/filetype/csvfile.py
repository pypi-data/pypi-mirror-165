import pandas as pd
from tabulate import tabulate
from rich.console import Console
from rich import print as rprint
from rich import inspect
from rich.pretty import pprint
from tqdm import tqdm
from loguru import logger

console = Console()

def read(file, separator=","):
    df = pd.read_csv(file, separator)
    return df


# for append, mode = 'a'
def write(df, outfile, mode='w', header=True, index_label=None):
    if not outfile.endswith('.csv'):
        outfile = f'{outfile}.csv'
    if index_label is not None:
        df.to_csv(outfile, mode=mode, header=header, index_label=index_label)
    else:
        df.to_csv(outfile, mode=mode, header=header, index=False)


def make_df_with_columns(columns):
    df = pd.DataFrame(columns=columns)
    return df


def insert_row(df, row_dict_or_list):
    if isinstance(row_dict_or_list, list):
        new_row_df = pd.DataFrame([row_dict_or_list], columns=df.columns)
        df = pd.concat([df, new_row_df], ignore_index=True)
        return df
    elif isinstance(row_dict_or_list, dict):
        df = df.append(row_dict_or_list, ignore_index=True)
        return df
    else:
        raise ValueError('invalid row data')


def display_df(df):
    print(tabulate(df, headers='keys', tablefmt='psql', numalign="right"))


def config_display_pd(max_rows=None, max_columns=None,
                      display_width=1000, col_header_justify='center',
                      precision=10):
    pd.set_option('display.max_rows', max_rows)
    pd.set_option('display.max_columns', max_columns)
    pd.set_option('display.width', display_width)
    pd.set_option('display.colheader_justify', col_header_justify)
    pd.set_option('display.precision', precision)



class DFCreator(dict):
    """docstring for ClassName."""
    
    def __init__(self,*arg,**kw):
      super(DFCreator, self).__init__(*arg, **kw)
      
    def create_table(self, table_name, columns):
        self[table_name] = pd.DataFrame(columns=columns)
    
    def insert_row(self, table_name, row_dict_or_list):
        assert len(self[table_name].columns) == len(row_dict_or_list), 'invalid row data'
        self[table_name] = insert_row(self[table_name], row_dict_or_list)
    
    def display_table(self, table_name):
        display_df(self[table_name])
    
    def write_table(self, table_name, outfile, mode='w', header=True, index_label=None):
        write(self[table_name], outfile, mode, header, index_label)
    
    
    def display_table_schema(self, table_name):
        columns = list(self[table_name].columns)
        console.print(f'TABLE {table_name}: {columns}', style='bold blue')
    
    def display_all_table_schema(self):
       table_names = list(self.keys())
       for table_name in table_names:
           self.display_table_schema(table_name)
           
    def display_all_table(self):
        for table_name in self.keys():
            console.rule(table_name)
            display_df(self[table_name])
    def write_all_table(self, output_dir, mode='w', header=True, index_label=None):
        for table_name in self.keys():
            outfile = f'{output_dir}/{table_name}.csv'
            write(self[table_name], outfile, mode, header, index_label)
            

    