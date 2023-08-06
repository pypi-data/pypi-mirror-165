This package contains set of modules for mechanical press design.
In this version there are total 5 modules.
Usage of each module is explained below:

------------------------------ Module 1: ed.py ---------------------------------

"""
About ed:
ed is for Eccentric Drive press. It is similar to Slider crank mechanism. Crankshaft is driven by a motor. Connecting rod connects crankpin (connecting rod journal) of Crankshaft at one end (called big end) and Slider at other end through pin. Rotary motion of Crankshaft is converted to linear movement of Slider. Slider motion is used to apply pressing force on a die to shape a component. The maximum force the Slider can apply is called rated force. Number of rotations of Crankshaft in one minute is called RPM (rotations per minute). Number of strokes per minute of Slider is called SPM. As the Slider crank mechanism is symmetrical, the forward motion time of Slider is equal to return time. At a given position (angle) of Crankshaft, Slider position, linear velocity and  acceleration can be of interest. For this, we need to define the position of crakshaft at 0 degree angle. The convention is to define 0 degree angle of Crankshaft when it is at extremely top position (TDC or TOS), similarly, 180 degree is extremely bottom position (BDC or BOS). 
Two parameters are extremely important in sizing of a press with Slider crank mechanism. One is the maximum pressing force you can take from Slider. Another is the maximum Crankshaft torque. Force is simple to understand and implement in design, but Crankshaft torque is a bit tricky to understand. With higher Crankshaft torque, we can get higher force throughout the storke of Slider. This can be quantified by a parameter named Rated Distance. Rated distance is the distance of Slider from BDC where we can take rated press force from Slider. Higher the rated distance, higher will be the torque required at Crankshaft.
Because of the kinematics of Slider crank mechanism, Slider can give theoritically infinite force at 180 degree (BDC) with almost neglegible torque requirement at Crankshaft. This can be a matter of concern for the structure of press because any structure can take finite amount of load only. To prevent overloading of structure, a separare overload prevention device is required. Generally, connecting rod length should be more than or equal to 3 times of the stroke. For large strokes of slide, Eccentric gear is used in place of Crankshaft. The calculations for eccentric gear are same as with Crankshaft.

This module can be used to calculate torque required for an eccentric drive press. The torque output is based on the consideration of only 1 eccentric gear. Besides torque, it can also calculate slide position "from bottom of stroke" (FBOS) and acceleration at a given angle of Crankshaft.
"""

from mechpress import ed

stroke = 0.150  # m
conrod = 0.9  # m
rd = 0.013  # m
fr = 6300000  # N

th2_deg = 110  # deg
th2_rad = math.pi * th2_deg / 180  # rad
n2 = 20  # rpm of crank
w2 = 2 * math.pi * n2 / 60  # ang vel of crank

press1 = ed.ED(stroke, conrod, rd, fr)  # object press1

alp_rad = press1.get_alp_rad()
print("alp_rad: ", alp_rad)

beta_rad = press1.get_beta_rad()
print("beta_rad: ", beta_rad)

t_eg = press1.get_torque()
print("EG torque is: ", t_eg)

fbos = press1.get_fbos(th2_rad)
print("FBOS: ", fbos)

vel = press1.get_slide_vel(th2_rad, w2)
print("Slide vel: ", vel)

acc = press1.get_slide_acc(th2_rad, w2, 0)
print("Slide acc: ", acc)

force = press1.get_f(th2_rad)
print("Press force: ", force)

"""
Attributes
----------
r : float
    Eccentricity or half of Press Stroke in m
l : float
    Conrod length in m
s : float
    Rated distance in m
f : float
    Press force in N

Methods
-------
get_alp_rad():
	Returns the rated angle of crank in radian
get_beta_rad():
	Returns the rated angle of conrod in radian
get_torque():
	Returns the rated torque at Eccentric Gear in Nm
get_fbos(th2_rad):
	Returns the Slide distance FBOS (From Bottom Of Stroke) at given angle in m
get_slide_vel(th2_rad, w2):
	Returns the Slide velocity (in m/s) at given angle and angular velocity of crank
get_slide_acc(th2_rad, w2, alp2):
	Returns the Slide acceleration (in m/s2) at given angle, angular velocity and angular acceleration of crank
get_f(th2_rad):
	Returns the Available force (in N) at given crank angle
"""

------------------------------ Module 2: ld.py ---------------------------------

"""
About ld:
Please read about ed press before reading further.
ld is for Link Drive press. It is slightly different from Eccentric drive press in construction. To reduce the speed of slider in forming zone, few extra links are provided in this mechanism. Generally, these presses are driven by eccentric gears rather than crankshaft. Eccnetric gear is driven by a pinion which is driven by a  motor. There are 3 links in this system: Ternary link with 3 joints, rocker link with 2 joints and connecting rod with 2 joints. Rocker link is connected to Crown at one end and with ternary link at other. Connecting rod is connected with ternary link at oner end and slide to another. Ternary link is also connected to eccentric gear's eccentric portion. Eccentric gears rotates at constant speed. Due to linkage mechanism, Slide moves slowly in forming zone (bottom 1/3rd zone of forward motion) and fast in return stroke.

This module can be used to calculate torque required for link drive press. The torque output is based on the consideration of only 1 eccentric gear. Besides torque, it can also calculate TDC and BDC angle, slide position "from bottom of stroke" (FBOS) and velocity at all the angles of Eccentric gear.
"""

from mechpress import ld

press2 = ld.LD(0.30, 0.8, 0.9, 1.2, 0.4, 2.33923, 1.3, 0, 1.4, 10000000, 0.013)

print("Stroke: ", press2.get_stroke())
print("EG torque: ", press2.get_eg_torque())

th2_lst = press2.get_th2_decideg_lst()
fbos_lst = press2.get_fbos_lst()
vel_lst = press2.get_vel_lst(2)

print("TDC: ", press2.get_th2_tdc())
print("BDC: ", press2.get_th2_bdc())

"""
Attributes
----------
a : float
    Eccentricity in m
b : float
    Ternary link length (rocker side) in m
c : float
    Rocker link length in m
d : float
    Rocker x distance from Eccentric Gear rotating center in m (+ve value only)
f : float
    Rocker y distance from Eccentric Gear rotating center in m (+ve value only)
tht:float
	Obtuse angle between 2 sides of ternary link in radian
g : float
    Conrod length (connected to slide) in m
h : float
    Slide offset in m (+ve value if offset is away from rocker side)
m : float
    Ternary link length (conrod side) in m
fr: float
    Rated press force in N
rd: float
    Rated distance in m

Methods
-------
get_stroke():
	Returns Slide stroke in m
get_eg_torque():
	Returns the rated torque at Eccentric Gear in Nm
get_th2_decideg_lst():
	Returns the list of crank angle for 1 complete rotation in resolution of 0.1 deg
get_fbos_lst():
	Returns the list of fbos with respect to th2_decideg_lst
get_vel_lst(w2):
	Returns the list of slide velocity with respect to th2_decideg_lst at given angular velocity of crank
get_th2_tdc():
	Returns crank angle at TDC in deg
get_th2_bdc():
	Returns crank angle at BDC in deg

Notes
-----

Folowing sketch is for reference only.
Actual sketch considered in the program is mirror of this.

............f............

                 o
              / / \\
O1          /  /   \\        .
|         /   /     c        .
|       b    /       \\      d
a     /     /         \\     .
|   /      /           O2    .
| /       /
o        /
|       /
|      /
|     /
m    /
|   /
|  /
| /
|/
o
|
|
|
|
g
|
|
|
|
O3


O1 is Eccentric gear rotation center
O2 is rocker link pivot point
O3 is slide connection point
"""

------------------------------ Module 3: crown.py ---------------------------------

"""
About crown:
Crown is one of the main structural component of mechanical press. It houses drive components like gears, shafts links etc. It also transfers press force to tie rods. It acts like a simply supported beam where tie rod acts as supports and eccentric gear pin acts as load points.
Bending and shear stresses are generated in crown when press applies load. Crown also deflects due to bending and shear forces.
This module can be used to determine stresses and defelction in crown due to load. The maximum stress and deflection comes in the center of the crown in left to right direction.
Generally stresses are limited to 50 N/mm2 and deflection is limited to 0.2mm/m at center. Deflection calculated by this module is the total deflection at center. It should be divided by tie rod center distance to get the value in mm/m. For example, if the tie rod center distance is 5000 mm and deflection at center is 0.8 mm, then deflection in mm/m = 0.8 / 5 = 0.16 mm/m
"""


from mechpress import crown

c1 = crown.Crown(12500000, 5, 3, 1.2, 0.4245, 0.2, 2)
print("Bending stress (MPa): ", c1.get_sb() / 1000000)
print("Shear stress (MPa): ", c1.get_ss() / 1000000)
print("Def in bending (mm): ", c1.get_def_b() * 1000)
print("Def in shear (mm): ", c1.get_def_s() * 1000)

"""
Attributes
----------
fr : float
	rated force of press in N
l : float
	Tie rod center distance in m
sus_cd : float
	Distance between suspensions in m
y : float
	distance of farthest fiber from centroid in m
i : float
	section inertia in m4
x2 : float
	section web width in m
y2 : float
	section web height in m
e : float (Optional)
	Youngs modulus in N/m2
g : float (Optional)
	shear modulus in N/m2

Methods
-------
get_sb():
	Returns the stress due to bending in N/m2
get_ss():
	Returns the stress due to shear in N/m2
get_def_b():
	Returns the deflection due to bending in m
get_def_s():
	Returns the deflection due to shear in m
"""

------------------------------ Module 4: bed.py ---------------------------------

"""
About bed
Bed (also known as Bottom Head) is one of the main structural component of mechanical press. It is the bottom most part of structure. It takes the vertical load of forming which comes from the bolster plate which is mounted on top of the bed. It also transfers press force to tie rods. It acts like a simply supported beam where tie rod acts as supports and bolster acts as Uniformly distributed load.
Bending and shear stresses are generated in bed when press applies load. Bed also deflects due to bending and shear forces.
This module can be used to determine stresses and defelction in bed due to load. The maximum stress and deflection comes in the center of the bed in left to right direction.
Generally stresses are limited to 50 N/mm2 and deflection is limited to 0.17mm/m at center. Deflection calculated by this module is the total deflection at center. It should be divided by tie rod center distance to get the value in mm/m. For example, if the tie rod center distance is 6000 mm and deflection at center is 1 mm, then deflection in mm/m = 1 / 6 = 0.167 mm/m
"""

from mechpress import bed

b1 = bed.Bed(12500000, 5, 4, 0.66, 1.2, 0.4245, 0.2, 2)
print("Bending stress (MPa): ", b1.get_sb() / 1000000)
print("Shear stress (MPa): ", b1.get_ss() / 1000000)
print("Def in bending (mm): ", b1.get_def_b() * 1000)
print("Def in shear (mm): ", b1.get_def_s() * 1000)

"""
Attributes
----------
fr : float
	rated force of press in N
l : float
	Tie rod center distance in m
lr : float
	Bolster Left to Right size in m
pc_l : float
	percentage length in LR on which load will act on bolster
y : float
	distance of farthest fiber from centroid in m
i : float
	section inertia in m4
x2 : float
	section web width in m
y2 : float
	section web height in m
e : float (Optional)
	Youngs modulus in N/m2
g : float (Optional)
	shear modulus in N/m2

Methods
-------
get_sb():
	Returns the stress due to bending in N/m2
get_ss():
	Returns the stress due to shear in N/m2
get_def_b():
	Returns the deflection due to bending in m
get_def_s():
	Returns the deflection due to shear in m
"""

------------------------------ Module 5: slide.py ---------------------------------


"""
About slide
Slide is one of the main structural component of mechanical press. It is the moving part of press which applies load on the die. It takes the vertical load of forming which comes from the upper die which is mounted on the slide. It also transfers press force from top die to connecting rods. It acts like a simply supported beam where connecting rod acts as supports and top die acts as Uniformly distributed load.
Bending and shear stresses are generated in slide when press applies load. Slide also deflects due to bending and shear forces.
This module can be used to determine stresses and defelction in slide due to load. The maximum stress and deflection comes in the center of the slide in left to right direction. 
Generally stresses are limited to 50 N/mm2 and deflection is limited to 0.17mm/m at center. Deflection calculated by this module is the total deflection at center. It should be divided by suspension center distance to get the value in mm/m. For example, if the susepnsion center distance is 4000mm and deflection at center is 0.6 mm, then deflection in mm/m = 0.6 / 4 = 0.15 mm/m
"""


from mechpress import slide

s1 = slide.Slide(12500000, 3, 4, 0.66, 1.2, 0.4245, 0.2, 2)
print("Bending stress (MPa): ", s1.get_sb() / 1000000)
print("Shear stress (MPa): ", s1.get_ss() / 1000000)
print("Def in bending (mm): ", s1.get_def_b() * 1000)
print("Def in shear (mm): ", s1.get_def_s() * 1000)

"""
Attributes
----------
fr : float
	rated force of press in N
l : float
	center distance between suspension in m
lr : float
	Bolster Left to Right size in m
pc_l : float
	percentage length in LR on which load will act on bolster
y : float
	distance of farthest fiber from centroid in m
i : float
	section inertia in m4
x2 : float
	section web width in m
y2 : float
	section web height in m
e : float (Optional)
	Youngs modulus in N/m2
g : float (Optional)
	shear modulus in N/m2

Methods
-------
get_sb():
	Returns the stress due to bending in N/m2
get_ss():
	Returns the stress due to shear in N/m2
get_def_b():
	Returns the deflection due to bending in m
get_def_s():
	Returns the deflection due to shear in m
"""



------------------------------ Module 6: section_mi.py ---------------------------------


"""
about section_mi
This module is used to calculate section properties like centroid, second moment of area etc of I beam. I beam consists of 3 main rectangular sections: Top flange, Web and bottom flange. This module also gives provision to include top and bottom reinforced plates. 

"""


from mechpress import section_mi

my_sec = section_mi.Section_mi(100, 10, 10, 100, 100, 10, 5, 25, 5, 25)
print(my_sec.get_centroid())
print(my_sec.get_case())
print(my_sec.get_inertia())
print(my_sec.get_section_area())

"""
Attributes
----------
x1 : float
	top flange with of I beam in m
y1 : float
	top flange thickness of I beam in m
x2 : float
	web thickness of I beam in m
y2 : float
	web height of I beam in m
x3 : float
	bottom flange with of I beam in m
y3 : float
	bottom flange thickness of I beam in m
x4 : float
	top reinforced plate thickness of I beam in m
y4 : float
	top reinforced plate height of I beam in m
x5 : float
	bottom reinforced plate thickness of I beam in m
y5 : float
	bottom reinforced plate height of I beam in m

Methods
-------
get_centroid():
	Returns the centroid of section from bottom in m
get_section_area():
	Returns the section area in m2
get_inertia():
	Returns the section inertia in m4
"""



------------------------------ Module 7: polynomial_345.py ---------------------------------


"""
about polynomial_345
This module is used to calculate the distance, velocity and acceleration function of a 3-4-5 polynomial. Input of the function is the travel time, distance to be covered and idle time. Output if the list of distance, velocity and acceleration at each millisecond.

"""
from mechpress import polynomial_345

poly = polynomial_345.Polynomial_345(800, 1, 0.2)

t_lst = poly.t_lst_fcn()
s_lst = poly.s_lst_fcn()
v_lst = poly.v_lst_fcn()
a_lst = poly.a_lst_fcn()
v_pk = poly.v_max_fcn()
a_pk = poly.a_max_fcn()
a_rms = poly.a_rms_fcn()

print("max velocity (mm/s): ", v_pk)
print("max acceleration (m/s2): ", a_pk)
print("rms acceleration (m/s2): ", a_rms)

"""
Attributes
----------
s : float
    distance to be travelled in mm
t : float
    time in which distance to be travelled in second
ti : float
    idle time in second
    

Methods
-------
t_lst_fcn():
    returns time list in ms
s_lst_fcn():
    returns distance list in mm
v_lst_fcn():
    returns velocity list in mm/s
a_lst_fcn():
    returns acceleration list in m/s2
v_max_fcn():
    returns max velocity in mm/s
a_max_fcn():
    returns max acceleration in m/s2
a_rms_fcn():
    returns rms acceleration in m/s2

"""



------------------------------ Module 8: automation_345.py ---------------------------------


"""
about automation_345
This module is used to select the servo motor for a linear axis. It is based on a single axis automation system which is driven by a servo motor. A gearbox is coupled with servo motor. Timing pulley is mounted on the output shaft of gearbox. Timing pulley drives the timing belt which is connected to a actuator bar or arm. This arm moves in linear direction as motor rotates. The arm is guided through Linear guides. The movement of arm is horizontal so servo motor is not oving it against gravity. However, there will be friction force due to arm's weight on Linear guides. Motor must overcome this frictional force if arm is to be moved. Additional resistance force (if any) can also be defined in the module.
The output of the module is list of all important parameters like distance, velocity, acceleration, rpm, torque etc. Values of peak velocity, acceleration, torque, rpm can also be takem as output. 

"""

from mechpress import automation_345

axis1 = automation_345.Automation_345(1200, 2, 90, 50, 0.02, 500, 0.02, 0.005, 0.003, 10, 0.5)
t_lst = axis1.get_t_lst()
s_lst = axis1.get_s_lst()
v_lst = axis1.get_v_lst()
trq_lst = axis1.get_trq_mot_lst()
n_lst = axis1.get_n_mot_lst()

t_mot_rms = axis1.get_t_mot_rms()
t_mot_pk = axis1.get_t_mot_pk()
n_mot_avg = axis1.get_n_mot_avg()
n_mot_pk = axis1.get_n_mot_pk()
a_pk = axis1.get_a_pk()
v_pk = axis1.get_v_pk()

print("RMS torque of motor (Nm): ", t_mot_rms)
print("Peak torque of motor (Nm): ", t_mot_pk)
print("Average rpm of motor: ", n_mot_avg)
print("Peak rpm of motor: ", n_mot_pk)
print("Peak acceleration (m/s2): ", a_pk)
print("Peak velocity (mm/s): ", v_pk)


"""
Attributes
----------
s : float
	distance to be travelled in mm
t : float
	time in which distance to be travelled in second
d_pu : float
	pulley pcd in mm
m : float
	moving mass in kg
cof : float
	coefficient of friction
f_res : float
	force opposing motion in N
j_pu : float
	timing pulley inertia in kgm2
j_mot : float
	motor inertia in kgm2
j_gb : float
	gearbox inertia in kgm2
gr : float
	gear ratio of gearbox
t_idle : float
	idle time after motion in s


Methods
-------
get_t_lst():
	returns time list in ms
get_s_lst():
	returns distance list in mm
get_v_lst():
	returns velocity list in mm/s
get_a_lst():
	returns acceleration list in m/s2
get_n_mot_lst():
	returns motor rpm list
get_trq_mot_lst():
	returns motor torque list in Nm
get_t_mot_rms():
	returns motor rms torque list in Nm
get_t_mot_pk():
	returns motor peak torque in Nm
get_n_mot_avg():
	returns motor average rpm
get_n_mot_pk():
	returns motor peak rpm
get_a_pk():
	returns peak acceleration in m/s2
get_v_pk():
	returns peak velocity in mm/s

"""