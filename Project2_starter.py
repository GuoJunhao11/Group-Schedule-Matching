import ast
from datetime import datetime

def time_to_minutes(time_str):
    # Convert "HH:MM" time format to total minutes for easier calculations
    try:
        time_obj = datetime.strptime(time_str, "%H:%M")
        return time_obj.hour * 60 + time_obj.minute
    except ValueError:
        raise ValueError(f"Time format error with '{time_str}'. Ensure it's in HH:MM format.")

def minutes_to_time(minutes):
    # Convert minutes back to "HH:MM" format for readable output
    hours = minutes // 60
    minutes = minutes % 60
    return f"{hours:02}:{minutes:02}"

def merge_intervals(intervals):
    intervals.sort(key=lambda x: x[0])
    merged = []
    for start, end in intervals:
        if not merged or merged[-1][1] < start:
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)
    return merged

def get_free_times(busy_intervals, working_period):
    login, logout = map(time_to_minutes, working_period)
    busy_intervals = [[time_to_minutes(start), time_to_minutes(end)] for start, end in busy_intervals]
    merged_busy = merge_intervals(busy_intervals)

    free_times = []
    if login < merged_busy[0][0]:
        free_times.append([login, merged_busy[0][0]])
    for i in range(1, len(merged_busy)):
        if merged_busy[i-1][1] < merged_busy[i][0]:
            free_times.append([merged_busy[i-1][1], merged_busy[i][0]])
    if merged_busy[-1][1] < logout:
        free_times.append([merged_busy[-1][1], logout])
    return free_times

def intersect_intervals(all_free_times):
    if not all_free_times:
        return []
    common_intervals = all_free_times[0]
    for free_times in all_free_times[1:]:
        temp_intersection = []
        i, j = 0, 0
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
    all_free_times = [get_free_times(busy, work) for busy, work in zip(busy_schedules, working_periods)]
    common_free_times = intersect_intervals(all_free_times)
    valid_meeting_times = [[minutes_to_time(start), minutes_to_time(end)] 
                           for start, end in common_free_times if (end - start) >= meeting_duration]
    return valid_meeting_times

def read_input(filename="input.txt "):
    test_cases = []
    with open(filename, "r") as file:
        busy_schedules, working_periods, meeting_duration = [], [], None
        for line in file:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if line.isdigit():
                meeting_duration = int(line)
                test_cases.append((busy_schedules, working_periods, meeting_duration))
                busy_schedules, working_periods = [], []
            else:
                data = ast.literal_eval(line)
                if isinstance(data[0], list):
                    busy_schedules.append(data)
                else:
                    working_periods.append(data)
    return test_cases

def write_output(all_available_slots, filename="output.txt"):
    with open(filename, "w") as file:
        for i, slots in enumerate(all_available_slots, start=1):
            file.write(f"Test Case {i}:\n")
            for slot in slots:
                file.write(f"{slot}\n")
            file.write("\n")

def main():
    test_cases = read_input()
    all_available_slots = [find_available_meeting_slots(*case) for case in test_cases]
    write_output(all_available_slots)
    print("Available meeting slots for each test case written in 'output.txt'")

if __name__ == "__main__":
    main()
