from pymavlink import mavutil
import time
import math

def connect():
    print("Connecting...")
    drone = mavutil.mavlink_connection("udp:127.0.0.1:14551")
    drone.wait_heartbeat()
    print(f"Heartbeat from system {drone.target_system}, component {drone.target_component}")
    return drone

def set_guided(drone):
    drone.mav.set_mode_send(
        drone.target_system,
        mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
        4,
    )
    time.sleep(1)
    print("Mode set to GUIDED")

def arm_and_takeoff(drone, altitude):
    drone.mav.command_long_send(
        drone.target_system,
        drone.target_component,
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        )
    print("Arming...")
    time.sleep(1)

    drone.mav.command_long_send(
        drone.target_system,
        drone.target_component,
        mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
            altitude,
        )
    print(f"Taking off to {altitude}m...")

def wait_to_arrival(drone, target_x, target_y, target_z, threshold=1.0):
    print("Waiting for arrival...")
    while True:
        msg = drone.recv_match(type='LOCAL_POSITION_NED', blocking=True)
        current_x = msg.x
        current_y = msg.y
        current_z = msg.z

        distance = ((current_x - target_x)**2 + (current_y - target_y)**2 + (current_z - target_z)**2) ** 0.5
        print(f"current: ({current_x}, {current_y}, {current_z}) target: ({target_x}, {target_y}, {target_z}) distance: {distance}")

        if distance < threshold:
            break
    print("Arrived")


def sweepingMode(drone):
    #Asks what you want to do: Boundaries, ___MORE LATER____

    while True:
        try:
            #Asks prompt from list
            sweepingModePrompt = int(input("What would you like to do?\n1. Change Boundaries\n2. Return\n"))

            if sweepingModePrompt in [1, 2]:
                break
            else:
                print("Invalid choice. Pick either 1 or 2.")

        except ValueError:
            print("Please enter a valid number")
    if sweepingModePrompt == 1:
        #North Boundary

        while True:
            try:
                #Ask for input and tries to make it an integer and if it succeeds it no longer loops
                maxNorthInput = int(input("What is the northmost boundary of the sweep in meters? "))


                break
            except ValueError:
                print("Please print a valid number ")
        #If it passes each check for integer then it moves on and displays the northmost boundary of the perimeter.
        print(f"Northmost boundary set to {maxNorthInput}m north of the GCS") 

        #South Boundary

        while True:
            try:
                #Ask for input and tries to make it an integer and if it succeeds it no longer loops
                maxSouthInput = int(input("What is the southmost boundary of the sweep in meters? "))


                break
            except ValueError:
                print("Please print a valid number ")
        #If it passes each check for integer then it moves on and displays the southmost boundary of the perimeter.
        print(f"Southmost boundary set to {maxSouthInput}m south of the GCS")    

        #West Boundary

        while True:
            try:
                #Ask for input and tries to make it an integer and if it succeeds it no longer loops
                maxWestInput = int(input("What is the westmost boundary of the sweep in meters? "))


                break
            except ValueError:
                print("Please print a valid number ")
        #If it passes each check for integer then it moves on and displays the westmost boundary of the perimeter.
        print(f"Westmost boundary set to {maxWestInput}m west of the GCS")    

        #East Boundary

        while True:
            try:
                #Ask for input and tries to make it an integer and if it succeeds it no longer loops
                maxEastInput = int(input("What is the eastmost boundary of the sweep in meters? "))


                break
            except ValueError:
                print("Please print a valid number ")
        #If it passes each check for integer then it moves on and displays the eastmost boundary of the perimeter.
        print(f"Eastmost boundary set to {maxEastInput}m east of the GCS")
        
        #Altitude
        while True:
                    try:
                        #Ask for input and tries to make it an integer and if it succeeds it no longer loops
                        altitude = int(input("What altitude do you want to climb to? "))
                        break
                    except ValueError:
                        print("Please print a valid number ")
                #If it passes each check for integer then it moves on and displays the altitude
                    print(f"Altitude set to {altitude}m above the GCS")  
                     
    else:
        print("Returning...")
        return

    north_south_distance = maxNorthInput + maxSouthInput
    num_rows = math.ceil(north_south_distance / 50)
    
    
    #Starts going to the starting point for sweeping
    drone.mav.set_position_target_local_ned_send(
        10,
        drone.target_system,
        drone.target_component,
        mavutil.mavlink.MAV_FRAME_LOCAL_NED,
        0b110111111000,
        maxNorthInput - 25,
        -maxWestInput,
        -altitude, 
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0
    )
    
    wait_to_arrival(drone, maxNorthInput -25, -maxWestInput, -altitude)
        
    #Here is where it actually starts sweeping
    
    drone.mav.set_position_target_local_ned_send(
    10,
    drone.target_system,
    drone.target_component,
    mavutil.mavlink.MAV_FRAME_LOCAL_NED,
    0b110111111000,
    maxNorthInput - 25,
    maxEastInput,
    -altitude, 
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0
    )
    
    wait_to_arrival(drone, maxNorthInput -25, maxEastInput, -altitude)
    
    i = 0
    while i < num_rows:
        if i % 2: 
            #ODD i
            drone.mav.set_position_target_local_ned_send(
            10,
            drone.target_system,
            drone.target_component,
            mavutil.mavlink.MAV_FRAME_LOCAL_NED,
            0b110111111000,
            maxNorthInput - 50 * (i + 1) - 25,
            -maxWestInput,
            -altitude, 
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0
            )

            wait_to_arrival(drone, maxNorthInput - 50 * (i + 1) - 25, -maxWestInput, -altitude)
            
            drone.mav.set_position_target_local_ned_send(
            10,
            drone.target_system,
            drone.target_component,
            mavutil.mavlink.MAV_FRAME_LOCAL_NED,
            0b110111111000,
            maxNorthInput - 50 * (i + 1) - 25,
            maxEastInput,
            -altitude, 
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0
            )
            
            wait_to_arrival(drone, maxNorthInput - 50 * (i + 1) - 25, maxEastInput, -altitude)
 
        else:
        #Even         
            drone.mav.set_position_target_local_ned_send(
            10,
            drone.target_system,
            drone.target_component,
            mavutil.mavlink.MAV_FRAME_LOCAL_NED,
            0b110111111000,
            maxNorthInput - 50 * (i + 1) - 25,
            maxEastInput,
            -altitude, 
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0
            )
            
            wait_to_arrival(drone, maxNorthInput - 50 * (i + 1) - 25, maxEastInput, -altitude)
            
            drone.mav.set_position_target_local_ned_send(
            10,
            drone.target_system,
            drone.target_component,
            mavutil.mavlink.MAV_FRAME_LOCAL_NED,
            0b110111111000,
            maxNorthInput - 50 * (i + 1) - 25,
            -maxWestInput,
            -altitude, 
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0
            )
            
            wait_to_arrival(drone, maxNorthInput - 50 * (i + 1) - 25, -maxWestInput, -altitude)
            
        i += 1


def goHome(drone):
    drone.mav.command_long_send(
    drone.target_system,
    drone.target_component,
    mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH,
    0, 
    0, 0, 0, 0, 0, 0, 0
    )
    
def main():
    drone = connect()
    print("Waiting 15 seconds for EKF to initialize...")
    time.sleep(15)

    set_guided(drone)
    altitude = float(input("Takeoff altitude (meters): "))
    arm_and_takeoff(drone, altitude)
    time.sleep(3)

    sweepingMode(drone)
    
    
main()
    

