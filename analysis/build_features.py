import sys, json
from pathlib import Path
import pandas as pd

#Path object that represents a Directory, returns pointer to user's home directory
RAW = Path.home() / "anomaly-monitor"/ "data"/ "raw"
#Path object saves table to windows.csv
OUT = Path.home() / "anomaly-monitor"/ "data" / "features" / "windows.csv"
WINDOW_NS = 10 * 1_000_000_000 

#Creates Table for given file f
def load_session(f):
    #list of dictionaries
    rows = []
    #read the file's text, split into individual lines 
    for line in f.read_text().splitlines():
        #parse each JSON line into a Python Dictionary
        try:
            rows.append(json.loads(line))
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

#Generates the five features/properties that describes whath happens in each time window.
def features_for_window(g):
    #oldest event ts - newest event ts to get the duration a process was active in nanoseconds-> then convert into seconds
    span_sec = max((g.ts.max()- g.ts.min()) / 1e9, 1e-9)
    execs = (g.type == "exec").sum() #gives scalar
    
    return pd.Series({
        "events_per_sec":   len(g) / 10.0,
        "exec_ratio":       execs / len(g), #number of events / length of process window
        "unique_comms":     g.comm.nunique(), #number of unqiue process names (values)
        #filter dataframe by finding all events of type 'open', group rows into buckets based on thier PID, get the number of rows in each bucket for each PID
        #max finds the pid with the most events of type 'open'
        "max_files_per_proc": g[g.type == "open"].groupby("pid").size().max()
                              if(g.type == "open").any() else 0,
        "max_chain_depth":    chain_depth(g.pid.tolist(), g.ppid.tolist())

    })


def main():
    all_windows = []
    #path object to the user's home directoty, glob finds the pathnames with the given patten.
    files = sorted(RAW.glob("*.jsonl"))

    if not files:
        sys.exit(f" no files found in {RAW}")
    # for each data file(f) in files create a DataFrame by calling the load_session function that creates a Table based on the data
    for f in files:
        df = load_session(f)
        if df.empty:
            print(f"Skipping Empty Fille {f.name}")
            continue
        
        #timestamp from colum - earliest time found // 10 billion Nanoseconds to get the corresponding bucket number.
        df["window"] = (df.ts - df.ts.min()) // WINDOW_NS

        #groups by bucket and feeds each time window bucket to my features_for_window funciton     
        feats = df.groupby("window").apply(features_for_window, include_groups=False)

        #assigning new column sessions = filename excluding filepath or exentension
        feats["session"] = f.stem
        feats["label"] = "anomaly" if f.stem.startswith("anomaly") else "baseline"
        all_windows.append(feats)

        print(f"{f.stem}: has {len(feats)} windows")

    #combines windows into one dataframe
    result = pd.concat(all_windows, ignore_index=False)
    result.to_csv(OUT, index=False)
    print(f"\nOutput: {len(result)} windows -> {OUT}")

if __name__ == "__main__":
    main()




