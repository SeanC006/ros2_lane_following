# ROS2 Lane Following Project (Evolution of CV Control)

This project demonstrates the progression of classical computer vision techniques for autonomous lane following in ROS2 Gazebo (TurtleBot3 AutoRace environment).

---

## Pipeline Evolution

### Stage 1: Hough Line Detection (Baseline)
- Edge detection + HoughLinesP
- Lane classification via slope
- Basic steering controller

Problem:
- unstable in curves
- sensitive to noise

---

### Stage 2: ROI + Filtering Improvements
- Shortened ROI
- Excluded extremes line filtering
- Added smoothing motion using previous angular twist

Problem:
- Still unable to detect lines for first sharp turn
- Angular twist Z was outputting extremely low values (0.008)
- Line detection showed 0 lines were being detected at the start of the curve

---

### Stage 3: Centroid-Based Lane Tracking (Next)
- threshold-based lane segmentation
- centroid computation of lane pixels
- robust to missing lane markings

Major improvement in robustness

---

### Stage 4: PID Controller (Not Done)
- replaces P controller
- smoother steering response
- reduced oscillation

---

### Stage 5: AutoRace Optimization (Not Done)
- tuned parameters for TurtleBot3 AutoRace world
- improved curve handling
- stable lap completion

---

## Technologies
- ROS2 Humble
- OpenCV
- Gazebo
- Python

---

## Key Insight
This project demonstrates why centroid-based perception is more robust than slope-based Hough detection in noisy autonomous driving environments.
