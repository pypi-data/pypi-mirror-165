import math
# this class has been validated with excel sheet

class Bed:
	"""
	A class for calculation of Bottom Head of a mechanical press

	...

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
	def __init__(self, fr, l, lr, pc_l, y, i, x2, y2, e = 21E10, g = 8E10):
		"""
        Constructs all the necessary attributes for the Bed object.

        Parameters
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
		"""
		self.fr = fr  # press force in N
		self.l = l  # tie rod CD in m
		self.lr = lr  # Bolster LR in m
		self.pc_l = pc_l  # % length for load
		self.y = y  # distance of farthest fiber from centroid in m
		self.i = i  # section mi in m4
		self.x2 = x2  # section web width in m
		self.y2 = y2  # section web height in m
		self.e = e  # youngs modulus in N/m2
		self.g = g  # shear modulus in N/m2

		self.b = self.pc_l * self.lr  # UDL length
		self.a = (self.l - self.b) / 2  # distance of toe rod from start 
		# of load on bolster in m
		self.q = self.fr / self.b  # UDL in N/m
		self.bm = self.q * self.b * (self.a + 0.25 * self.b) / 2
		# bending moemnt at center (max) Nm
		self.v = self.fr / 2  # Shear force in N

		self.s_b = self.bm * self.y / self.i  # N/m2  stress in bending
		self.s_s = 1.5 * self.v / (self.x2 * self.y2)  # N/m2  stress in shear
		self.def_b = self.q * self.l**2 * (self.l**2 - 4 * self.a**2) / (64 * self.e * self.i) - \
			self.q * (self.l**4 - 16 * self.a**4) / (384 * self.e * self.i)  # deflection due to bending in m
		self.def_s1 = 1.5 * self.a * self.b * self.q / (2 * self.x2 * self.y2 * self.g)
		# def_s1 is the deflection in length of constant shear force
		self.def_s2 = 1.5 * self.q * (self.b * self.l / 2 - self.l**2/4 + self.a * self.l - \
			self.a * self.b - self.a**2) / (2 * self.x2 * self.y2 * self.g)
		# def_s2 is the deflection in length where UDL is acting
		self.def_s = self.def_s1 + self.def_s2  # total deflection in shear at center
		# above is deflection due to shear in m

	def get_sb(self):
		"""
		Returns the stress due to bending in N/m2

		Parameters
		----------

		Returns
		-------
		float
		Returns the stress due to bending in N/m2
		"""
		return self.s_b  # N/m2  stress in bending

	def get_ss(self):
		"""
		Returns the stress due to shear in N/m2

		Parameters
		----------

		Returns
		-------
		float
		Returns the stress due to shear in N/m2
		"""
		return self.s_s  # N/m2  stress in shear

	def get_def_b(self):
		"""
		Returns the deflection due to bending in m

		Parameters
		----------

		Returns
		-------
		float
		Returns the deflection due to bending in m
		"""
		return self.def_b
		# deflection due to bending in m

	def get_def_s(self):
		"""
		Returns the deflection due to shear in m

		Parameters
		----------

		Returns
		-------
		float
		Returns the deflection due to shear in m
		"""
		return self.def_s 
		# above is deflection due to shear in m

# def __init__(self, fr, l, lr, pc_l, y, i, x2, y2, e = 21E10, g = 8E10):
# b1 = Bed(12500000, 5, 4, 0.66, 1.2, 0.4245, 0.2, 2)
# print("Bending stress (MPa): ", b1.get_sb() / 1000000)
# print("Shear stress (MPa): ", b1.get_ss() / 1000000)
# print("Def in bending (mm): ", b1.get_def_b() * 1000)
# print("Def in shear (mm): ", b1.get_def_s() * 1000)
