import glob
import subprocess
from random import shuffle
from re import search


def get_test_paths(unit, feature_dir, processes, accounts=None):
    paths = __get_paths(feature_dir, unit)
    result = __get_path_groups(paths, processes, accounts)
    return result


def __get_path_groups(paths, num_split, accounts=None, section=None):
    # split as evenly as possible
    inc = -(-len(paths) // num_split)

    # group the paths
    path_groups = [paths[i:i + inc] for i in range(0, len(paths), inc)]
    shuffle(path_groups)

    if accounts:
        return list(zip(accounts, path_groups))

    return list(zip(list(range(len(path_groups))), path_groups))


def __get_paths(feature_dir, unit):
    feature_paths = glob.glob(f'{feature_dir}/**/*.feature', recursive=True)

    if unit.lower() == 'scenario':
        # get all "Scenarios"
        scenario_paths = subprocess.run(
            [f'grep -irn "Scenario:" {" ".join(feature_paths)} | sed s/": .*"/""/'],
            shell=True,
            capture_output=True
        ).stdout.decode('utf-8').split('\n')

        # get all "Examples" and remove the first one to prevent duplicates
        example_paths = subprocess.run(
            [f'grep -rin "Examples\||" {" ".join(feature_paths)}'],
            shell=True,
            capture_output=True
        ).stdout.decode('utf-8').split('\n')

        # remove commented example lines
        example_paths = [path for path in example_paths if not search(r'.*:[0-9]+:#.*', path) and not len(path) == 0]

        # remove first occurrence of a file path to prevent duplicate examples
        example_paths_filtered = []
        i = 0
        while i < len(example_paths):
            if 'Examples' in example_paths[i]:
                i += 2
            else:
                example_paths_filtered.append(example_paths[i].split(': ')[0])
                i += 1
        return scenario_paths + example_paths_filtered

    return feature_paths
