
import time, random, math, numpy
from util import LinearMotion, PolarCoord

# Asteroid generation parametrs
###############################
SPEED_RANGE = (1.0, 3.0)
PHI_RANGE = (0, math.pi)
THETA_RANGE = (10.0/180.0*math.pi,170/180.0*math.pi)
INITIAL_DISTANCE = 50

PHI_RANGE = (0, 0.5)
THERA_RANGE = (0.5,0.8)

#PHI_RANGE = (0,0.1)
#THETA_RANGE = (0,0.1)
class AsteroidGenerator:
    """
    Generates shootable obects.
    """
    
    # Initialize the object
    #   model_list - A list of Model objects of the shootable
    #   motion_func - A function describing the motion of the object
    #   rate - Generation rate, in obj/sec
    #   angle_restricion - TBD
    def __init__(self, model_list, rate, angle_restiction):
        self.model_list = model_list
        self.rate = rate
        self.rate_range = ((1.0/self.rate)*0.8, (1.0/self.rate)*1.2)
        self.next_gen_time = time.time()
        self.calc_next_gen_time()
    
    # Calculate the next time in which an object should be generated
    def calc_next_gen_time(self):
        self.next_gen_time = self.next_gen_time + random.uniform(*(self.rate_range))

    # Generates new asteroid.
    # The function may be called at any desirable rate. It may return either
    # None, if no object should be created; or a tuple containing the new
    # object and a motion function
    def generate_asteroid(self, now):
        # Check if it's time to create a new object
        if (now > self.next_gen_time):
            # Create a new object
            
            # Select a random item from the list, and
            # clone it
            nobj = random.choice(self.model_list).clone()
            
            # Select an incident angle and speed
            phi = random.uniform(*PHI_RANGE)
            theta = random.uniform(*THETA_RANGE)
            speed = random.uniform(*SPEED_RANGE)
            
            #print("phi=%f tetha=%f speed=%f" % (phi, theta, speed))
            #print("x=%f y=%f z=%f" % PolarCoord(speed, phi, theta).to_cartesian())
            # Create a linear motion coordinator
            initial_location = numpy.array(PolarCoord(INITIAL_DISTANCE, phi, theta).
                                           to_cartesian())
            m = LinearMotion(initial_location, numpy.array((0,0,0)), speed, now)
           
            # Set the initial position
            nobj.position(initial_location[0], initial_location[1], initial_location[2])
            
            # Calculate the next generation time
            self.calc_next_gen_time()
            
            # Return the new asteroid
            return (nobj, m)
        
        else:
            # Do not create anything
            return None

