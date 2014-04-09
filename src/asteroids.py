
import time, random, math

class PolarCoord:
    def __init__(self, r, phi, tetha):
        self.r = r
        self.phi = phi
        self.tetha = tetha
        
    def to_cartesian(self):
        x = self.r * math.sin(self.tetha)*math.cos(self.phi)
        y = self.r * math.sin(self.tetha)*math.sin(self.phi)
        z = self.r * math.cos(self.tetha)
        return (x, y, z)

# Asteroid generation parametrs
###############################
SPEED_RANGE = (1.0, 3.0)
PHI_RANGE = (0, math.pi)
THETA_RANGE = (10.0/180.0*math.pi,170/180.0*math.pi)
INITIAL_DISTANCE = 50

class LinearMotion:
    # initial_location - Object of class PolarCoord describing the
    #                    initial location of the item
    # speed - The speed of the item towards the origin
    # t0 - The initial time
    def __init__(self, initial_location, speed, t0):
        self.loc = initial_location.to_cartesian()
        speed_polar = PolarCoord(-speed, 
                                 initial_location.phi,
                                 initial_location.tetha)
        self.speed = speed_polar.to_cartesian()
        self.t0 = t0
        
    def location(self, t):
        dt = t - self.t0
        return (self.loc[0]+self.speed[0]*dt,
                self.loc[1]+self.speed[1]*dt,
                self.loc[2]+self.speed[2]*dt)

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
            m = LinearMotion(PolarCoord(INITIAL_DISTANCE, phi, theta), speed, now)
            
            # Set the initial position
            nobj.position(*(m.location(now)))
            
            # Calculate the next generation time
            self.calc_next_gen_time()
            
            # Return the new asteroid
            return (nobj, m)
        
        else:
            # Do not create anything
            return None

