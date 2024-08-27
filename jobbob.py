#!/usr/bin/env python3

import os
import sys
import datetime
import glob
import shutil
import pickle
from typing import List, Dict
import argparse
from AaronTools.geometry import Geometry
from AaronTools.fileIO import FileReader, read_types
import numpy as np
np.float = float


class LeafDirectory:
    def __init__(self, dirname: str):
        self.name: str = dirname
        self.logs: List[str] = glob.glob(f"{self.name}/*.log")
        self.log_details: Dict[str, List[str]] = dict()
        self.detail_log_completion()
        # self.detail_log_dinuclearity()
    
    def detail_log_completion(self) -> None:
        self.log_details["complete"] = list()
        self.log_details["incomplete"] = list()
        for log in self.logs:
            with open(log, 'r') as f:
                lastline: str = f.read().splitlines()[-1]
                if "Normal termination of Gaussian" in lastline:
                    self.log_details["complete"].append(log)
                else:
                    self.log_details["incomplete"].append(log)

    def detail_log_dinuclearity(self) -> None:
        self.log_details["dinuclear"] = list()
        for log in self.logs:
            logreader: FileReader = FileReader(log, just_geom=False)
            loggeom: Geometry = Geometry(logreader, refresh_connected=True, refresh_ranks=False)
            pd_list: List[Atom] = loggeom.find("Pd")
            if len(pd_list) > 1:
                self.log_details["dinuclear"].append(log)
    
    def delete_subdirs(self):
        subdirs: List[str] = glob.glob(f"{self.name}*/")
        for subdir in subdirs:
            shutil.rmtree(subdir)
    
    def get_name(self) -> str: return self.name

    def get_logs(self) -> List[str]: return self.logs

    def get_log_detail(self, key: str) -> List[str]: return self.log_details[key]

    def __repr__(self) -> str: return f"LeafDirectory(name:\'{self.name}\',logs:{self.logs},log_details:{self.log_details})" 


class BranchDirectory:
    def __init__(self, dirname: str, leaf_pattern: str):
        self.name: str = dirname
        self.leaves: List[LeafDirectory] = self._find_leaves(leaf_pattern)
    
    def _find_leaves(self, leaf_pattern: str) -> List[LeafDirectory]:
        leaves: List[LeafDirectory] = list()
        leafnames: List[str] = glob.glob(f"{leaf_pattern}/*/")
        for leafname in leafnames:
            leaves.append(LeafDirectory(leafname))
        return leaves
    
    def get_name(self) -> str: return self.name

    def get_leaves(self) -> List[LeafDirectory]: return self.leaves

    def get_leaf_detail(self, detail: str) -> List[str]:
        detail_list: List[str] = list()
        for leaf in self.leaves:
            detail_list.extend(leaf.get_log_detail(detail))
        return detail_list

    def __repr__(self) -> str: return f"BranchDirectory(name:\'{self.name}\',leaves:{self.leaves})"


parser = argparse.ArgumentParser(
    prog="jobbob.py",
    description="Gives info on, sorts, and runs Gaussian jobs",
    epilog="Que sais-je?"
)
parser.add_argument("directory", help="directory to be processed")
parser.add_argument("-i", "--info", dest="actions", action="append_const", const="info", help="prints job and log files status")
parser.add_argument("-s", "--sort", dest="actions", action="append_const", const="sort", help="sorts subdirectories by success or failure of the files within")
parser.add_argument("--custom", dest="actions", action="append_const", const="custom", help="perform a custom action")


if __name__ == "__main__":
    args = parser.parse_args()
    centraldir: str = args.directory
    actions: List[str] = args.actions
    if not actions:
        raise ValueError("Action must be specified with a flag")
    complex_pattern: str = "[A-Z]" * 6
    branch: BranchDirectory = BranchDirectory(centraldir, complex_pattern)
    print(branch)
    stdout = sys.stdout
    output = open(f"{centraldir}/jobbobsays.txt", 'w')
    sys.stdout = output
    # print(f"Pickled branch:\n{pickle.dumps(branch)}\n")
    print(datetime.datetime.now())
    for action in actions:
        if action == "info":
            print("***INFO***")
            for leaf in branch.get_leaves():
                leaf.delete_subdirs()
                print(leaf.get_name())
                if leaf.get_log_detail("incomplete"):
                    print('\t', "Incomplete:")
                    for log in leaf.get_log_detail("incomplete"):
                        print('\t', log)
                else:
                    print('\t', "All logs completed.")
                    print(leaf.get_log_detail("complete"))
                print()
            print(".coms for the incomplete logs:")
            for log in branch.get_leaf_detail("incomplete"):
                print(os.path.splitext(log)[0] + ".com")
            print("Complexes with less than 5 .log files:")
            for leaf in branch.get_leaves():
                if len(leaf.get_logs()) < 5:
                    print(f"{leaf.get_name()} has {len(leaf.get_logs())} .log files")
            # print("Dinuclear:", branch.get_leaf_detail("dinuclear"))
        elif action == "sort":
            print("***SORT***")
            os.mkdir("./dinuclear")
            os.mkdir("./incomplete")
            os.mkdir("./complete")
            dinuclear: int = 0
            incomplete: int = 0
            complete: int = 0
            for leaf in branch.get_leaves():
                leafname: str = leaf.get_name()
                if leaf.get_log_detail("dinuclear"):
                    shutil.move(leafname, f"dinuclear/{leafname}")
                    dinuclear += 1
                else:
                    if leaf.get_log_detail("incomplete"):
                        shutil.move(leafname, f"incomplete/{leafname}")
                        incomplete += 1
                    else:
                        shutil.move(leafname, f"complete/{leafname}")
                        complete += 1
            print(f"Moved {complete} complexes into \"complete/\" and {incomplete} complexes into \"incomplete/\".")
            print(f"{dinuclear} dinuclear complexes found.")
        elif action == "custom":
            pass
        else:
            pass
    output.close()
    sys.stdout = stdout
