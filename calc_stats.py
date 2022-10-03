
def calc_time_per_mile(in_miles:str, in_min:str, in_sec:str) -> (str, int, int):
    """
    :param in_miles:
    :param in_min:
    :param in_sec:
    :return: 'mm:ss' time per mile, seconds per mile, seconds per race
    """
    try:
        miles = float(in_miles)
        seconds = ( (int(in_min) * 60) + int(in_sec) )
        #ignores fractional seconds remainder, and skip rounding
        sec_per_mile = int(seconds / miles)
        # print(sec_per_mile)
        min_per_mile = sec_per_mile // 60
        sec_remain = sec_per_mile % 60
        time_per_mile_str = '{}:{}'.format(min_per_mile, sec_remain)
    except Exception as err:
        time_per_mile_str = 'Error:  Miles input be a nonzero Integer or Decimal;\nMinutes and Seconds should be an integers.'
        print('********** calc_time_per_mile failed with this error:', str(err))
    return (time_per_mile_str, sec_per_mile, seconds)

#TEST1:
# race_stats = calc_time_per_mile('1.6', '15', '30')
# print(type(race_stats))
# print('For 1.6 miles, 15 min, 30 seconds; time per mile, seconds per mile, seconds per race  is:  \n', race_stats)

