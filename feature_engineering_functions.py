def calculate_time_differences(data):
    from datetime import datetime
    times = []
    pressure = [row[2] for row in data]
    
    # Parse timestamps, handling both formats
    times_data = []
    for row in data:
        try:
            # Try parsing with microseconds
            times_data.append(datetime.strptime(row[4], "%H:%M:%S.%f"))
        except ValueError:
            # If it fails for not completed tasks where time = 00:00:00, parse without microseconds
            times_data.append(datetime.strptime(row[4], "%H:%M:%S"))
    
    # Calculate time differences between consecutive points
    indices = [i for i, p in enumerate(pressure) if p > 0] # Find indices where pressure > 0, the consecutive points

    for k in range(1, len(indices)):
        prev_idx = indices[k-1]
        curr_idx = indices[k]
        time_diff = (times_data[curr_idx] - times_data[prev_idx]).total_seconds()
        times.append(time_diff)
    
    return times

def calculate_distances(x_coords, y_coords):
    import numpy as np
    distances = []
    for i in range(1, len(x_coords)):
        dist = np.sqrt((x_coords[i] - x_coords[i-1])**2 + (y_coords[i] - y_coords[i-1])**2)
        distances.append(dist)
    return distances

def calculate_edge_types(data):
    edge_types = []
    pressure = [row[2] for row in data]
    
    # Find indices where pressure > 0
    indices = [i for i, p in enumerate(pressure) if p > 0]
    
    # Calculate edge types between consecutive nodes
    for k in range(1, len(indices)):
        prev_idx = indices[k-1]
        curr_idx = indices[k]
        # Check for gap between prev_idx and curr_idx
        if all(pressure[j] > 0 for j in range(prev_idx + 1, curr_idx)):
            edge_types.append(0)  # No gap
        else:
            edge_types.append(1)  # Gap exists
    
    return edge_types

def calculate_speeds(distances, times):
    """
    Calculate speed for each edge as distance/time.
    
    Args:
        distances (list): List of distances between consecutive nodes.
        times (list): List of time differences between consecutive nodes.
    
    Returns:
        list: Speeds for each edge (distance/time), with 0 if time is 0 to avoid division errors.
    """
    return [d / t if t != 0 else 0 for d, t in zip(distances, times)]

def calculate_directions(x_coords, y_coords):
    """
    Calculate direction (angle in radians) for each edge.
    
    Args:
        x_coords (list): List of x-coordinates of nodes.
        y_coords (list): List of y-coordinates of nodes.
    
    Returns:
        list: Directions for each edge, computed as arctan2(dy, dx).
    """
    import numpy as np
    return [np.arctan2(y_coords[i+1] - y_coords[i], x_coords[i+1] - x_coords[i]) 
            for i in range(len(x_coords) - 1)]

def calculate_pressure_diffs(pressure):
    """
    Calculate pressure difference between consecutive nodes.
    
    Args:
        pressure (list): List of pressure values at nodes.
    
    Returns:
        list: Pressure differences for each edge (p[i+1] - p[i]).
    """
    return [pressure[i+1] - pressure[i] for i in range(len(pressure) - 1)]

def calculate_fraction_pen_on(indices):
    """
    Calculate fraction of time pen was on between consecutive nodes.
    
    Args:
        indices (list): Original indices of nodes where pressure > 0.
    
    Returns:
        list: Fractions for each edge, as 2 / (total points between nodes).
    """
    fractions = []
    for k in range(1, len(indices)):
        i = indices[k-1]  # Index of first node in edge
        j = indices[k]    # Index of second node in edge
        total_points = j - i + 1  # Total samples from i to j, inclusive
        fractions.append(2 / total_points if total_points > 0 else 0)
    return fractions

