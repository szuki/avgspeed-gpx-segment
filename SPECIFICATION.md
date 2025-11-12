# Specification: Average Speed Calculator from GPX

## 1. Overview

A command-line application that calculates the average speed for a specific segment of a ride or activity recorded in a GPX file.

## 2. Input

The application will accept the following inputs:

1.  **GPX File:** The path to a valid `.gpx` file.
2.  **Segment Definition:** The user must be able to define the start and end of the segment for which the average speed is to be calculated. The following methods will be supported:
    *   **By Time:** Using start and end timestamps (e.g., `--start-time "2025-11-12T10:00:00Z" --end-time "2025-11-12T10:15:00Z"`).
    *   **By Distance:** Using start and end distances from the beginning of the track (e.g., `--start-distance 5 --end-distance 10` in kilometers).

## 3. Processing

1.  **Parse GPX File:** The application will parse the input GPX file to extract all track points (`<trkpt>`) from the first track (`<trk>`). Each track point should contain latitude, longitude, and a timestamp.

2.  **Identify Segment:**
    *   If the segment is defined by time, the application will identify the first track point at or after the start time and the last track point at or before the end time.
    *   If the segment is defined by distance, the application will first calculate the cumulative distance from the start of the track for each point. It will then identify the points that correspond to the start and end distances.

3.  **Calculate Total Distance:** The total distance of the segment will be calculated by summing the distances between consecutive track points within the segment. The distance between two points will be calculated using the Haversine formula.

4.  **Calculate Total Time:** The total time for the segment will be the difference between the timestamp of the last track point in the segment and the timestamp of the first track point in the segment.

5.  **Calculate Average Speed:** The average speed will be calculated as:
    ```
    Average Speed = Total Distance / Total Time
    ```

## 4. Output

The application will output the calculated average speed to the console. The user should be able to specify the desired units for the speed:

*   Kilometers per hour (km/h) - default
*   Miles per hour (mph)

Example output:
```
Average Speed: 25.5 km/h
```

## 5. Error Handling

The application will handle the following error conditions:

*   The specified GPX file does not exist or is not a valid GPX file.
*   The GPX file does not contain any tracks or track points.
*   The specified start or end points for the segment (time or distance) are not found within the track.
*   The end point occurs before the start point.

## 6. Future Enhancements

*   A graphical user interface (GUI) to visualize the track on a map and allow the user to graphically select the desired segment.
*   Support for more output units (e.g., meters/second).
*   The ability to analyze and compare multiple segments from the same or different files.
*   Consideration of elevation changes in distance and speed calculations.
