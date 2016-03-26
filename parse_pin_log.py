import re
import datetime

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


with open('pin_timers.log','r') as log:
    lines = "".join(log.readlines())
    parseall = re.findall("(\d+) (\S+):main:(\S+) (.*?)[$\n]", lines)
    timers_info = re.findall("(\d+) set:main:(\S+) (?P<mainlabel>.*?)[\n](?:(?:(?:.*?[\n])*?)(?:(\d+) ack:main:null (?P=mainlabel)[\n]))",
            lines)
    print timers_info[0]
    print "..."
    print timers_info[-1]
    #testtimers(parseall, timers_info)
    import json
    with open('pin_interpreted.log','w') as savefile:
        json.dump(parse_matches(timers_info), savefile)
        # forgot whether json.dump was (data, file) or (file, data)..


