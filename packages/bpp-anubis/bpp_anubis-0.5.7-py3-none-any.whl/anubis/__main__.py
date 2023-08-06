# __main__.py
import os
import json
import sys
import multiprocessing
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace

# custom
from anubis import account_splitter
from anubis import feature_splitter
from anubis import arg_parser
from anubis import results
from anubis.parallelizer import command_generator

ANUBIS_ASCII = ("""
                 ♡♡                                               
                ♡♡♡                                                 
              ♡♡ ♡♡♡♡                                               
         ♡♡♡♡♡♡♡♡♡♡♡♡                                               
                 ♡♡♡♡♡                                              
                  ♡♡♡♡♡                                             
               ♡♡♡♡♡♡♡♡♡                                            
              ♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡        ♡♡♡♡♡♡                         
              ♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡ ♡♡♡♡                     
              ♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡                   
          ♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡     ♡♡♡♡♡♡♡♡♡♡                  
♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡       ♡♡♡♡♡     ♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡                 
                                                    ♡♡♡              
          POWERED BY ANUBIS                          ♡♡♡♡            
(and the power of love  Σ>―(〃°ω°〃)♡→)               ♡♡♡♡♡          
                                                      ♡♡♡♡♡         
                                                       ♡♡♡♡         
                                                        ♡♡     """)


def main():
    start = datetime.now()
    print(ANUBIS_ASCII)

    # <editor-fold desc="--- Parse arguments">
    args_known, args_unknown = arg_parser.parse_arguments()
    user_definitions = SimpleNamespace()
    for arg in args_known.D:
        setattr(user_definitions, arg[0].split('=')[0], arg[0].split('=')[1])
    # </editor-fold>

    # <editor-fold desc="--- Set up the output directories for the run">
    # create a dir that will contain results and be exported
    print('--- SETTING UP OUTPUT')
    if not os.path.isdir(args_known.output):
        print(f"\tThe results should go to <{args_known.output}> but it doesn't exist (creating it now)")
        os.makedirs(args_known.output, exist_ok=True)
    else:
        print(f'\tSending the output of this run to <{args_known.output}>')

    if not Path(args_known.aggregate).parent.is_dir():
        print(f"\tThe directory to store <{args_known.aggregate}> doesn't exist (creating it now)")
        Path(args_known.aggregate).parent.mkdir(parents=True, exist_ok=True)
    # </editor-fold>

    # set up the multiple processes
    pool = multiprocessing.Pool(args_known.processes)

    # <editor-fold desc="--- Set up the accounts for the run">
    # get account data available for parallel runs
    print('--- Handling Accounts')
    # the `accounts_data` list looks like this --> [(<run_name>, "user pass"), [<list of feature files>]]
    if hasattr(user_definitions, 'account_file') and hasattr(user_definitions, 'account_section'):
        print(f'\tfile:    <{user_definitions.account_file}>')
        print(f'\tsection: <{user_definitions.account_section}>')
        accounts_data = account_splitter.get_accounts(
            args_known.processes, user_definitions.account_file, user_definitions.account_section)
    elif hasattr(user_definitions, 'account_file') and hasattr(user_definitions, 'env'):
        print('\n--- PARSING ACCOUNTS')
        print(f'\tfile:    <{user_definitions.account_file}>')
        print(f'\tassuming section: <{user_definitions.env}>')
        accounts_data = account_splitter.get_accounts(
            args_known.processes, user_definitions.account_file, user_definitions.env)
    else:
        print('\tusing timestamps, instead of accounts, for output file names')
        # create dummy account data just for the purpose of naming the runs
        accounts_data = [(i+1, 'NONE NONE') for i in range(args_known.processes)]
    # </editor-fold>

    # <editor-fold desc="--- Set up the features">
    # split the features and store as list
    print('\n--- GROUPING FEATURES & ACCOUNTS')
    print(f'\tfeature dir: <{args_known.feature_dir}>')
    print(f'\ttags: <{",".join([t[0] for t in args_known.tags]) if args_known.tags else "(none)"}>')

    # parallel
    feature_groups = feature_splitter.get_test_paths(
        args_known.unit, args_known.feature_dir, args_known.processes, accounts_data)

    # run all the processes and save the locations of the result files
    num_groups = len(feature_groups)
    print(f'\n--- RUNNING <{num_groups} PROCESS{"ES" * int(num_groups > 1)}>')
    result_files = pool.map(command_generator, feature_groups)
    # </editor-fold>

    # <editor-fold desc="--- Combine the results">
    res_string = None
    total = 0
    try:
        print('--- HANDLING RESULTS')
        # create the aggregate file and calculate pass/fail rate
        results.create_aggregate(files=result_files, aggregate_out_file=args_known.aggregate)

        with open(args_known.aggregate) as f:
            res = json.load(f)

        statuses = []
        for feature in res:
            if 'elements' in feature:
                for scenario in feature['elements']:
                    if scenario['type'] != 'background':
                        statuses.append(scenario['status'])

        passed = statuses.count('passed')
        failed = statuses.count('failed')
        total = passed + failed
        res_string = f'{passed / total * 100:.2f}%'
    except Exception as e:
        passed, failed = 0, 0
        if args_known.aggregate:
            print(f'There was an error combining results\n{e}')
        else:
            pass

    if args_known.aggregate.startswith('.temp'):
        os.remove(args_known.aggregate)
    # </editor-fold>

    end = datetime.now()

    # <editor-fold desc="extremely basic summary">
    print('\n===========♡𓃥♡ SUMMARY ♡𓃥♡===========')
    print(f'Env:         <{user_definitions.env}>')
    print(f'Results:     <{args_known.aggregate}>') if hasattr(args_known, 'aggregate') else None
    print(f'Total tests: <{total}>')
    print(f'Pass Rate:   <{res_string if res_string else "could not calculate"}>')
    print(f'Run Time:    <{(end - start)}>')
    print('=======================================')
    # </editor-fold>


if __name__ == '__main__':
    # run everything
    main()
    sys.exit(0)
