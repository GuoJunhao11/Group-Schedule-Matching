import ast
from datetime import datetime

def time_to_minutes(time_str):
    time_obj = datetime.strptime(time_str, "%H:%M")
    return time_obj.hour * 60 + time_obj.minute

def minutes_to_time(minutes):
    hours = minutes // 60
    minutes = minutes % 60
    return f"{hours:02}:{minutes:02}"

def merge_intervals(intervals):
    intervals.sort(key=lambda x: x[0])  # Sort intervals by start time
    merged = []
    for start, end in intervals:
        if not merged or merged[-1][1] < start:
            merged.append([start, end])  # No overlap
        else:
            merged[-1][1] = max(merged[-1][1], end)  # Merge
    return merged

def get_free_times(busy_intervals, working_period):
    login, logout = map(time_to_minutes, working_period)
    busy_intervals = [[time_to_minutes(start), time_to_minutes(end)] for start, end in busy_intervals]
    merged_busy = merge_intervals(busy_intervals)

    free_times = []
    # Check for free time before the first busy interval
    if login < merged_busy[0][0]:
        free_times.append([login, merged_busy[0][0]])
    
    # Check for free time between busy intervals
    for i in range(1, len(merged_busy)):
        free_times.append([merged_busy[i-1][1], merged_busy[i][0]])
    
    # Check for free time after the last busy interval
    if merged_busy[-1][1] < logout:
        free_times.append([merged_busy[-1][1], logout])
    
    return free_times

def intersect_intervals(all_free_times):
    common_intervals = all_free_times[0]
    for free_times in all_free_times[1:]:
        temp_intersection = []
        i, j = 0, 0
        # Merge all_free_times into valid common_intervals using two pointer
        while i < len(common_intervals) and j < len(free_times):
            start = max(common_intervals[i][0], free_times[j][0])
            end = min(common_intervals[i][1], free_times[j][1])
            if start < end:
                temp_intersection.append([start, end])
            if common_intervals[i][1] < free_times[j][1]:
                i += 1
            else:
                j += 1
        common_intervals = temp_intersection
    return common_intervals

def find_available_meeting_slots(busy_schedules, working_periods, meeting_duration):
    all_free_times = []
    # Append free time ranges in mutes for each person to all_free_times
    for i in range(len(busy_schedules)):
        busy_intervals = busy_schedules[i]
        working_period = working_periods[i]
        free_times = get_free_times(busy_intervals, working_period)
        all_free_times.append(free_times)

    common_free_times = intersect_intervals(all_free_times)

    # Filter by meeting duration
    available_meeting_times = []
    for start, end in common_free_times:
        if end - start >= meeting_duration:
            available_meeting_times.append([minutes_to_time(start), minutes_to_time(end)])

    return available_meeting_times

def read_input():
    with open("input.txt", "r") as file:
        busy_schedules = []
        working_periods = []
        
        # Read until we reach the last line for meeting duration
        while True:
            line = file.readline().strip()
            if not line:
                break
            if line.isdigit():
                meeting_duration = int(line)  # This is the meeting duration
                break
            busy_schedule = ast.literal_eval(line)
            busy_schedules.append(busy_schedule)  # Collect busy schedules
            
            working_period = ast.literal_eval(file.readline().strip())
            working_periods.append(working_period)  # Collect working periods
            
    return busy_schedules, working_periods, meeting_duration

def write_output(available_slots):
    with open("output.txt", "w") as file:
        file.write(str(available_slots))

def main():
    busy_schedules, working_periods, meeting_duration = read_input()
    available_slots = find_available_meeting_slots(busy_schedules, working_periods, meeting_duration)
    write_output(available_slots)
    print("Available meeting slots written to output.exe")

if __name__ == "__main__":
    main()
