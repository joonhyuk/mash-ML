def clamp(value, in_min = 0, in_max = 1):
    if in_min > in_max: raise ValueError('in_max must be larger than in_min.')
    return min(in_max, max(in_min, value))

def map_range(value, in_min, in_max, out_min, out_max, clamped = False):
    if clamped: value = clamp(value, in_min, in_max)
    return ((value - in_min) / (in_max - in_min)) * (out_max - out_min) + out_min