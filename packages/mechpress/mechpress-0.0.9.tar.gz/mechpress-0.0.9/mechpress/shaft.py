import math

class Shaft:
	"""
	A class to calculate shaft diameter which is under torsion and bending moment 
	using ASME Elliptic equation

	...

	Attributes
	----------
	tm : float
		Midrange torsion in Nm
	ta : float
		Alternate torsion in Nm
	mm : float
		Midrange bending moment in Nm
	ma : float
		Alternate bending moment in Nm
	kf : float
		fatigue stress concentration factor for bending
	kfs : float
		fatigue stress concentration factor for torsion
	se : float
		endurance strength of shaft material in N/m2
	sy : float
		yield strength of shaft material in N/m2
	n : float
		factor of safety

	Methods
	-------
	get_shaft_dia():
		Returns the shaft diameter in m
	"""

	def __init__(self, tm, ta, mm, ma, kf, kfs, se, sy, n):
		"""
        Constructs all the necessary attributes for the Shaft object.

        Parameters
        ----------
		tm : float
			Midrange torsion in Nm
		ta : float
			Alternate torsion in Nm
		mm : float
			Midrange bending moment in Nm
		ma : float
			Alternate bending moment in Nm
		kf : float
			fatigue stress concentration factor for bending
		kfs : float
			fatigue stress concentration factor for torsion
		se : float
			endurance strength of shaft material in N/m2
		sy : float
			yield strength of shaft material in N/m2
		n : float
			factor of safety
		"""
		k1 = 4 * (kf * ma / se)**2
		k2 = 3 * (kfs * ta / se)**2
		k3 = 4 * (kf * mm / sy)**2
		k4 = 3 * (kfs * tm / sy)**2
		k = k1 + k2 + k3 + k4
		self.d = (16 * n * k**0.5 / math.pi)**(1/3)  # shaft dia in m

    
	def get_shaft_dia(self):
		"""
		Returns the shaft diameter in mm

		Parameters
		----------

		Returns
		-------
		float
		Returns the shaft diameter in m
		"""
		return self.d

# def __init__(self, tm, ta, mm, ma, kf, kfs, se, sy, n)
# s1 = Shaft(10000, 25000, 5000, 35000, 2, 2, 180_000_000, 240_000_000, 1.5)
# print("Shaft diameter (mm): ", s1.get_shaft_dia() * 1000)
