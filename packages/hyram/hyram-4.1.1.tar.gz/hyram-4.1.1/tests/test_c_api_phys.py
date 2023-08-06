"""
Copyright 2015-2022 National Technology & Engineering Solutions of Sandia, LLC (NTESS).
Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains certain rights in this software.

You should have received a copy of the GNU General Public License along with HyRAM+.
If not, see https://www.gnu.org/licenses/.
"""

import os
import unittest

import numpy as np
from scipy import constants as const

from hyram.phys import c_api
from hyram.utilities import misc_utils


"""
NOTE: if running from IDE like pycharm, make sure cwd is hyram/ and not hyram/tests.
"""

VERBOSE = False


class IndoorReleaseTestCase(unittest.TestCase):
    """
    Test accumulation analysis.
    """
    def setUp(self):
        self.output_dir = misc_utils.get_temp_folder()
        c_api.setup(self.output_dir, verbose=VERBOSE)

    def tearDown(self):
        pass

    def test_default(self):
        amb_temp = 288.
        amb_pres = 101325.
        orif_diam = 0.00356
        orif_dis_coeff = 1.0

        rel_height = 0.
        enclos_height = 2.72
        floor_ceil_area = 16.72216
        dist_rel_to_wall = 2.1255
        ceil_vent_xarea = 0.09079
        ceil_vent_height = 2.42
        floor_vent_xarea = 0.00762
        floor_vent_height = 0.044
        rel_angle = 0.
        nozzle_key = 'yuce'

        rel_species = "H2"
        rel_pres = 35000000.
        rel_temp = 287.8
        rel_phase = None

        tank_volume = 0.00363
        vol_flow_rate = 0.

        times = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
                          26, 27, 28, 29, 29.5])
        max_sim_time = 30.
        is_steady = False
        pt_pressures = None
        pt_times = None
        pres_ticks = None

        wrapped = c_api.analyze_accumulation(amb_temp, amb_pres,
                                             rel_species, rel_temp, rel_pres, rel_phase,
                                             tank_volume, orif_diam, rel_height,
                                             enclos_height, floor_ceil_area,
                                             ceil_vent_xarea, ceil_vent_height,
                                             floor_vent_xarea, floor_vent_height,
                                             times,
                                             orif_dis_coeff,
                                             vol_flow_rate, dist_rel_to_wall,
                                             max_sim_time, rel_angle, nozzle_key,
                                             pt_pressures, pt_times, pres_ticks, is_steady=is_steady,
                                             output_dir=self.output_dir, verbose=VERBOSE)

        result_dict = wrapped["data"]
        warning = wrapped["warning"]
        status = result_dict["status"]
        pres_plot_filepath = result_dict['pres_plot_filepath']
        mass_plot_filepath = result_dict['mass_plot_filepath']
        lay_plot_filepath = result_dict['layer_plot_filepath']
        traj_plot_filepath = result_dict['trajectory_plot_filepath']

        self.assertTrue(status)
        self.assertTrue('mass_flow_rates' in result_dict)

        # Plots created
        self.assertTrue(os.path.isfile(pres_plot_filepath))
        self.assertTrue(os.path.isfile(mass_plot_filepath))
        self.assertTrue(os.path.isfile(lay_plot_filepath))
        self.assertTrue(os.path.isfile(traj_plot_filepath))

    def test_saturated_vapor(self):
        amb_temp = 288.15
        amb_pres = 101325.
        orif_diam = 0.00356
        orif_dis_coeff = 1.0

        rel_height = 0.
        enclos_height = 2.72
        floor_ceil_area = 16.72216
        dist_rel_to_wall = 2.1255
        ceil_vent_xarea = 0.09079
        ceil_vent_height = 2.42
        floor_vent_xarea = 0.00762
        floor_vent_height = 0.044
        rel_angle = 0.
        nozzle_key = 'yuce'

        rel_species = "H2"
        rel_pres = 5. * const.atm
        rel_temp = None
        rel_phase = 'gas'

        tank_volume = 0.00363
        vol_flow_rate = 0.

        times = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                          21, 22, 23, 24, 25, 26, 27, 28, 29, 29.5])
        is_steady = False
        max_sim_time = 30.
        pt_pressures = None
        pt_times = None
        pres_ticks = None

        wrapped = c_api.analyze_accumulation(amb_temp, amb_pres,
                                             rel_species, rel_temp, rel_pres, rel_phase,
                                             tank_volume, orif_diam, rel_height,
                                             enclos_height, floor_ceil_area,
                                             ceil_vent_xarea, ceil_vent_height,
                                             floor_vent_xarea, floor_vent_height,
                                             times,
                                             orif_dis_coeff,
                                             vol_flow_rate, dist_rel_to_wall,
                                             max_sim_time, rel_angle, nozzle_key,
                                             pt_pressures, pt_times, pres_ticks, is_steady=is_steady,
                                             output_dir=self.output_dir, verbose=VERBOSE)

        result_dict = wrapped["data"]
        status = result_dict["status"]
        pres_plot_filepath = result_dict['pres_plot_filepath']
        mass_plot_filepath = result_dict['mass_plot_filepath']
        lay_plot_filepath = result_dict['layer_plot_filepath']
        traj_plot_filepath = result_dict['trajectory_plot_filepath']

        self.assertTrue(status)
        self.assertTrue('mass_flow_rates' in result_dict)
        # Plots created
        self.assertTrue(os.path.isfile(pres_plot_filepath))
        self.assertTrue(os.path.isfile(mass_plot_filepath))
        self.assertTrue(os.path.isfile(lay_plot_filepath))
        self.assertTrue(os.path.isfile(traj_plot_filepath))

    def test_saturated_vapor_birch(self):
        amb_temp = 288.15
        amb_pres = 101325.
        orif_diam = 0.00356
        orif_dis_coeff = 1.0

        rel_height = 0.
        enclos_height = 2.72
        floor_ceil_area = 16.72216
        dist_rel_to_wall = 2.1255
        ceil_vent_xarea = 0.09079
        ceil_vent_height = 2.42
        floor_vent_xarea = 0.00762
        floor_vent_height = 0.044
        rel_angle = 0.
        nozzle_key = 'bir'

        rel_species = "H2"
        rel_pres = 1.0e6
        rel_temp = None
        rel_phase = 'gas'

        tank_volume = 0.00363
        vol_flow_rate = 0.

        times = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                          21, 22, 23, 24, 25, 26, 27, 28, 29, 29.5])
        is_steady = False
        max_sim_time = 30.
        pt_pressures = None
        pt_times = None
        pres_ticks = None

        wrapped = c_api.analyze_accumulation(amb_temp, amb_pres,
                                             rel_species, rel_temp, rel_pres, rel_phase,
                                             tank_volume, orif_diam, rel_height,
                                             enclos_height, floor_ceil_area,
                                             ceil_vent_xarea, ceil_vent_height,
                                             floor_vent_xarea, floor_vent_height,
                                             times,
                                             orif_dis_coeff,
                                             vol_flow_rate, dist_rel_to_wall,
                                             max_sim_time, rel_angle, nozzle_key,
                                             pt_pressures, pt_times, pres_ticks, is_steady=is_steady,
                                             output_dir=self.output_dir, verbose=VERBOSE)

        result_dict = wrapped["data"]
        status = result_dict["status"]
        pres_plot_filepath = result_dict['pres_plot_filepath']
        mass_plot_filepath = result_dict['mass_plot_filepath']
        lay_plot_filepath = result_dict['layer_plot_filepath']
        traj_plot_filepath = result_dict['trajectory_plot_filepath']

        self.assertTrue(status)
        self.assertTrue('mass_flow_rates' in result_dict)
        # Plots created
        self.assertTrue(os.path.isfile(pres_plot_filepath))
        self.assertTrue(os.path.isfile(mass_plot_filepath))
        self.assertTrue(os.path.isfile(lay_plot_filepath))
        self.assertTrue(os.path.isfile(traj_plot_filepath))

    def test_steady(self):
        amb_temp = 288.15
        amb_pres = 101325.
        orif_diam = 0.00356
        orif_dis_coeff = 1.0

        rel_height = 0.
        enclos_height = 2.72
        floor_ceil_area = 16.72216
        dist_rel_to_wall = 2.1255
        ceil_vent_xarea = 0.09079
        ceil_vent_height = 2.42
        floor_vent_xarea = 0.00762
        floor_vent_height = 0.044
        rel_angle = 0.
        nozzle_key = 'yuce'

        rel_species = "H2"
        rel_pres = 35000000.
        rel_temp = 287.8
        rel_phase = None

        tank_volume = 0.00363
        vol_flow_rate = 0.

        times = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
                          26, 27, 28, 29, 29.5])
        is_steady = True
        max_sim_time = 30.
        pt_pressures = None
        pt_times = None
        pres_ticks = None

        wrapped = c_api.analyze_accumulation(amb_temp, amb_pres,
                                             rel_species, rel_temp, rel_pres, rel_phase,
                                             tank_volume, orif_diam, rel_height,
                                             enclos_height, floor_ceil_area,
                                             ceil_vent_xarea, ceil_vent_height,
                                             floor_vent_xarea, floor_vent_height,
                                             times,
                                             orif_dis_coeff,
                                             vol_flow_rate, dist_rel_to_wall,
                                             max_sim_time, rel_angle, nozzle_key,
                                             pt_pressures, pt_times, pres_ticks, is_steady=is_steady,
                                             output_dir=self.output_dir, verbose=VERBOSE)

        result_dict = wrapped["data"]
        warning = wrapped["warning"]
        status = result_dict["status"]
        pres_plot_filepath = result_dict['pres_plot_filepath']
        mass_plot_filepath = result_dict['mass_plot_filepath']
        lay_plot_filepath = result_dict['layer_plot_filepath']
        traj_plot_filepath = result_dict['trajectory_plot_filepath']

        self.assertTrue(status)
        # Plots created
        self.assertTrue(os.path.isfile(pres_plot_filepath))
        self.assertTrue(os.path.isfile(mass_plot_filepath))
        self.assertTrue(os.path.isfile(lay_plot_filepath))
        self.assertTrue(os.path.isfile(traj_plot_filepath))


class TestFlameTempPlotGeneration(unittest.TestCase):
    """
    Test plume analysis.
    """
    def setUp(self):
        self.output_dir = misc_utils.get_temp_folder()
        c_api.setup(self.output_dir, verbose=VERBOSE)

    def tearDown(self):
        pass

    def test_default(self):
        amb_temp = 288.15
        amb_pres = 101325.

        rel_species = "H2"
        rel_pres = 35000000.
        rel_temp = 287.8
        rel_phase = None

        rel_angle = 0.
        orif_diam = 0.00356
        discharge_coeff = 1.0
        nozzle_key = "yuce"

        wrapped = c_api.jet_flame_analysis(amb_temp, amb_pres,
                                           rel_species, rel_temp, rel_pres, rel_phase,
                                           orif_diam, discharge_coeff,
                                           rel_angle,
                                           nozzle_key, 0.89,
                                           None, None, None, None, False,
                                           output_dir=self.output_dir, verbose=VERBOSE)

        filepath = wrapped["data"]
        warning = wrapped["warning"]
        self.assertTrue(filepath)
        self.assertFalse(warning)

    def test_unchoked_causes_warning(self):
        amb_temp = 288.15
        amb_pres = 101325.
        rel_species = "H2"
        rel_pres = 151325.
        rel_temp = 287.8
        rel_phase = None
        rel_angle = 0.
        orif_diam = 0.00356
        discharge_coeff = 1.0
        nozzle_key = "yuce"

        wrapped = c_api.jet_flame_analysis(amb_temp, amb_pres,
                                           rel_species, rel_temp, rel_pres, rel_phase,
                                           orif_diam, discharge_coeff,
                                           rel_angle,
                                           nozzle_key, 0.89,
                                           None, None, None, None, False,
                                           output_dir=self.output_dir, verbose=VERBOSE)

        filepath = wrapped["data"]
        warning = wrapped["warning"]
        self.assertTrue(filepath)
        self.assertTrue(warning)


class TestRadHeatAnalysis(unittest.TestCase):
    """
    Test plume analysis.
    """
    def setUp(self):
        self.output_dir = misc_utils.get_temp_folder()
        c_api.setup(self.output_dir, VERBOSE)

    def tearDown(self):
        pass

    def test_default(self):
        amb_temp = 288.15
        amb_pres = 101325.

        rel_species = "H2"
        rel_pres = 35000000.
        rel_temp = 287.8
        rel_phase = None
        rel_angle = 0.

        orif_diam = 0.00356
        discharge_coeff = 1.0
        nozzle_key = "yuce"
        rel_humid = 0.89

        xpos = [1.0e-02, 5.0e-01, 1.0e+00, 2.0e+00, 2.5e+00, 5.0e+00, 1.0e+01, 1.5e+01, 2.5e+01, 4.0e+01]
        ypos = [1., 1., 1., 1., 1., 2., 2., 2., 2., 2.]
        zpos = [0.01, 0.5, 0.5, 1., 1., 1., 0.5, 0.5, 1., 2.]

        contours = [1.577, 4.732, 25.237]

        wrapped = c_api.jet_flame_analysis(amb_temp, amb_pres,
                                           rel_species, rel_temp, rel_pres, rel_phase,
                                           orif_diam, discharge_coeff,
                                           rel_angle,
                                           nozzle_key, rel_humid,
                                           xpos, ypos, zpos,
                                           contours,
                                           analyze_flux=True,
                                           output_dir=self.output_dir, verbose=VERBOSE)

        data = wrapped["data"]
        warning = wrapped["warning"]
        flux = data["flux_data"]
        srad = data['srad']
        visible_length = data['visible_length']
        flux_filepath = data["flux_plot_filepath"]
        temp_filepath = data["temp_plot_filepath"]

        self.assertTrue(flux_filepath is not None)
        self.assertTrue(os.path.isfile(flux_filepath))
        self.assertTrue(os.path.isfile(temp_filepath))
        self.assertFalse(warning)

    def test_sat_liquid(self):
        amb_temp = 288.15
        amb_pres = 101325.

        rel_species = "H2"
        rel_pres = 5. * const.atm
        rel_temp = None
        rel_phase = 'liquid'
        rel_angle = 0.

        orif_diam = 0.00356
        discharge_coeff = 1.0
        nozzle_key = "yuce"
        rel_humid = 0.89

        xpos = [1.0e-02, 5.0e-01, 1.0e+00, 2.0e+00, 2.5e+00, 5.0e+00, 1.0e+01, 1.5e+01, 2.5e+01, 4.0e+01]
        ypos = [1., 1., 1., 1., 1., 2., 2., 2., 2., 2.]
        zpos = [0.01, 0.5, 0.5, 1., 1., 1., 0.5, 0.5, 1., 2.]

        contours = [1.577, 4.732, 25.237]

        wrapped = c_api.jet_flame_analysis(amb_temp, amb_pres,
                                           rel_species, rel_temp, rel_pres, rel_phase,
                                           orif_diam, discharge_coeff,
                                           rel_angle,
                                           nozzle_key, rel_humid,
                                           xpos, ypos, zpos,
                                           contours,
                                           analyze_flux=True,
                                           output_dir=self.output_dir, verbose=VERBOSE)

        data = wrapped["data"]
        flux = data["flux_data"]
        flux_filepath = data["flux_plot_filepath"]
        temp_filepath = data["temp_plot_filepath"]

        self.assertTrue(flux_filepath is not None)
        self.assertTrue(os.path.isfile(flux_filepath))
        self.assertTrue(os.path.isfile(temp_filepath))

    def test_sat_vapor_birch(self):
        amb_temp = 288.15
        amb_pres = 101325.

        rel_species = "H2"
        rel_pres = 1.0e6
        rel_temp = None
        rel_phase = 'gas'
        rel_angle = 0.

        orif_diam = 0.00356
        discharge_coeff = 1.0
        nozzle_key = "bir"
        rel_humid = 0.89

        xpos = [1.0e-02, 5.0e-01, 1.0e+00, 2.0e+00, 2.5e+00, 5.0e+00, 1.0e+01, 1.5e+01, 2.5e+01, 4.0e+01]
        ypos = [1., 1., 1., 1., 1., 2., 2., 2., 2., 2.]
        zpos = [0.01, 0.5, 0.5, 1., 1., 1., 0.5, 0.5, 1., 2.]

        contours = [1.577, 4.732, 25.237]

        wrapped = c_api.jet_flame_analysis(amb_temp, amb_pres,
                                           rel_species, rel_temp, rel_pres, rel_phase,
                                           orif_diam, discharge_coeff,
                                           rel_angle,
                                           nozzle_key, rel_humid,
                                           xpos, ypos, zpos,
                                           contours,
                                           analyze_flux=True,
                                           output_dir=self.output_dir, verbose=VERBOSE)

        data = wrapped["data"]
        flux = data["flux_data"]
        flux_filepath = data["flux_plot_filepath"]
        temp_filepath = data["temp_plot_filepath"]

        self.assertTrue(flux_filepath is not None)
        self.assertTrue(os.path.isfile(flux_filepath))
        self.assertTrue(os.path.isfile(temp_filepath))

    def test_unchoked_flow_yields_warning(self):
        amb_temp = 288.15
        amb_pres = 101325.

        rel_species = "H2"
        rel_pres = 151325.
        rel_temp = 287.8
        rel_phase = None
        rel_angle = 0.

        orif_diam = 0.00356
        discharge_coeff = 1.0
        nozzle_key = "yuce"
        rel_humid = 0.89

        xpos = [1.0e-02, 5.0e-01, 1.0e+00, 2.0e+00, 2.5e+00, 5.0e+00, 1.0e+01, 1.5e+01, 2.5e+01, 4.0e+01]
        ypos = [1., 1., 1., 1., 1., 2., 2., 2., 2., 2.]
        zpos = [0.01, 0.5, 0.5, 1., 1., 1., 0.5, 0.5, 1., 2.]

        contours = [1.577, 4.732, 25.237]

        wrapped = c_api.jet_flame_analysis(amb_temp, amb_pres,
                                           rel_species, rel_temp, rel_pres, rel_phase,
                                           orif_diam, discharge_coeff,
                                           rel_angle,
                                           nozzle_key, rel_humid,
                                           xpos, ypos, zpos,
                                           contours,
                                           analyze_flux=True,
                                           output_dir=self.output_dir, verbose=VERBOSE)

        data = wrapped["data"]
        warning = wrapped["warning"]
        flux = data["flux_data"]
        flux_filepath = data["flux_plot_filepath"]
        temp_filepath = data["temp_plot_filepath"]

        self.assertTrue(flux_filepath is not None)
        self.assertTrue(os.path.isfile(flux_filepath))
        self.assertTrue(os.path.isfile(temp_filepath))
        self.assertTrue(warning)


if __name__ == "__main__":
    unittest.main()
