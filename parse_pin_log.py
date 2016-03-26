import re
import datetime

# going the fuck over time
# confused by a syntax error

"""
# wishlist
def main_loop():
    "run all the pieces I need"

def get_logfile(savename):
    "get logfile from adb, save to savename. if already exists, ask whether to
    append or to overwrite"

def get_filenames():
    "prompt user or get args for logfile and savefile filepaths"

def make_readable(logname, savename):
    "get 

    with open(filename, 'w') as logfile:
        # wishlist
        def parse_entry(logfile):
            "given a logfile, return each entry as a tuple. Ask the user to " +
                "correct any misformed entries manually (or quit) along the way."
        def chunk_lines(logentries):
            "given a logfile, return chunks of set:main:# to set:main#. inclusive."
        def test_chunk(chunk):
            "figure out whether a chunk contains all and only the right options, print " +
            "notifications to sdout when it's missing cruicial features, return " +
            "a list containing tuples of (optiontype, timestamp)."
        def get_endstamp(chunk):
            "given a logchunk, return the timestamp of the single " + 
                "(error if more than one besides last) ack:main:null <label> " + 
                "matching the first label, or the next best option's timestamp"
        def order_options(label, array_of_option_timestamp_tuples):
            "given a label of the first entry in a chunk, return the best match " +
                "between the next fire:main:null <label>, ack:bother:null, " + 
                "fire:bother:null, and next set:main:#... prints out which is" +
                "used."
        def format_entry(entry, endstamp):
            "given an entry and a concluding timestamp, return a human readable string " +
                "containing the StartTime, SetLength, Duration, and Label."
        def save_data(filename, datastring, overwrite=None):
            "given a filename and a datastring, write the data to the file. " +
                "if file already exists, ask the user whether to abort, " +
                "overwrite, or append."

"""
if __name__ == "__main__":
    pass
# couldn't remember how to check for main instance in python

with open('pin_timers.log','r') as log:
    lines = "".join(log.readlines())
        # can't remeber
       # can't remember how to parse a string format 
        # .*? : the ? makes it nongreedy
    parseall = re.findall("(\d+) (\S+):main:(\S+) (.*?)[$\n]", lines)
    timers_info = re.findall("(\d+) set:main:(\S+) (?P<mainlabel>.*?)[\n](?:(?:(?:.*?[\n])*?)(?:(\d+) ack:main:null (?P=mainlabel)[\n]))|(?:\d+ fire:bother:null Bother Countdown\n(\d+) ack:bother:null)|(?:(?=(\d+) set:main))",
            lines)
    print timers_info[0]
    print "..."
    print timers_info[-1]
    testtimers(parseall, timers_info)
    import json
    with open('pin_interpreted.log','w') as savefile:
        json.dump(parse_matches(timers_info), savefile)
        # forgot whether json.dump was (data, file) or (file, data)..


def testtimers(all_parsed, matched_timers):
    mindex = 0
    for (timestamp, actiontype, timeset, label) in all_parsed:
        if actiontype == "set":
            for i, (m_timestamp, m_timeset, m_label, m_endstamp) in enumerate(matched_timers[mindex:]):
                if m_timestamp == timestamp and label == m_label and timeset == m_timeset:
                    mindex += i
                    break
                if int(m_timestamp) > int(timestamp):
                    raise ValueError("Did not find end for %s: %s" % (timestamp, label))
                # forgot how to raise errors in python


def parse_matches(matches):
    results = []
    for timestamp, timeset, label, endstamp in matches:
        start_date = datetime.datetime.fromtimestamp(int(timestamp) / 1000.0)
        timeset = int(timeset)
        duration = (start_date - datetime.datetime.fromtimestamp(int(endstamp)/1000.0)).total_seconds() / 60
        if abs(duration - timeset) >= (timeset * 0.10) and duration < 30:
            # abs() is not a math function, but built-in
            duration = timeset
        results.append(
                {"time":start_date.ctime(),
                "label":label,
                "set_time":timeset,
                "duration":duration}
                )


