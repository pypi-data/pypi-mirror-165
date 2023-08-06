import math

class ED:
	"""
	A class to represent a Eccentric Drive Mechanical Press

	...

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

	def __init__(self, r, l, s, f):
		"""
        Constructs all the necessary attributes for the ED (EccentricDrive) object.

        Parameters
        ----------
		r : float
		    Eccentricity or half of Press Stroke in m
		l : float
		    Conrod length in m
		s : float
		    Rated distance in m
		f : float
		    Press force in N
		"""
		self.r = r  # eccentricity in m
		self.l = l  # con rod length in m
		self.s = s  # rated distance in m
		self.f = f  # press force in N
		self.c1 = self.r + self.l - self.s
		self.alp_rad = math.acos((self.r**2 + self.c1**2 -self.l**2)/(2*self.r*self.c1))  # rated angle in rad
		self.alp_deg = self.alp_rad * 180 / math.pi
		self.beta_rad = math.acos((self.l**2 + self.c1**2 -self.r**2)/(2*self.l*self.c1))  # conrod rated angle 
		self.beta_deg = self.beta_rad * 180 / math.pi
		self.t = self.f * self.r * (math.sin(self.alp_rad) + math.cos(self.alp_rad)*math.tan(self.beta_rad))  # torque at EG in Nm

		"""
		Following code is for generating list for plotting graph
		It will be activated in future revision

		TH2_S_DEG = 90  # start crank angle in deg
		self.th2_deg_lst = []  # crank angle from tdc in deg
		self.f_lst = []  # press force in N
		self.fbos_lst = []  # fbos in m
		self.th2_deg_lst.clear()
		self.f_lst.clear()
		self.fbos_lst.clear()
		for x in range(TH2_S_DEG, 181):
		    self.th2_deg_lst.append(x)
		    this_th2_rad = x * math.pi / 180  # crank angle from tdc in rad
		    this_alp_rad = math.pi - this_th2_rad  # crank angle from BDC
		    this_beta_rad = math.asin(self.r * math.sin(this_th2_rad) / self.l)
		    this_fbos = self.r + self.l - (self.l * math.cos(this_beta_rad) - self.r * math.cos(this_th2_rad))
		    self.fbos_lst.append(this_fbos)
		    try:
		        this_f = self.t / (self.r * (math.sin(this_alp_rad) + math.cos(this_alp_rad)*math.tan(this_beta_rad)))  # force in N
		    except ZeroDivisionError:
		        this_f = self.f
		    
		    if this_f > self.f:
		        this_f = self.f

		    self.f_lst.append(this_f)
		"""

    
	def get_alp_rad(self):
		"""
		Returns the rated angle of crank in radian

		Parameters
		----------

		Returns
		-------
		float
		Returns the rated angle of crank in radian
		"""
		return self.alp_rad


	def get_beta_rad(self):
		"""
		Returns the rated angle of conrod in radian

		Parameters
		----------

		Returns
		-------
		float
		Returns the rated angle of conrod in radian
		"""
		return self.beta_rad

	def get_torque(self):
		"""
		Returns the rated torque at Eccentric Gear in Nm

		Parameters
		----------

		Returns
		-------
		float
		Returns the rated torque at Eccentric Gear in Nm
		"""
		return self.t

	def get_fbos(self, th2_rad):
		"""
		Returns the Slide distance FBOS (From Bottom Of Stroke) at given angle in m

		Parameters
		----------
		th2_rad : float
		    Crank angle from TDC in rad

		Returns
		-------
		float
		Returns the FBOS in m
		"""
		th3_rad = math.asin(self.r * math.sin(th2_rad) / self.l)  #conrod angle in rad
		fbos = self.l + self.r - (self.l * math.cos(th3_rad) - self.r * math.cos(th2_rad))
		return fbos  # in m

	def get_slide_vel(self, th2_rad, w2):
		"""
		Returns the Slide velocity (in m/s) at given angle and angular velocity of crank

		Parameters
		----------
		th2_rad : float
		    Crank angle from TDC in rad

		w2 : float
		    Angular velocity of crank in rad/s

		Returns
		-------
		float
		Returns the Slide velocity in m/s
		"""
		th3_rad = math.asin(self.r * math.sin(th2_rad) / self.l)  #conrod angle in rad
		w3 = self.r * math.cos(th2_rad) * w2 / (self.l * math.cos(th3_rad))
		slide_vel = self.r * w2 * math.sin(th2_rad) - self.l * w3 * math.sin(th3_rad)  # in m/s
		return slide_vel  # in m/s
	
	def get_slide_acc(self, th2_rad, w2, alp2):
		"""
		Returns the Slide acceleration (in m/s2) at given angle, angular velocity and angular acceleration of crank

		Parameters
		----------
		th2_rad : float
		    Crank angle from TDC in rad

		w2 : float
		    Angular velocity of crank in rad/s

		alp2 : float
		    Angular acceleration of crank in rad/s2

		Returns
		-------
		float
		Returns the Slide acceleration in m/s2
		"""
		th3_rad = math.asin(self.r * math.sin(th2_rad) / self.l)  # conrod angle in rad
		w3 = self.r * math.cos(th2_rad) * w2 / (self.l * math.cos(th3_rad))
		alp3 = (self.r * alp2 * math.cos(th2_rad) - self.r * w2**2 * math.sin(th2_rad) + self.l * w3**2 * math.sin(th3_rad)) / (self.l * math.cos(th3_rad))
		slide_acc = self.r * alp2 * math.sin(th2_rad) + self.r * w2**2 * math.cos(th2_rad) - self.l * alp3 * math.sin(th3_rad) - self.l * w3**2 * math.cos(th3_rad)
		return slide_acc  # in m/s2

	def get_f(self, th2_rad):
		"""
		Returns the Available force (in N) at given crank angle

		Parameters
		----------
		th2_rad : float
		    Crank angle from TDC in rad

		Returns
		-------
		float
		Returns the available press force in N
		"""
		th3_rad = math.asin(self.r * math.sin(th2_rad) / self.l)  # conrod angle in rad
		f_this = self.t * math.cos(th3_rad) / (self.r * math.sin((math.pi - th2_rad) + th3_rad))
		if f_this > self.f:
			f_this = self.f
		return f_this  # in N