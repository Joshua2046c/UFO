thruster_1_diameter=param("thruster_1_diameter",16.0)
thruster_1_stem_length=param("thruster_1_stem_length",1.5)
r=thruster_1_diameter/2
hemisphere=Sphere(r) & Box(2*r,2*r,r,align=(Align.CENTER,Align.CENTER,Align.MIN))
stem=Cylinder(r,thruster_1_stem_length,align=(Align.CENTER,Align.CENTER,Align.MAX))
thruster_1=hemisphere+stem
assert len(thruster_1.solids())==1
bounds=thruster_1.bounding_box()
assert abs(bounds.size.X-thruster_1_diameter)<1e-5
assert abs(bounds.size.Z-(r+thruster_1_stem_length))<1e-5
thruster_1.color=Color(0.49,0.54,0.59)
publish("thruster_1",thruster_1,"独立推进器 1",material="petg")
