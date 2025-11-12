
import argparse
import gpxpy
import gpxpy.gpx
from datetime import datetime
from haversine import haversine, Unit

def calculate_average_speed(gpx_file, start_time=None, end_time=None, start_distance=None, end_distance=None, unit='km/h', skip_zeros=False):
    """
    Calculates the average speed for a segment of a GPX track.
    """
    try:
        with open(gpx_file, 'r') as f:
            gpx = gpxpy.parse(f)
    except FileNotFoundError:
        print(f"Error: File not found at {gpx_file}")
        return
    except gpxpy.gpx.GPXXMLSyntaxException:
        print(f"Error: Could not parse GPX file. Check if it is a valid GPX file.")
        return

    if not gpx.tracks:
        print("Error: GPX file contains no tracks.")
        return

    track = gpx.tracks[0]
    segment = track.segments[0]

    points = segment.points

    if start_time and end_time:
        start_time_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
        end_time_dt = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
        
        segment_points = [p for p in points if start_time_dt <= p.time <= end_time_dt]

    elif start_distance is not None and end_distance is not None:
        
        segment_points = []
        total_distance = 0
        start_index = -1
        end_index = -1

        if start_distance == 0:
            start_index = 0

        for i in range(1, len(points)):
            p1 = points[i-1]
            p2 = points[i]
            dist = haversine((p1.latitude, p1.longitude), (p2.latitude, p2.longitude), unit=Unit.KILOMETERS)
            
            if total_distance < start_distance and total_distance + dist >= start_distance:
                start_index = i
            
            if total_distance < end_distance and total_distance + dist >= end_distance:
                end_index = i
                break
            
            total_distance += dist
        
        if start_index != -1 and end_index != -1:
            segment_points = points[start_index:end_index+1]
        elif start_index != -1:
            segment_points = points[start_index:]
    else:
        segment_points = points


    if not segment_points or len(segment_points) < 2:
        print("Error: No points found in the specified segment or segment is too short.")
        return

    total_dist_segment = 0
    total_time_seconds = 0
    for i in range(1, len(segment_points)):
        p1 = segment_points[i-1]
        p2 = segment_points[i]
        dist = haversine((p1.latitude, p1.longitude), (p2.latitude, p2.longitude), unit=Unit.KILOMETERS)
        time_diff = (p2.time - p1.time).total_seconds()

        if skip_zeros:
            speed_kph = 0
            if time_diff > 0:
                speed_kph = (dist / time_diff) * 3600
            
            if speed_kph >= 1:
                total_dist_segment += dist
                total_time_seconds += time_diff
        else:
            total_dist_segment += dist
            total_time_seconds += time_diff

    if total_time_seconds == 0:
        avg_speed = 0
    else:
        if unit == 'mph':
            total_dist_segment *= 0.621371
            avg_speed = (total_dist_segment / total_time_seconds) * 3600
        else: #km/h
            avg_speed = (total_dist_segment / total_time_seconds) * 3600


    print(f"Average Speed: {avg_speed:.2f} {unit}")


def main():
    parser = argparse.ArgumentParser(description="Calculate the average speed for a segment of a GPX track.")
    parser.add_argument("gpx_file", help="The path to the GPX file.")
    
    parser.add_argument("--start-time", help="Start time of the segment in ISO format (e.g., 2025-11-12T10:00:00Z)")
    parser.add_argument("--end-time", help="End time of the segment in ISO format (e.g., 2025-11-12T10:15:00Z)")
    
    parser.add_argument("--start-distance", type=float, help="Start distance of the segment in kilometers.")
    parser.add_argument("--end-distance", type=float, help="End distance of the segment in kilometers.")

    parser.add_argument("--unit", choices=['km/h', 'mph'], default='km/h', help="Output unit for speed (km/h or mph).")
    parser.add_argument("--skip-zeros", action="store_true", help="Skip points where speed is 0 km/h.")

    args = parser.parse_args()

    if (args.start_time and not args.end_time) or (not args.start_time and args.end_time):
        parser.error("--start-time and --end-time must be used together.")

    if (args.start_distance is not None and args.end_distance is None) or \
       (args.start_distance is None and args.end_distance is not None):
        parser.error("--start-distance and --end-distance must be used together.")

    if (args.start_time and args.start_distance is not None):
        parser.error("Please specify a segment by either time or distance, not both.")

    calculate_average_speed(args.gpx_file, args.start_time, args.end_time, args.start_distance, args.end_distance, args.unit, args.skip_zeros)

if __name__ == "__main__":
    main()
