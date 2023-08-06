import math

class LD:
	"""
	A class to represent a 6 Link Drive Mechanical Press

	...

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

	def __init__(self, a, b, c, d, f, tht, g, h, m, fr, rd):

		"""
        Constructs all the necessary attributes for the LD (6 Link Drive) object.

		Parameters
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
		

		Note
		----
		Positive X axis is considered zero degree crank angle.
		Counter clockwise direction is considered as positive for angle rotation.
		This is similar to cartesian coordinate system.
		When crank angle (th2...) = 0, slide in near mid stroke.
		if th2 increases from 0 deg, slide moves towards TDC.
		"""
		self.a = a  # eccentricity
		self.b = b  # ternary link length rocker side
		self.c = c  # rocker length
		self.d = d  # rocker x (+ve value only)
		self.f = f  # rocker y (+ve value only)
		
		self.tht = tht  # ternary link angle
		self.g = g  # conrod length
		self.h = h  # slide offset  (+ve value if offset is away from rocker side)
		self.m = m  # ternary link length conrod side

		self.fr = fr  # rated press force in N
		self.rd = rd  # rated distance of press in m

		self.k1 = d/a
		self.k2 = d/c
		self.k3 = (a**2 - b**2 + c**2 + d**2 + f**2)/(2 * a * c)
		self.k4 = f/c
		self.k5 = f/a

		self.th2_decideg_lst = []
		self.k_lst = []
		self.vel_lst = []

		self.w2 = 1  # crank ang vel in rad/s assumed as 1 rad/s

		for th2_decideg in range(3601):
			th2 = math.pi * (th2_decideg / 10) / 180  # crank angle in rad
			self.th2_decideg_lst.append(th2)

			A = math.cos(th2) + self.k1 + self.k3 + self.k2 * math.cos(th2) + self.k4 * math.sin(th2)
			B = -2 * math.sin(th2) - 2 * self.k5
			C = self.k3 + self.k2 * math.cos(th2) + self.k4 * math.sin(th2) - math.cos(th2) - self.k1

			th4 = 2 * math.atan((-B + math.pow(B**2 - 4 * A * C, 0.5)) / (2 * A))
			th3 = math.acos(c * math.cos(th4)/b - a * math.cos(th2) / b - d / b)
			th7 = th3 - (math.pi - tht)
			th8 = math.acos(a * math.cos(th2) / g - m * math.cos(th7) / g - h / g)
			k = - a * math.sin(th2) + m * math.sin(th7) + g * math.sin(th8)  # k is slide position from eg rotating center
			self.k_lst.append(k)


			w4 = self.w2 * (a/c) * (math.sin(th3 - th2) / math.sin(th3 - th4))
			w3 = c * w4 * math.sin(th4) / (b * math.sin(th3)) - a * self.w2 * math.sin(th2) / (b * math.sin(th3))

			w7 = w3
			w8 = self.w2 * (a / g) * (math.sin(th2) / math.sin(th8)) - w7 * (m / g) * (math.sin(th7) / math.sin(th8)) 
			v_k = - a * self.w2 * math.cos(th2) + m * w7 * math.cos(th7) + g * w8 * math.cos(th8)
			self.vel_lst.append(v_k)


		self.min_k = min(self.k_lst)  # min distance of slide from eg center
		self.max_k = max(self.k_lst)  # max distance of slide from eg center
		self.stroke = self.max_k - self.min_k  # stroke of slide in m

	def get_stroke(self):
		"""
		Returns the stroke in m

		Parameters
		----------

		Returns
		-------
		float
		Returns the stroke in m
		"""
		return self.stroke

	def get_eg_torque(self):
		"""
		Returns the Eccentric gear torque in Nm

		Parameters
		----------

		Returns
		-------
		float
		Returns the Eccentric gear torque in Nm
		"""
		k_rd = self.max_k - self.rd  # slide position from eg center at rated distance in m
		x_at_rd = 0  # index of list of fbos at rated distance
		for x in range(3601):
			this_k = self.k_lst[x]
			this_vel = self.vel_lst[x]
			if this_vel > 0:
				if k_rd < this_k:
					x_at_rd = x - 1
					break
		vel_at_rd = self.vel_lst[x_at_rd]
		t_eg = self.fr * vel_at_rd / self.w2  # eg torque in Nm
		return t_eg
		
	def get_th2_decideg_lst(self):
		"""
		Returns the list containing crank angle

		Parameters
		----------

		Returns
		-------
		float
		Returns the list containing crank angle (in radian) with least count of 0.1 deg which is equal to 0.00174 radian
		"""
		return self.th2_decideg_lst  # mention about sign and index, CA = 0 in pos x axis

	def get_fbos_lst(self):
		"""
		Returns the FBOS list at each 0.1 degree in m

		Parameters
		----------

		Returns
		-------
		float
		Returns the FBOS list at each 0.1 degree in m
		"""
		fbos_lst = []
		for x in self.k_lst:
			fbos_lst.append(self.max_k - x)
		return fbos_lst

	def get_vel_lst(self, w2):
		"""
		Returns the SLide velocity list at each 0.1 degree in m/s

		Parameters
		----------

		Returns
		-------
		float
		Returns the SLide velocity list at each 0.1 degree in m/s
		"""
		vel_at_w2_lst = []
		for x in self.vel_lst:
			vel_at_w2_lst.append(x * w2)
		return vel_at_w2_lst  # mention about sign and index, CA = 0 in pos x axis

	def get_th2_tdc(self):
		"""
		Returns the crank angle at TDC in degree.
		Positive X axis is considered zero degree crank angle.
		Counter clockwise direction is considered as positive for angle rotation.
		This is similar to cartesian coordinate system.

		Parameters
		----------

		Returns
		-------
		float
		Returns the crank angle at TDC in degree
		"""
		x_at_tdc = 0  # index of list of fbos at tdc - init only
		for x in range(3601):
			this_k = self.k_lst[x]
			if this_k == self.min_k:
				x_at_tdc = x 
				break
		return x_at_tdc / 10  # in deg

	def get_th2_bdc(self):
		"""
		Returns the crank angle at BDC in degree.
		Positive X axis is considered zero degree crank angle.
		Counter clockwise direction is considered as positive for angle rotation.
		This is similar to cartesian coordinate system.

		Parameters
		----------

		Returns
		-------
		float
		Returns the crank angle at BDC in degree
		"""
		x_at_bdc = 0  # index of list of fbos at bdc - init only
		for x in range(3601):
			this_k = self.k_lst[x]
			if this_k == self.max_k:
				x_at_bdc = x 
				break
		return x_at_bdc / 10  # in deg
