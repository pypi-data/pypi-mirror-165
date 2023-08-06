#############################################################
__version__ = '0.0.2'
__author__ = 'Jian Jiang'
__email__ = 'jianjiang.bio@gmail.com'
#############################################################

from manim import rate_functions

func_list = rate_functions.__dict__.keys()

def time_manager(start=0, stop=None, total_time=1, func='ease_in_sine'):
    if stop is None:
        stop = total_time
    relative_start = start / total_time
    relative_duration = (stop - start) / total_time
    def rate_func(t, relative_start=relative_start, relative_duration=relative_duration):
        if   t < relative_start:
            return 0.
        elif t > relative_start + relative_duration:
            return 1.
        else:
            _t = (t - relative_start) / relative_duration
            return rate_functions.__dict__[func](_t)
    return {
        'run_time': total_time,
        'rate_func': rate_func
    }