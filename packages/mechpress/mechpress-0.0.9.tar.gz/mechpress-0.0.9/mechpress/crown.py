import math
# this class has been validated with excel sheet

class Crown:
	"""
	A class for calculation of Crown of a mechanical press 
	with 2 or 4 suspensions

	...

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
	def __init__(self, fr, l, sus_cd, y, i, x2, y2, e = 21E10, g = 8E10):
		"""
        Constructs all the necessary attributes for the Crown object.

        Parameters
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
		e : float
			Youngs modulus in N/m2
		g : float
			shear modulus in N/m2
		"""
		self.fr = fr  # press force in N
		self.l = l  # tie rod CD in m
		self.sus_cd = sus_cd  # suspension cd in m
		self.y = y  # distance of farthest fiber from centroid in m
		self.i = i  # section mi in m4
		self.x2 = x2  # section web width in m
		self.y2 = y2  # section web height in m
		self.e = e  # youngs modulus in N/m2
		self.g = g  # shear modulus in N/m2

		self.a = (self.l - self.sus_cd) / 2  # distance of suspension from tie rod in m
		self.f = self.fr / 2  # suspension force on one side in N
		self.bm = self.f * self.a  # bending moemnt at suspension (max) Nm
		self.v = self.f  # Shear force in N

		self.s_b = self.bm * self.y / self.i  # N/m2  stress in bending
		self.s_s = 1.5 * self.v / (self.x2 * self.y2)  # N/m2  stress in shear
		self.def_b = - self.f * self.a * (4 * self.a**2 - 3 * self.l**2) / \
		(24 * self.e * self.i)  # deflection due to bending in m
		self.def_s = 1.5 * self.a * self.v / (self.x2 * self.y2 * self.g)  
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
		return self.def_b  # deflection due to bending in m

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
		return self.def_s  # above is deflection due to shear in m

# def __init__(self, fr, l, sus_cd, y, i, x2, y2, e = 21E10, g = 8E10):
# c1 = Crown(12500000, 5, 3, 1.2, 0.4245, 0.2, 2)
# print("Bending stress (MPa): ", c1.get_sb() / 1000000)
# print("Shear stress (MPa): ", c1.get_ss() / 1000000)
# print("Def in bending (mm): ", c1.get_def_b() * 1000)
# print("Def in shear (mm): ", c1.get_def_s() * 1000)