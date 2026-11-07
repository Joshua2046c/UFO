thruster_2_diameter=param("thruster_2_diameter",16.0)
thruster_2_stem_length=param("thruster_2_stem_length",1.5)
r=thruster_2_diameter/2
hemisphere=Sphere(r) & Box(2*r,2*r,r,align=(Align.CENTER,Align.CENTER,Align.MIN))
stem=Cylinder(r,thruster_2_stem_length,align=(Align.CENTER,Align.CENTER,Align.MAX))
thruster_2=hemisphere+stem
assert len(thruster_2.solids())==1
bounds=thruster_2.bounding_box()
assert abs(bounds.size.X-thruster_2_diameter)<1e-5
assert abs(bounds.size.Z-(r+thruster_2_stem_length))<1e-5
thruster_2.color=Color(0.49,0.54,0.59)
publish("thruster_2",thruster_2,"独立推进器 2",material="petg")
