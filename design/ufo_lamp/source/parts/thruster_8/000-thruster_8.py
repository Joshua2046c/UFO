thruster_8_diameter=param("thruster_8_diameter",16.0)
thruster_8_stem_length=param("thruster_8_stem_length",1.5)
r=thruster_8_diameter/2
hemisphere=Sphere(r) & Box(2*r,2*r,r,align=(Align.CENTER,Align.CENTER,Align.MIN))
stem=Cylinder(r,thruster_8_stem_length,align=(Align.CENTER,Align.CENTER,Align.MAX))
thruster_8=hemisphere+stem
assert len(thruster_8.solids())==1
bounds=thruster_8.bounding_box()
assert abs(bounds.size.X-thruster_8_diameter)<1e-5
assert abs(bounds.size.Z-(r+thruster_8_stem_length))<1e-5
thruster_8.color=Color(0.49,0.54,0.59)
publish("thruster_8",thruster_8,"独立推进器 8",material="petg")
