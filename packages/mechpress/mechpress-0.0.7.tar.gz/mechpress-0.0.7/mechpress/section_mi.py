class Section_mi:
	"""
	A class for calculation of I section properties for bending calculations

	...

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
	def __init__(self, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5):
		"""
        Constructs all the necessary attributes for the Section_mi object.

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
		"""
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2
		self.x3 = x3
		self.y3 = y3
		self.x4 = x4
		self.y4 = y4
		self.x5 = x5
		self.y5 = y5

		self.a1 = self.x1 * self.y1
		self.a2 = self.x2 * self.y2
		self.a3 = self.x3 * self.y3
		self.a4 = self.x4 * self.y4
		self.a5 = self.x5 * self.y5

		self.at = self.a1 + self.a2 + self.a3 + self.a4 + self.a5

		c1 = self.y2 + self.y3 + 0.5 * self.y1
		c2 = self.y3 + 0.5 * self.y2
		c3 = 0.5 * self.y3
		c4 = self.y2 + self.y3 - 0.5 * self.y4
		c5 = self.y3 + 0.5 * self.y5

		self.c = (self.a1 * c1 + self.a2 * c2 + self.a3 * c3 + self.a4 * c4 + 
			self.a5 * c5) / self.at

		self.case = 0
		self.inertia = 0


		if self.c >= self.y2 + self.y3:
			self.case = 1
			self.inertia = self.get_inertia_case1()
		elif self.c < (self.y2 + self.y3) and self.c >= (self.y2 + self.y3 - self.y4):
			self.case = 2
			self.inertia = self.get_inertia_case2()
		elif self.c < (self.y2 + self.y3 - self.y4) and self.c >= (self.y3 + self.y5):
			self.case = 3
			self.inertia = self.get_inertia_case3()
		elif self.c < (self.y3 + self.y5) and self.c >= self.y3:
			self.case = 4
			self.inertia = self.get_inertia_case4()
		elif self.c < self.y3:
			self.case = 5
			self.inertia = self.get_inertia_case5()

	def get_centroid(self):
		"""
		Returns the centroid of section from bottom in m

		Parameters
		----------

		Returns
		-------
		float
		Returns the centroid of section from bottom in m
		"""
		return self.c

	def get_case(self):
		return self.case

	def get_section_area(self):
		"""
		Returns the section area in m2

		Parameters
		----------

		Returns
		-------
		float
		Returns the section area in m2
		"""
		return self.at

	def get_inertia_case1(self):
		i = 0
		yu = self.y1 + self.y2 + self.y3 - self.c
		yl = self.c - self.y3 - self.y2
		ci1u = 0.5 * yu
		ci1l = 0.5 * yl
		ci2 = 0.5 * self.y2 + yl
		ci3 = 0.5 * self.y3 + self.y2 + yl
		ci4 = 0.5 * self.y4 + yl
		ci5 = self.y2 + yl - 0.5 * self.y5

		i1u = self.x1 * yu**3 / 12
		i1l = self.x1 * yl**3 / 12
		i2 = self.x2 * self.y2**3 / 12
		i3 = self.x3 * self.y3**3 / 12
		i4 = self.x4 * self.y4**3 / 12
		i5 = self.x5 * self.y5**3 / 12

		a1u = self.x1 * yu
		a1l = self.x1 * yl

		i = (i1u + a1u * ci1u**2) + (i1l + a1l * ci1l**2) + (i2 + self.a2 * ci2**2) + \
			(i3 + self.a3 * ci3**2) + (i4 + self.a4 * ci4**2) + (i5 + self.a5 * ci5**2)

		return i

	def get_inertia_case2(self):
		i = 0
		yu = self.y2 + self.y3 - self.c
		yl = self.c - self.y3
		yl2=self.y4-yu

		ci1 = 0.5 * self.y1+yu
		ci2u = 0.5 * yu
		ci2l = 0.5 * yl
		ci3 = 0.5 * self.y3 + yl
		ci4u = 0.5 * yu
		ci4l = 0.5*yl2
		ci5 = yl - 0.5 * self.y5

		i1 = self.x1 * self.y1**3 / 12
		i2u = self.x2 * yu**3 / 12
		i2l = self.x2 * yl**3 / 12
		i3 = self.x3 * self.y3**3 / 12
		i4u = self.x4 * yu**3 / 12
		i4l = self.x4 * yl2**3 / 12
		i5 = self.x5 * self.y5**3 / 12

		a2u = self.x2 * yu
		a2l = self.x2 * yl
		a4u = self.x4 * yu
		a4l = self.x4 * yl2

		i = (i1 + self.a1 * ci1**2) + (i2u + a2u * ci2u**2) + (i2l + a2l * ci2l**2) + \
			(i3 + self.a3 * ci3**2) + (i4u + a4u * ci4u**2) + (i4l + a4l * ci4l**2) + \
			(i5 + self.a5 * ci5**2)

		return i

	def get_inertia_case3(self):
		i = 0
		yu = self.y2 + self.y3 - self.c
		yl = self.c - self.y3

		ci1 = 0.5 * self.y1 + yu
		ci2u = 0.5 * yu
		ci2l = 0.5 * yl
		ci3 = self.c - 0.5 * self.y3
		ci4 = yu - 0.5 * self.y4
		ci5 = yl - 0.5 * self.y5

		i1 = self.x1 * self.y1**3 / 12
		i2u = self.x2 * yu**3 / 12
		i2l = self.x2 * yl**3 / 12
		i3 = self.x3 * self.y3**3 / 12
		i4 = self.x4 * self.y4**3 / 12
		i5 = self.x5 * self.y5**3 / 12

		a2u = self.x2 * yu
		a2l = self.x2 * yl

		i = (i1 + self.a1 * ci1**2) + (i2u + a2u * ci2u**2) + (i2l + a2l * ci2l**2) + \
			(i3 + self.a3 * ci3**2) + (i4 + self.a4 * ci4**2) + (i5 + self.a5 * ci5**2)

		return i

	def get_inertia_case4(self):
		i = 0
		yu = self.y2 + self.y3 - self.c
		yl = self.c - self.y3
		yu2 = self.y3 + self.y5 - self.c

		ci1 = 0.5 * self.y1 + yu
		ci2u = 0.5 * yu
		ci2l = 0.5 * yl
		ci3 = 0.5 * self.y3 + yl
		ci4 = yu - 0.5 * self.y4
		ci5u = 0.5 * yu2
		ci5l = 0.5 * yl

		i1 = self.x1 * self.y1**3 / 12
		i2u = self.x2 * yu**3 / 12
		i2l = self.x2 * yl**3 / 12
		i3 = self.x3 * self.y3**3 / 12
		i4 = self.x4 * self.y4**3 / 12
		i5u = self.x5 * yu2**3 / 12
		i5l = self.x5 * yl**3 / 12

		a2u = self.x2 * yu
		a2l = self.x2 * yl
		a5u = self.x5 * yu2
		a5l = self.x5 * yl

		i = (i1 + self.a1 * ci1**2) + (i2u + a2u * ci2u**2) + (i2l + a2l * ci2l**2) + \
			(i3 + self.a3 * ci3**2) + (i4 + self.a4 * ci4**2) + \
			(i5u + a5u * ci5u**2) + (i5l + a5l * ci5l**2)
			
		return i

	def get_inertia_case5(self):
		i = 0
		yu = self.y3 - self.c
		yl = self.c

		ci1 = 0.5 * self.y1 + self.y2 + yu
		ci2 = 0.5 * self.y2 + yu
		ci3u = 0.5 * yu
		ci3l = 0.5 * yl
		ci4 = yu + self.y2 - 0.5 * self.y4
		ci5 = 0.5 * self.y5 + yu

		i1 = self.x1 * self.y1**3 / 12
		i2 = self.x2 * self.y2**3 / 12
		i3u = self.x3 * yu**3 / 12
		i3l = self.x3 * yl**3 / 12
		i4 = self.x4 * self.y4**3 / 12
		i5 = self.x5 * self.y5**3 / 12

		a3u = self.x3 * yu
		a3l = self.x3 * yl

		i = (i1 + self.a1 * ci1**2) + (i2 + self.a2 * ci2**2) + \
			(i3u + a3u * ci3u**2) + (i3l + a3l * ci3l**2) + \
			(i4 + self.a4 * ci4**2) + (i5 + self.a5 * ci5**2)
		return i

	def get_inertia(self):
		"""
		Returns the section inertia in m4

		Parameters
		----------

		Returns
		-------
		float
		Returns the section inertia in m4
		"""
		return self.inertia


# my_sec = Section_mi(100, 10, 10, 100, 100, 10, 5, 25, 5, 25)
# my_sec = Section_mi(500, 50, 100, 2000, 500, 50, 0, 0, 0, 0)
# print(my_sec.get_centroid())
# print(my_sec.get_case())
# print(my_sec.get_inertia())
# print(my_sec.get_section_area())
