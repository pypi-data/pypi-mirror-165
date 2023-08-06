
from mechpress import polynomial_345
import math

class Automation_345:
	"""
    A class for calculation of servo motor based on 345 polynomial function

    ...

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

	def __init__(self, s, t, d_pu, m, cof, f_res, j_pu, j_mot, j_gb, gr, t_idle):
		"""
        Constructs all the necessary attributes for the Automation_345 object.

        Parameters
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
        """

		self.s = s  # stroke in mm
		self.t = t  # time for stroke in s
		self.d_pu = d_pu  # pulley pcd in mm
		self.m = m  # moving mass in kg
		self.cof = cof  # coefficient of friction
		self.f_res = f_res  # any other resisting force opposing motion in N
		self.j_pu = j_pu  # pulley inertia in kgm2 (individual)
		self.j_mot = j_mot  # motor inertia in kgm2 (individual)
		self.j_gb = j_gb  # gearbox inertia in kgm2 at its input (individual)
		self.gr = gr  # gear ratio of gearbox
		self.t_idle = t_idle  # idle time after motion in s

        # declaring all list
		self.n_pu_lst = []  # pulley rpm list
		self.n_mot_lst = []  # motor rpm list
		self.w_pu_lst = []  # pulley ang vel list
		self.alp_pu_lst = []  # pulley ang acc list
		self.alp_mot_lst = []  # motor ang acc list
		self.trq_mot_lst = []  # motor torque list. Units in Nm

		# clear all lists
		self.n_pu_lst.clear()
		self.n_mot_lst.clear()
		self.w_pu_lst.clear()
		self.alp_pu_lst.clear()
		self.alp_mot_lst.clear()
		self.trq_mot_lst.clear()

        # calculations
		self.j_t_mot = self.j_mot + self.j_gb + (self.j_pu / self.gr**2) + (self.m * (self.d_pu/2000)**2) / self.gr**2  #  total inertia taken at motor in kgm2
		self.f_cof = self.m * 9.8 * self.cof  # friction fornce in N
		self.f_res_tot = self.f_res + self.f_cof  # resistance force in N 
		self.trq_res_tot_pu = self.f_res_tot * (self.d_pu/2000)  # resistance torque on pulley in Nm
		self.trq_res_tot_mot = self.trq_res_tot_pu / self.gr  # resistance torque on motor in Nm

        # making object of 345 polynomial
		self.curveGen = polynomial_345.Polynomial_345(self.s, self.t, self.t_idle)

        # getting calculation answers from object methods
		self.T_ms = self.curveGen.t_fcn()
		self.t_lst = self.curveGen.t_lst_fcn()
		self.s_lst = self.curveGen.s_lst_fcn()
		self.v_lst = self.curveGen.v_lst_fcn()
		self.a_lst = self.curveGen.a_lst_fcn()
		self.v_avg = self.curveGen.v_avg_fcn()
		self.v_pk = self.curveGen.v_max_fcn()
		self.a_pk = self.curveGen.a_max_fcn()
		self.a1_rms = self.curveGen.a1_rms_fcn()
		self.a_rms = self.curveGen.a_rms_fcn()


        # making list of pulley rpm and w from list of "linear velocity of belt"
		for x in range(self.T_ms + 1):
		    self.n_pu_lst.append(60 * self.v_lst[x] / (math.pi * self.d_pu))
		    self.w_pu_lst.append(2 * self.v_lst[x] / self.d_pu)
		
		# making list of motor rpm
		for x in range(self.T_ms + 1):
		    self.n_mot_lst.append(self.gr * 60 * self.v_lst[x] / (math.pi * self.d_pu))

        # calculating average rpm of pulley
		self.n_pu_avg = 60 * self.v_avg/(math.pi * self.d_pu)

        # calculating peak rpm of pulley
		self.n_pu_pk = 60 * self.v_pk / (math.pi * self.d_pu)

        # making list of pulley alpha from list of "linear acceleration of belt"
		for x in range(self.T_ms + 1):
		    self.alp_pu_lst.append(2 * self.a_lst[x] / (self.d_pu * 0.001))  # a is m/s2 and dia in m

        # making list of motor alpha from list of "pulley alpha"
		for x in range(self.T_ms + 1):
		    self.alp_mot_lst.append(self.alp_pu_lst[x] * self.gr)

        # making list of motor torque from list of "motor alpha", value of total inertia and resisting torque
		for x in range(self.T_ms + 1):
		    self.trq_mot_lst.append(self.alp_mot_lst[x] * self.j_t_mot + self.trq_res_tot_mot)

        # getting peak torque of motor form list
		self.t_mot_pk = max(self.trq_mot_lst)  # max torque on motor in Nm

        # calculating average motor rpm from average pulley rpm
		self.n_mot_avg = self.n_pu_avg * self.gr

        # calculating peak motor rpm from peak pulley rpm
		self.n_mot_pk = self.n_pu_pk * self.gr

        # calculating rms torque on motor including idle time
		self.t_mot_rms = self.j_t_mot * self.gr * self.a_rms / ((self.d_pu*0.5)*0.001)  + self.trq_res_tot_mot  # Nm
		
	def get_t_lst(self):
		"""
        returns time list in ms

        Parameters
        ----------

        Returns
        -------
        int
        returns time list in ms
        """
		return self.t_lst
	
	def get_s_lst(self):
		"""
        returns distance list in mm

        Parameters
        ----------

        Returns
        -------
        float
        returns distance list in mm
        """
		return self.s_lst
	
	def get_v_lst(self):
		"""
        returns velocity list in mm/s

        Parameters
        ----------

        Returns
        -------
        float
        returns velocity list in mm/s
        """
		return self.v_lst

	def get_a_lst(self):
		"""
        returns acceleration list in m/s2

        Parameters
        ----------

        Returns
        -------
        float
        returns acceleration list in m/s2
        """
		return self.a_lst

	def get_n_mot_lst(self):
		"""
        returns motor rpm list

        Parameters
        ----------

        Returns
        -------
        float
        returns motor rpm list
        """
		return self.n_mot_lst

	def get_trq_mot_lst(self):
		"""
        returns motor torque list in Nm

        Parameters
        ----------

        Returns
        -------
        float
        returns motor torque list in Nm
        """
		return self.trq_mot_lst

	def get_t_mot_rms(self):
		"""
        returns motor rms torque list in Nm

        Parameters
        ----------

        Returns
        -------
        float
        returns motor rms torque list in Nm
        """
		return self.t_mot_rms
	
	def get_t_mot_pk(self):
		"""
        returns motor peak torque in Nm

        Parameters
        ----------

        Returns
        -------
        float
        returns motor peak torque in Nm
        """
		return self.t_mot_pk

	def get_n_mot_avg(self):
		"""
        returns motor average rpm

        Parameters
        ----------

        Returns
        -------
        float
        returns motor average rpm
        """
		return self.n_mot_avg

	def get_n_mot_pk(self):
		"""
        returns motor peak rpm

        Parameters
        ----------

        Returns
        -------
        float
        returns motor peak rpm
        """
		return self.n_mot_pk

	def get_a_pk(self):
		"""
        returns peak acceleration in m/s2

        Parameters
        ----------

        Returns
        -------
        float
        returns peak acceleration in m/s2
        """
		return self.a_pk

	def get_v_pk(self):
		"""
        returns peak velocity in mm/s

        Parameters
        ----------

        Returns
        -------
        float
        returns peak velocity in mm/s
        """
		return self.v_pk


# axis1 = Automation_345(1200, 2, 90, 50, 0.02, 500, 0.02, 0.005, 0.003, 10, 0.5)
# t_lst = axis1.get_t_lst()
# s_lst = axis1.get_s_lst()
# v_lst = axis1.get_v_lst()
# trq_lst = axis1.get_trq_mot_lst()
# n_lst = axis1.get_n_mot_lst()

# t_mot_rms = axis1.get_t_mot_rms()
# t_mot_pk = axis1.get_t_mot_pk()
# n_mot_avg = axis1.get_n_mot_avg()
# n_mot_pk = axis1.get_n_mot_pk()
# a_pk = axis1.get_a_pk()
# v_pk = axis1.get_v_pk()

# print("RMS torque of motor (Nm): ", t_mot_rms)
# print("Peak torque of motor (Nm): ", t_mot_pk)
# print("Average rpm of motor: ", n_mot_avg)
# print("Peak rpm of motor: ", n_mot_pk)
# print("Peak acceleration (m/s2): ", a_pk)
# print("Peak velocity (mm/s): ", v_pk)