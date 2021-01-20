# Social Distance Estimator

## Overview

This project is to detect persons on the place and estimate the social distance between them on Jetson Nano device. 
If social distance is less than safe distance, the person is marked in green and if not, he will be marked in red.

## Structure

- src

    The source code for person detection, calculation between 2 persons.
   
- utils

    * The model to detect person
    * The source code for calibration frame and management of folder and file in this project
    
- app

    The main execution file
    
- requirements

    All the dependencies for this project
    
- settings

    Several settings for this project
    
## Installation

- Environment

    Jetson Nano(Ubuntu 18.04, GPU 4G), python 3.6+

- Dependency Installation

    Please go ahead to this project directory and run the following command in the terminal.
    
    ```
    pip3 install -r requirements.txt
    ``` 
    
    Also, building OpenCV 4.2.0 is needed. So please follow the https://github.com/mdegans/nano_build_opencv 
    to build OpenCV==4.2.0. Before this, since it needs more memory to build OpenCV, please create swap memory 
    by following https://www.jetsonhacks.com/2019/04/14/jetson-nano-use-more-memory/. The swap memory has to be 4G at least.

## Execution

- You can set the SAFE_DISTANCE as a safe distance (unit:cm) FOCUS_LENGTH as a calibration for each camera in settings file.

- Please run the following command in terminal.

    ```
    python3 app.py
    ```
