from .arg_parser import parse_arguments
import os
from subprocess import call


def command_generator(account_feature_groups: list) -> str:
    """
    Use args, accounts, and features to construct behave command
    :param account_feature_groups:
    :return:
    """
    # get arguments
    known_args, unknown_args = parse_arguments()

    # construct the behave command
    process_name = account_feature_groups[0][0]
    results_json_file = os.path.join(known_args.output, f'{process_name}.json')
    defined_args_formatted = ' '.join('-D {}'.format(arg[0]) for arg in known_args.D) if known_args.D else ''
    unknown_args_formatted = ' '.join(arg for arg in unknown_args)
    tags_formatted = ' '.join('--tags="{}" '.format(tags[0].replace("@", "")) for tags in known_args.tags)
    scenarios = ' '.join(scenario for scenario in account_feature_groups[1])
    output_file = f'-f json -o "output/{process_name}.json"'

    command = f'behave -D parallel=true -D pgi={process_name} ' \
              f'{defined_args_formatted} {unknown_args_formatted} {tags_formatted} {output_file} {scenarios}'

    print(command, end='\n\n')
    r = call(command, shell=True)
    return results_json_file
