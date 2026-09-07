from pymavlink import mavutil
import time


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


def go_to(drone, lat, lon, alt):
    print(f"Flying to:\n---------------------------------\nLatitude:\t{lat}\nLongitude:\t{lon}\nAltitude:\t{alt}\n---------------------------------")


def return_home(drone):
    drone.mav.command_long_send(
        drone.target_system,
        drone.target_component,
        mavutil.mavlink.MAV_CMD_RETURN_TO_LAUNCH,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
    )
    print("Returning to launch")


def main():
    drone = connect()
    print("Waiting 15 seconds for EKF to initialize...")
    time.sleep(15)

    set_guided(drone)
    altitude = float(input("Takeoff altitude (meters): "))
    arm_and_takeoff(drone, altitude)
    time.sleep(3)

    while True:
        print("\n1.\tFly to coordinates")
        print("2.\tManual Move")
        print("3.\tReturn to origin")
        print("4.\tExit")
        choice = input("Select:\t")

        if choice == "1":
            latitude = float(input("Latitude:\t"))
            longitude = float(input("Longitude:\t"))
            altitude = float(input("Altitude (meters):\t"))
            go_to(drone, latitude, longitude, altitude)

        elif choice == "2":
            print("not ready yet :(")

        elif choice == "3":
            return_home(drone)

        elif choice == "4":
            break

    print("Mission ended")


