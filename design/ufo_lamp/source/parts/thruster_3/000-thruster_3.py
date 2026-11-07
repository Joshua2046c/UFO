thruster_3_diameter=param("thruster_3_diameter",16.0)
thruster_3_stem_length=param("thruster_3_stem_length",1.5)
r=thruster_3_diameter/2
hemisphere=Sphere(r) & Box(2*r,2*r,r,align=(Align.CENTER,Align.CENTER,Align.MIN))
stem=Cylinder(r,thruster_3_stem_length,align=(Align.CENTER,Align.CENTER,Align.MAX))
thruster_3=hemisphere+stem
assert len(thruster_3.solids())==1
bounds=thruster_3.bounding_box()
assert abs(bounds.size.X-thruster_3_diameter)<1e-5
assert abs(bounds.size.Z-(r+thruster_3_stem_length))<1e-5
thruster_3.color=Color(0.49,0.54,0.59)
publish("thruster_3",thruster_3,"独立推进器 3",material="petg")
