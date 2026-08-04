import sys, json
from pathlib import Path
import pandas as pd

#Path object that represents a Directory, returns pointer to user's home directory
RAW = Path.home() / "anomaly-monitor"/ "data"/ "raw"
#Path object saves table to windows.csv
OUT = Path.home() / "anomaly-monitor"/ "data" / "raw" / "windows.csv"
WINDOW_NS = 10 * 1_000_000_000 

def load_session(f):
    rows = []
    #with splitlines we take the giant file string and turns the whole file into a list of indivual line strings
    for line in f.read_text().splitlines():
        #takes json into a python object
        try:
            rows.append(json.load(line))
        except json.JSONDecodeError:
            continue
            #DataFrame is a 2D Tabular Data Structure with rows,columns.
    return pd.DataFrame(rows)


#determines the longest ancestry chain, by evaluating each pid down to its last parent pid
def chain_depth(pids, parents):
    #zip pairs elements in same position in each list, and creates a dictionary of key:value pairs which reprenst pid and their corresponding parent id.
    parent_of = dict(zip(pids, parents))
    best = 0

#for every pid in dict parent_of
    for pid in parent_of:
        depth, current, seen = 1, pid, set()
        while current in parent_of and current not in seen:
            seen.add(current)
            #take current pid as a key and find its parent pid
            current = parent_of[current]
            depth += 1
        best = max(best, depth)
    return best

def features_for_window(g):
    #oldest event ts - newest event ts to get the duration a process was active in nanoseconds-> then convert into seconds
    span_sec = max((g.ts.max()- g.ts.min()) / 1e9, 1e-9)
    execs = (g.type == "exec").sum()
    
    return pd.Series({
        
    })