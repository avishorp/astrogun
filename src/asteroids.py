
import time, random, math, numpy
from util import LinearMotion, spher_to_cart
from settings import *
import pi3d

# A list of all available asteroid models
models = [
    # Mode file                    Scale
    ('10115_1992_SK.obj',          1.0   ),
    ('413_Edburga_354.obj',        1.0   ),
    ('BJ13_519.obj',               1.0   ),
    ('S11_Epimetheus_2.obj',       1.0   ),
    ('29075_1950_DA_Prograde.obj', 1.0   ),
    ('41_Daphne_131.obj',          0.007 ),
    ('M2_Deimos.obj',              0.8   ),
    ('SB_279.obj',                 1.0   )
    ]

class Asteroid:
    def __init__(self, base_model, azimuth, inclination, speed, t0, explosion_shader, regular_shader):
        self.base_model = base_model
        self.azimuth = azimuth
        self.inclination = inclination
        self.speed = speed
        self.explosion_shader = explosion_shader
        self.radius = 1   # TODO: Customize the radius for each model
        initial_location = numpy.array(
            spher_to_cart(azimuth, inclination, INITIAL_DISTANCE))
        self.motion = LinearMotion(initial_location, numpy.array((0,0,0)), speed, t0)
        self.hit_mode = False
        self.base_model.set_shader(regular_shader)
           
        # Set the initial position
        self.base_model.position(initial_location[0], 
                                 initial_location[1], 
                                 initial_location[2])
        
    def draw(self, camera):
        self.base_model.draw(camera = camera)
        
    def move(self, t):
        if not self.hit_mode:
            # Move the asteroid along the line towards the origin
            self.pos = self.motion.location(t)
            self.base_model.position(self.pos[0], self.pos[1], self.pos[2])
            self.base_model.rotateIncX(5)
            self.base_model.rotateIncY(9)
        else:
            # Set the explosion progress parameter
            self.hit_time = t - self.hit_t0
            self.base_model.set_custom_data(21, (0.0, self.hit_time/5.0, 0.0))
        
    def distance2(self):
        return self.pos.dot(self.pos)
    
    def get_position(self):
        return self.pos
    
    def hit(self, now):
        self.hit_mode = True
        self.hit_t0 = now
        self.hit_time = 0
        self.base_model.set_shader(self.explosion_shader)

    def get_base_model(self):
        return self.base_model

class AsteroidGenerator:
    """
    Generates shootable obects.
    """
    
    # Initialize the object
    #   model_list - A list of Model objects of the shootable
    #   motion_func - A function describing the motion of the object
    #   rate - Generation rate, in obj/sec
    #   angle_restricion - TBD
    def __init__(self, asteroid_db, rate, angle_restiction, explosion_shader, regular_shader):
        self.rate = rate
        self.rate_range = ((1.0/self.rate)*0.8, (1.0/self.rate)*1.2)
        self.explosion_shader = explosion_shader
        self.regular_shader = regular_shader
        self.next_gen_time = time.time()
        self.calc_next_gen_time()
        self.asteroid_model_list = asteroid_db
    
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
            # pull it out of the list
            # Note: It should have been cloned, but there is a problem
            # with clone()
            ast_num = random.randint(0,len(self.asteroid_model_list)-2)
            nobj = self.asteroid_model_list[ast_num]
            del self.asteroid_model_list[ast_num]
            
            # Select an incident angle and speed
            azimuth = random.uniform(*AZIMUTH_RANGE)
            incl = random.uniform(*INCLINATION_RANGE)
            speed = random.uniform(*SPEED_RANGE)

            # Create the asteroid object
            ast = Asteroid(nobj, azimuth, incl, speed, now, self.explosion_shader, self.regular_shader)
            
            # Calculate the next generation time
            self.calc_next_gen_time()
            
            # Return the new asteroid
            return ast
        
        else:
            # Do not create anything
            return None

    def return_asteroid(self, ast):
        self.asteroid_model_list.append(ast.get_base_model())

