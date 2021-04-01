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
