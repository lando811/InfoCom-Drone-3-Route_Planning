import math
import requests
import argparse
import time

#Write you own function that moves the drone from one place to another 
#the function returns the drone's current location while moving
#====================================================================================================
def travel(current, target):
    x,y = current
    x_t,y_t = target

    distance = math.sqrt((x_t - x)**2 + (y_t - y)**2) * 10000

    n = math.ceil(distance)

    x_next = x + (x_t - x)/n
    y_next = y + (y_t - x)/n
    
    return (x_next, y_next)


#====================================================================================================


def run(current_coords, from_coords, to_coords, SERVER_URL):
    # Complete the while loop:
    # 1. Change the loop condition so that it stops sending location to the data base when the drone arrives the to_address
    # 2. Plan a path with your own function, so that the drone moves from [current_address] to [from_address], and the from [from_address] to [to_address]. 
    # 3. While moving, the drone keeps sending it's location to the database.
    #====================================================================================================
#My function that moves the drone from one place to another
    
    current = current_coords
    targets = [from_coords, to_coords]
    
    for target in targets:
        while math.sqrt((target[0] - current[0])**2 + (target[1] - current[1])**2) * 10000> 0.0002:
            current = travel(current, target)
            with requests.Session() as session:
                drone_location = {'longitude': current[0],
                                  'latitude': current[1]
                            }
            resp = session.post(SERVER_URL, json=drone_location)
            time.sleep(0.2)
            
        current = target
    print(f"Arrived at {to_coords}")
  #====================================================================================================

   
if __name__ == "__main__":
    SERVER_URL = "http://127.0.0.1:5001/drone"

    parser = argparse.ArgumentParser()
    parser.add_argument("--clong", help='current longitude of drone location' ,type=float)
    parser.add_argument("--clat", help='current latitude of drone location',type=float)
    parser.add_argument("--flong", help='longitude of input [from address]',type=float)
    parser.add_argument("--flat", help='latitude of input [from address]' ,type=float)
    parser.add_argument("--tlong", help ='longitude of input [to address]' ,type=float)
    parser.add_argument("--tlat", help ='latitude of input [to address]' ,type=float)
    args = parser.parse_args()

    current_coords = (args.clong, args.clat)
    from_coords = (args.flong, args.flat)
    to_coords = (args.tlong, args.tlat)

    print(current_coords)
    print(from_coords)
    print(to_coords)

    run(current_coords, from_coords, to_coords, SERVER_URL)
