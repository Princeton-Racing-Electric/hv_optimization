class CarData(object):
    _data=dict()

    @property
    def data(self):
        return self._data
    @data.setter
    def data(self, val):
        raise Exception("Cannot change default values!")

class Nissan_Leaf(CarData):
    def __init__(self):
        self._data = dict(batt_soc=65.0,
                    batt_v_min=300.0,
                    batt_v_max=400.0,
                    batt_i_max=266.0,
                    batt_p_max=80000.0,
                    batt_kwh=30.0,
                    car_cd=0.29,
                    car_area=0.725,
                    car_mass=1521.0,
                    wheel_diameter=0.2159*2,
                    wheel_mass=9.0, # Rough google search
                    wheel_width=0.3, # APPROX
                    #brake_diameter=[0.1]*4, # assumed
                    brake_diameter=0.1, # assumed
                    #brake_max_torque=[500.0]*4,
                    brake_max_torque=500.0,
                    motor_rotor_mass=13.6,
                    motor_rotor_diameter=0.130,
                    motor_max_torque=280,#280.0,
                    motor_max_rpm=10390,
                    motor_reduction_ratio=7.9377,
                    motor_v_max = 400.0, # assumed
                    motor_v_min=300.0, # assumed
                    motor_i_max=266.0, # assumed
                    motor_p_max=80000.0 # assumed
                    )
        super().__init__()


class PRECar(CarData):

    def __init__(self):
        self._data = dict(batt_soc=65.0,  # NEED TO FIND
                          batt_v_min=40.0,  # UNKNOWN
                          batt_v_max=117.6,
                          batt_i_max=920.0,
                          batt_p_max=90000.0,
                          batt_kwh=5.0,  # adjusted to 5 for regs 6.25 originally
                          car_cd=1.4,  # NEED TO FIGURE OUT
                          car_area=1.0,  # NEED TO FIGURE OUT
                          car_mass=231.83,  # calculated 2/17/21
                          wheel_diameter=0.508,  # NEED TO CHECK
                          wheel_mass=9.0,  # NEED TO FIND
                          wheel_width=0.3,  # NEED TO FIND
                          brake_diameter=0.165,  # Estimation with calliper
                          brake_max_torque=386.08,  # Deceleration of 20m/s^2 divided among four brakes
                          motor_rotor_mass=9.5,  # NEED TO CHECK
                          motor_rotor_diameter=0.025,  # 25mm
                          motor_max_torque=80.0,
                          motor_max_rpm=7200,
                          motor_reduction_ratio=5.0,
                          motor_v_max=110.0,  # MAX ACC VOLTAGE (NOT MOTOR)
                          motor_v_min=96.0,
                          motor_i_max=425.0,
                          motor_p_max=36800  # 36.8Kw Peak, 23kW cont
                          )
        super().__init__()

