#!/usr/bin/python3

# Electric Vehicle, Object Oriented Model

# ELEVATE (ELEctric Vehicles and Advanced TEchnologies)
# Simon Howroyd, Loughborough University 2018

VERSION = 2.1

###############################
###    IMPORT LIBRARIES     ###
###############################
from elevate_includes import *
from Cars import Nissan_Leaf
from ElectricityClass import joules_to_kwh

###############################
###     LOCAL VARIABLES     ###
###############################
disp         = Display(VERSION)
graph        = True
feed_forward = False


###############################
###   TEST DATAFILE NAME    ###
###############################
filename     = "DriveCycles/WLTP_kph"
#filename     = "realcycle_kph"


###############################
###    PRINT SETUP DATA     ###
###############################
disp.disp_testfile(filename)
disp.disp_feed_forward(feed_forward)


if __name__ == "__main__":  

    ###############################
    ###     INITIALISATION      ###
    ###############################

    # Note starting epoch time for reference
    time_start = time.time()

    #eng = matlab.engine.start_matlab('-nojvm')
    #print(eng.sqrt(4.0))
    #eng.quit()
    
    datafile = DataIoClass(filename+".tsv")
    timer    = Continuous_dt(datafile.dt, 50)

    # Spawn vehicle(s)
    mycar = CarClass(Nissan_Leaf().data)
    
    disp.disp(datafile.num_lines, " lines in input file")

    disp.disp("SoC at start ",     round(mycar.battery_electricity.get('soc')*100.0,1), '%\n')

    progress = progressbar.ProgressBar().start()

    ###############################
    ###    BEGIN SIMULATION     ###
    ###############################
    while not datafile.finished:# and timer.sim_time<(10*60):


        ###############################
        ###      UPDATE TIMERS      ###
        ###############################
        timer.update()
        datafile.update(timer.sim_time)
        if datafile.new_data:
            progress.update(round(datafile.percent_complete,1))

            #if datafile.finished:
            #    disp.disp("100%", end="\n\n")
            #else:
            #    disp.disp(round(datafile.percent_complete,1),"%",end="\r")

        ###############################
        ###    SET VEHICLE SPEED    ###
        ###############################
        if datafile.new_data:
            mycar.target_speed = mph_to_ms(datafile.line[1])


        ###############################
        ###      UPDATE MODEL       ###
        ###############################
        mycar.update(timer.dt)


        ###############################
        ###      UPDATE SAVE        ###
        ###############################
        datafile.line = [ timer.sim_time ]

        datafile.line = [ ms_to_mph(mycar.target_speed) ]
        datafile.line = [ ms_to_mph(mycar.speed) ]
        datafile.line = [ mycar.powertrain_mode ]
        datafile.line = [ int(mycar._powertrain._motor.is_generating) ]

        datafile.line = [ mycar.battery_electricity.get('soc')*100.0 ]

        datafile.line = [ mycar.aero_force ]

        datafile.line = [ mycar.speed_ctrl_error ]
        datafile.line = [ mycar.speed_ctrl_pid.get('p') ]
        datafile.line = [ mycar.speed_ctrl_pid.get('i') ]
        datafile.line = [ mycar.speed_ctrl_pid.get('d') ]

        datafile.line = [ mycar.motor_ctrl_error ]
        datafile.line = [ mycar.motor_ctrl_pid.get('p') ]
        datafile.line = [ mycar.motor_ctrl_pid.get('i') ]
        datafile.line = [ mycar.motor_ctrl_pid.get('d') ]

        datafile.line = [ mycar.brake_ctrl_error ]
        datafile.line = [ mycar.brake_ctrl_pid.get('p') ]
        datafile.line = [ mycar.brake_ctrl_pid.get('i') ]
        datafile.line = [ mycar.brake_ctrl_pid.get('d') ]

        datafile.line = [ mycar.battery_electricity.get('voltage') ]
        datafile.line = [ mycar.esc_electricity.get('voltage') ]
        datafile.line = [ mycar.motor_electricity.get('voltage') ]

        datafile.line = [ mycar.battery_electricity.get('current') ]
        #datafile.line = [ mycar.esc_electricity.get('current') ]
        datafile.line = [ mycar._powertrain._esc.current ]
        datafile.line = [ mycar.motor_electricity.get('current') ]

        datafile.line = [ mycar.motor_rotation.get('torque') ]
        datafile.line = [ mycar.axle_rotation.get('torque') ]
        datafile.line = [ mycar.wheel_rotation[0].get('torque') ]
        datafile.line = [ mycar.wheel_rotation[2].get('torque') ]
        datafile.line = [ mycar.brake_rotation[0].get('torque') ]
        datafile.line = [ mycar.brake_rotation[2].get('torque') ]

        datafile.line = [ rads_to_rpm(mycar.motor_rotation.get('speed')) ]
        datafile.line = [ rads_to_rpm(mycar.axle_rotation.get('speed')) ]
        datafile.line = [ rads_to_rpm(mycar.wheel_rotation[0].get('speed')) ]
        datafile.line = [ rads_to_rpm(mycar.wheel_rotation[2].get('speed')) ]
        datafile.line = [ rads_to_rpm(mycar.brake_rotation[0].get('speed')) ]
        datafile.line = [ rads_to_rpm(mycar.brake_rotation[2].get('speed')) ]

    progress.finish()
    disp.disp("", end='\r\n')


    odometer = mycar.odometer/1000.0
    odometerW= mycar.odometer_wheels/1000.0
    soc      = mycar.battery_electricity.get('soc')*100.0
    kwh_out  = joules_to_kwh(mycar.battery_electricity.get('total_energy_out'))
    kwh_in   = joules_to_kwh(mycar.battery_electricity.get('total_energy_in'))

    disp.disp("Odometer ",         round(odometer,1), "km")
    disp.disp("Odometer (wheels)", round(odometerW,1), "km")
    disp.disp("Soc at end ",       round(soc,1), "%")
    disp.disp("Total energy out ", round(kwh_out, 1), "kWh")
    disp.disp("Total energy in ",  round(kwh_in, 1),  "kWh")
    disp.disp("Efficiency ",       round(100.0*kwh_out/odometer,1), "kWh/100km")

    disp.disp("\n\nFinished!\n\n")


    ###############################
    ###     COMPILE GRAPHS      ###
    ###############################
    if graph:

        # Get data from saved datafile
        data_out = np.genfromtxt(filename+"_out.csv", delimiter=',', skip_header=1, skip_footer=1,
                    names = [   'x',
                                'v_set', 'v_true',  'mode', 'regen',
                                'dragAero',
                                'speedE', 'speedP', 'speedI', 'speedD',
                                'motorE', 'motorP', 'motorI', 'motorD',
                                'brakeE', 'brakeP', 'brakeI', 'brakeD',
                                'batt_v', 'esc_v',  'motor_v',
                                'batt_i', 'esc_i',  'motor_i',
                                'tq_m',   'tq_ax',  'tq_w0',   'tq_w2', 'tq_b0', 'tq_b2',
                                'w_m',    'w_ax',   'w_w0',    'w_w2',  'w_b0',  'w_b2'
                            ])

        timestamp = data_out['x']
        timestamp /= 60 # Convert seconds to minutes

        xlim = False
        #xlim = [1.9, 2.0]
        

        ###############################
        ###        FIGURE 1         ###
        ###############################
        fig = plt.figure()

        ###############################
        ###    FIG 1, SUBPLOT 1     ###
        ###############################
        ax1 = fig.add_subplot(411)
        ax1.plot(timestamp, data_out['v_set'],  label='v_set')
        ax1.plot(timestamp, data_out['v_true'], label='v_true')
        ax1.plot(timestamp, data_out['dragAero']/10, label='dragAero')
        ax1.set_ylabel('Mph, N/10')
        #ax1.set_ylim([0, 80])
        if xlim is not False:
            ax1.set_xlim(xlim)
            ax1.relim()
            ax1.autoscale_view(scalex=False, scaley=True)
        ax1.grid(True)
        leg1 = ax1.legend(loc='upper right', shadow=True)

        ###############################
        ###    FIG 1, SUBPLOT 2     ###
        ###############################
        ax2 = fig.add_subplot(412)
        ax2.plot(timestamp, data_out['speedE'], label='speedE')
        ax2.plot(timestamp, data_out['speedP'], label='speedP', linestyle=':')
        ax2.plot(timestamp, data_out['speedI'], label='speedI', linestyle=':')
        ax2.plot(timestamp, data_out['speedD'], label='speedD', linestyle=':')
        ax2.set_ylabel('Speed Ctrl \n 0-255')
        #ax2.set_ylim([-260, 260])
        if xlim is not False:
            ax2.set_xlim(xlim)
            ax2.relim()
            ax2.autoscale_view(scalex=False, scaley=True)
        ax2.grid(True)
        leg2 = ax2.legend(loc='upper right', shadow=True)

        ###############################
        ###    FIG 1, SUBPLOT 3     ###
        ###############################
        ax3 = fig.add_subplot(413)
        ax3.plot(timestamp, data_out['motorE'], label='motorE')
        ax3.plot(timestamp, data_out['motorP'], label='motorP', linestyle=':')
        ax3.plot(timestamp, data_out['motorI'], label='motorI', linestyle=':')
        ax3.plot(timestamp, data_out['motorD'], label='motorD', linestyle=':')
        ax3.set_ylabel('Motor Ctrl \n 0-255')
        #ax3.set_ylim([-260, 260]
        if xlim is not False:
            ax3.set_xlim(xlim)
            ax3.relim()
            ax3.autoscale_view(scalex=False, scaley=True)
        ax3.grid(True)
        leg3 = ax3.legend(loc='upper right', shadow=True)

        ###############################
        ###    FIG 1, SUBPLOT 4     ###
        ###############################
        ax4 = fig.add_subplot(414)
        ax4.plot(timestamp, data_out['brakeE'], label='brakeE')
        ax4.plot(timestamp, data_out['brakeP'], label='brakeP', linestyle=':')
        ax4.plot(timestamp, data_out['brakeI'], label='brakeI', linestyle=':')
        ax4.plot(timestamp, data_out['brakeD'], label='brakeD', linestyle=':')
        ax4.set_ylabel('Brake Ctrl \n 0-255')
        #ax4.set_ylim([-260, 260])
        if xlim is not False:
            ax4.set_xlim(xlim)
            ax4.relim()
            ax4.autoscale_view(scalex=False, scaley=True)
        leg4 = ax4.legend(loc='upper right', shadow=True)
        ax4.grid(True)
        # Fig 1 x-Axis Label
        ax4.set_xlabel('Time /mins')


        ###############################
        ###        FIGURE 2         ###
        ###############################
        fig2 = plt.figure()

        ###############################
        ###    FIG 2, SUBPLOT 1     ###
        ###############################
        ax1 = fig2.add_subplot(411)
        #ax1.plot(timestamp, data_out['batt_v'],  label='batt_v')
        #ax1.plot(timestamp, data_out['esc_v'],   label='esc_v')
        #ax1.plot(timestamp, data_out['motor_v'], label='motor_v')
        #ax1.plot(timestamp, data_out['batt_i'],    label='batt_i')
        #ax1.plot(timestamp, data_out['esc_i'],     label='esc_i')
        #ax1.plot(timestamp, data_out['motor_i'],   label='motor_i')
        #ax1.plot(timestamp, data_out['motor_v']*data_out['motor_i']/1000.0,   label='motor_p', linestyle=':')
        ax1.plot(timestamp, data_out['speedE'], label='speedE')
        ax1.plot(timestamp, data_out['motorE'], label='motorE', linestyle=':')
        ax1.plot(timestamp, data_out['brakeE'], label='brakeE', linestyle=':')
        ax1.set_ylabel('Speed Ctrl \n 0-255')
        #ax1.set_ylabel('Voltage/4V, Current/I, Power/kW')
        #ax1.set_ylim([300, 400])
        if xlim is not False:
            ax1.set_xlim(xlim)
            ax1.relim()
            ax1.autoscale_view(scalex=False, scaley=True)
        ax1.grid(True)
        leg1 = ax1.legend(loc='upper right', shadow=True)

         ###############################
         ###   CALCULATE WIRE GAUGE  ###
         ###############################
        print(data_out['batt_i'])


        ###############################
        ###    FIG 2, SUBPLOT 2     ###
        ###############################
        ax2 = fig2.add_subplot(412)
        #ax2.plot(timestamp, data_out['mode'],  label='mode')
        #ax2.plot(timestamp, data_out['regen'], label='regen', linestyle=':')
        #ax2.set_ylabel('Mode')
        #ax2.set_ylim([0, 5])
        ax2.plot(timestamp, data_out['batt_i'],  label='batt_i')
        ax2.plot(timestamp, data_out['esc_i'],   label='esc_i')
        ax2.plot(timestamp, data_out['motor_i'], label='motor_i')
        ax2.plot([0,max(timestamp)], [267,267],  linestyle='--', color='k')
        ax2.set_ylabel('Current')
        ax2.set_ylim([0, 300])
        if xlim is not False:
            ax2.set_xlim(xlim)
            ax2.relim()
            ax2.autoscale_view(scalex=False, scaley=True)
        ax2.grid(True)
        leg2 = ax2.legend(loc='upper right', shadow=True)

        ###############################
        ###    FIG 2, SUBPLOT 3     ###
        ###############################
        ax3 = fig2.add_subplot(413)
        ax3.plot(timestamp, data_out['tq_m'],    label='tq_m' , linestyle='-')
        ax3.plot(timestamp, data_out['tq_ax'],   label='tq_ax', linestyle=':')
        ax3.plot(timestamp, data_out['tq_w0'],   label='tq_w0', linestyle='-')
        ax3.plot(timestamp, data_out['tq_b0'],   label='tq_b0', linestyle=':')
        ax3.set_ylabel('Torque')
        #ax3.set_ylim([0, 300])
        if xlim is not False:
            ax3.set_xlim(xlim)
            ax3.relim()
            ax3.autoscale_view(scalex=False, scaley=True)
        ax3.grid(True)
        leg3 = ax3.legend(loc='upper right', shadow=True)

        ###############################
        ###    FIG 2, SUBPLOT 4     ###
        ###############################
        ax4 = fig2.add_subplot(414)
        ax4.plot(timestamp, data_out['w_m'],      label='w_m' , linestyle='-')
        ax4.plot(timestamp, data_out['w_ax'],     label='w_ax', linestyle=':')
        ax4.plot(timestamp, data_out['w_w0'],     label='w_w0', linestyle='-')
        ax4.plot(timestamp, data_out['w_b0'],     label='w_b0', linestyle=':')
        ax4.set_ylabel('RPM')
        #ax4.set_ylim([-260, 260])
        if xlim is not False:
            ax4.set_xlim(xlim)
            ax4.relim()
            ax4.autoscale_view(scalex=False, scaley=True)
        leg4 = ax4.legend(loc='upper right', shadow=True)
        ax4.grid(True)
        # Fig 1 x-Axis Label
        ax4.set_xlabel('Time /mins')


    ###############################
    ###       SHOW COSTS        ###
    ###############################
    #disp.disp_cost("Speed Cost:", round(leaf1._powertrain_model_array[0]._speed_control.cost, 1))
    #disp.disp_cost("Motor Cost:", round(leaf1._powertrain_model_array[0]._speed_control._motor_controller.cost, 1))
    #disp.disp_cost("Brake Cost:", round(leaf1._powertrain_model_array[0]._speed_control._brake_controller.cost, 1))    

    ###############################
    ###       SHOW TIME         ###
    ###############################
    disp.disp_time(("\n", round((time.time()-time_start),1), "seconds to run"))

    ###############################
    ###       SHOW GRAPH        ###
    ###############################
    if graph:
        plt.show()

###############################
###############################
######       END         ######
###############################
###############################
