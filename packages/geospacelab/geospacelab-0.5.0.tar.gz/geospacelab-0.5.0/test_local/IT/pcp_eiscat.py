import datetime
import numpy as np

import geospacelab.express.eiscat_dashboard as eiscat


def test_esr_32m():
    dt_fr = datetime.datetime.strptime('20150215' + '1700', '%Y%m%d%H%M')
    dt_to = datetime.datetime.strptime('20150215' + '2200', '%Y%m%d%H%M')

    site = 'ESR'
    antenna = '32m'
    modulation = '32'
    # load_mode = 'dialog'
    load_mode = 'AUTO'
    data_file_type = 'eiscat-hdf5'

    dashboard = eiscat.EISCATDashboard(
        dt_fr, dt_to,
        site=site, antenna=antenna, modulation=modulation,
        data_file_type=data_file_type, load_mode=load_mode)

    # select beams before assign the variables
    # dashboard.dataset.select_beams(field_aligned=False)
    dashboard.check_beams()
    n_e = dashboard.assign_variable('n_e')
    n_e.visual.axis[1].data = '@d.AACGM_LAT.value'
    n_e.visual.axis[1].label = 'MLAT'
    n_e.visual.axis[1].unit = 'deg'
    n_e.visual.axis[1].lim = [69.5, 75]
    T_i = dashboard.assign_variable('T_i')
    T_i.visual.axis[1].data = '@d.AACGM_LAT.value'
    T_i.visual.axis[1].label = 'MLAT'
    T_i.visual.axis[1].unit = 'deg'
    T_i.visual.axis[1].lim = [69.5, 75]
    T_e = dashboard.assign_variable('T_e')
    T_e.visual.axis[1].data = '@d.AACGM_LAT.value'
    T_e.visual.axis[1].label = 'MLAT'
    T_e.visual.axis[1].unit = 'deg'
    T_e.visual.axis[1].lim = [69.5, 75]
    v_i = dashboard.assign_variable('v_i_los')
    v_i.visual.axis[1].data = '@d.AACGM_LAT.value'
    v_i.visual.axis[1].label = 'MLAT'
    v_i.visual.axis[1].unit = 'deg'
    v_i.visual.axis[1].lim = [69.5, 75]

    az = dashboard.assign_variable('AZ')
    el = dashboard.assign_variable('EL')

    layout = [[n_e], [T_e], [T_i], [v_i], [az, el]]
    dashboard.set_layout(panel_layouts=layout, row_height_scales=[5, 5, 5, 5, 3])
    dashboard.draw()
    dashboard.add_title()
    dashboard.add_panel_labels()
    # dashboard.show()
    dashboard.save_figure("ESR_32m")
    return dashboard


def test_tro_uhf():
    dt_fr = datetime.datetime.strptime('20150215' + '1700', '%Y%m%d%H%M')
    dt_to = datetime.datetime.strptime('20150215' + '2300', '%Y%m%d%H%M')

    site = 'UHF'
    antenna = 'UHF'
    modulation = ''
    load_mode = 'AUTO'
    data_file_type = 'eiscat-hdf5'

    dashboard = eiscat.EISCATDashboard(
        dt_fr, dt_to,
        site=site, antenna=antenna, modulation=modulation,
        data_file_type=data_file_type, load_mode=load_mode)
    dashboard.check_beams()
    n_e = dashboard.assign_variable('n_e')
    T_i = dashboard.assign_variable('T_i')
    T_e = dashboard.assign_variable('T_e')
    v_i = dashboard.assign_variable('v_i_los')

    az = dashboard.assign_variable('AZ')
    el = dashboard.assign_variable('EL')

    layout = [[n_e], [T_e], [T_i], [v_i], [az, el]]
    dashboard.set_layout(panel_layouts=layout, row_height_scales=[5, 5, 5, 5, 3])
    dashboard.draw()
    dashboard.add_title()
    dashboard.add_panel_labels()
    # dashboard.show()
    # dashboard.save_figure("TRO_UHF")
    return dashboard


def test_tro_vhf():
    dt_fr = datetime.datetime.strptime('20150215' + '1700', '%Y%m%d%H%M')
    dt_to = datetime.datetime.strptime('20150215' + '2300', '%Y%m%d%H%M')

    site = 'VHF'
    antenna = 'VHF'
    modulation = ''
    load_mode = 'AUTO'
    data_file_type = 'eiscat-hdf5'

    dashboard = eiscat.EISCATDashboard(
        dt_fr, dt_to,
        site=site, antenna=antenna, modulation=modulation,
        data_file_type=data_file_type, load_mode=load_mode)

    n_e = dashboard.assign_variable('n_e')
    T_i = dashboard.assign_variable('T_i')
    T_e = dashboard.assign_variable('T_e')
    v_i = dashboard.assign_variable('v_i_los')

    az = dashboard.assign_variable('AZ')
    el = dashboard.assign_variable('EL')

    layout = [[n_e], [T_e], [T_i], [v_i], [az, el]]
    dashboard.set_layout(panel_layouts=layout, row_height_scales=[5, 5, 5, 5, 3])
    dashboard.draw()
    dashboard.add_title()
    dashboard.add_panel_labels()
    # dashboard.show()
    dashboard.save_figure("TRO_vHF")
    return dashboard


if __name__ == "__main__":
    # test_esr_32m()
    test_tro_uhf()
    # test_tro_vhf()