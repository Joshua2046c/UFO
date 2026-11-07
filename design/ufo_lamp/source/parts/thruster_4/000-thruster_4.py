thruster_4_diameter=param("thruster_4_diameter",16.0)
thruster_4_stem_length=param("thruster_4_stem_length",1.5)
r=thruster_4_diameter/2
hemisphere=Sphere(r) & Box(2*r,2*r,r,align=(Align.CENTER,Align.CENTER,Align.MIN))
stem=Cylinder(r,thruster_4_stem_length,align=(Align.CENTER,Align.CENTER,Align.MAX))
thruster_4=hemisphere+stem
assert len(thruster_4.solids())==1
bounds=thruster_4.bounding_box()
assert abs(bounds.size.X-thruster_4_diameter)<1e-5
assert abs(bounds.size.Z-(r+thruster_4_stem_length))<1e-5
thruster_4.color=Color(0.49,0.54,0.59)
publish("thruster_4",thruster_4,"独立推进器 4",material="petg")
