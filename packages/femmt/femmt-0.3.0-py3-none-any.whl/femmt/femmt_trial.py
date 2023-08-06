import femmt as fmt
import numpy as np


geo = fmt.MagneticComponent(component_type="inductor")
geo.visualize_before = False

# Update Geometry
geo.core.update(window_h=0.03, window_w=0.011)

# geo.air_gaps.update(method="percent", n_air_gaps=4, air_gap_h=[0.0005, 0.0005, 0.0005, 0.0005],
#                     position_tag=[0, 0, 0, 0], air_gap_position=[20, 40, 60, 80])
geo.air_gaps.update(method="center", n_air_gaps=1, air_gap_h=[0.0005], position_tag=[0])

geo.update_conductors(n_turns=[[14]], conductor_type=["litz"], conductor_radii=[0.0015],
                      litz_para_type=['implicit_litz_radius'],
                      ff=[0.6], strands_numbers=[600], strand_radii=[35.5e-6],
                      winding=["primary"], scheme=["square"],
                      core_cond_isolation=[0.0005], cond_cond_isolation=[0.0001])

#geo.single_simulation(freq=100000, current=[1])
#fs = np.linspace(0, 250000, 6)
#cs = [10, 2, 1, 0.5, 0.2, 0.1]
#winding1_phi_rad_list=[0, 0, 0, 0, 0, 0]
#geo.excitation_sweep_old(fs, cs, winding1_phi_rad_list)
#geo.femm_reference(freq=100000, current=[1], sigma_cu=58, sign=[1], non_visualize=0)
geo.high_level_geo_gen(frequency=50, skin_mesh_factor=1)
geo.mesh.generate_hybrid_mesh(do_meshing=False)

# # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# # Colors
# for i in range(0, len(self.plane_surface_core)):
#     gmsh.model.setColor([(2, self.plane_surface_core[i])], 50, 50, 50)
# gmsh.model.setColor([(2, self.plane_surface_air[0])], 255, 255, 255)
# for num in range(0, self.component.n_windings):
#     for i in range(0, len(self.plane_surface_cond[num])):
#         gmsh.model.setColor([(2, self.plane_surface_cond[num][i])], 200 * num, 200 * (1 - num), 0)
#
# if '-nopopup' not in sys.argv:
#     gmsh.fltk.initialize()
#
# gmsh.write(os.path.join(self.component.mesh_folder_path, "geometry_preview.jpg"))
#
# if self.component.visualize_before:
#
#     # Output .msh file
#     gmsh.option.setNumber("Mesh.SaveAll", 1)
#
#     gmsh.write(self.component.hybrid_color_mesh_file)
#     if do_meshing:
#         gmsh.model.mesh.generate(2)
#         gmsh.fltk.run()
# else:
#     if do_meshing:
#         gmsh.model.mesh.generate(2)
#         gmsh.write(self.component.hybrid_mesh_file)
#
# gmsh.finalize()