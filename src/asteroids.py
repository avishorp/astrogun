
import time, random, math, numpy
from util import LinearMotion, PolarCoord
from settings import SPEED_RANGE, PHI_RANGE, THETA_RANGE, INITIAL_DISTANCE
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
    def __init__(self, base_model, azimuth, inclination, speed, t0, explosion_shader):
        self.base_model = base_model
        self.azimuth = azimuth
        self.inclination = inclination
        self.speed = speed
        self.explosion_shader = explosion_shader
        self.radius = 1   # TODO: Customize the radius for each model
        initial_location = numpy.array(
            PolarCoord(INITIAL_DISTANCE, azimuth, inclination).to_cartesian())
        self.motion = LinearMotion(initial_location, numpy.array((0,0,0)), speed, t0)
        self.hit_mode = False
           
        # Set the initial position
        self.base_model.position(initial_location[0], 
                                 initial_location[1], 
                                 initial_location[2])
        
    def draw(self):
        self.base_model.draw()
        
    def move(self, t):
        if not self.hit_mode:
            # Move the asteroid along the line towards the origin
            self.pos = self.motion.location(t)
            self.base_model.position(self.pos[0], self.pos[1], self.pos[2])
            self.base_model.rotateIncX(0.2)
            self.base_model.rotateIncY(0.3)
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
        self.base_model.set_shader(self.explosion_shader)

class AsteroidGenerator:
    """
    Generates shootable obects.
    """
    
    # Initialize the object
    #   model_list - A list of Model objects of the shootable
    #   motion_func - A function describing the motion of the object
    #   rate - Generation rate, in obj/sec
    #   angle_restricion - TBD
    def __init__(self, rate, angle_restiction):
        self.rate = rate
        self.rate_range = ((1.0/self.rate)*0.8, (1.0/self.rate)*1.2)
        self.next_gen_time = time.time()
        self.calc_next_gen_time()
        
        # Load the asteroid shaders
        self.regular_shader = pi3d.Shader("uv_flat")
        self.explosion_shader = pi3d.Shader("uv_flat_explode")
        
        # Load the asteroid models
        self.asteroid_model_list = []
        global_scale = 1.0
        for mf in models[0:3]:
            model_filename = mf[0]
            model_scale = mf[1]
            model_name = model_filename.split('.')[0] # Remove the .obj extention
  
            print("Loading " + model_name)
  
            m = pi3d.Model(file_string='../media/models/' + model_filename, 
                           name=model_name)
            m.set_shader(self.regular_shader)
            m.scale(model_scale*global_scale, 
                    model_scale*global_scale,
                    model_scale*global_scale)
  
            self.asteroid_model_list.append(m)

    
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
            nobj = random.choice(self.asteroid_model_list).clone()
            
            # Select an incident angle and speed
            phi = random.uniform(*PHI_RANGE)
            theta = random.uniform(*THETA_RANGE)
            speed = random.uniform(*SPEED_RANGE)

            # Create the asteroid object
            ast = Asteroid(nobj, phi, theta, speed, now, self.explosion_shader)
            
            # Calculate the next generation time
            self.calc_next_gen_time()
            
            # Return the new asteroid
            return ast
        
        else:
            # Do not create anything
            return None

