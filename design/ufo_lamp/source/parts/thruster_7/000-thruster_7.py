thruster_7_diameter=param("thruster_7_diameter",16.0)
thruster_7_stem_length=param("thruster_7_stem_length",1.5)
r=thruster_7_diameter/2
hemisphere=Sphere(r) & Box(2*r,2*r,r,align=(Align.CENTER,Align.CENTER,Align.MIN))
stem=Cylinder(r,thruster_7_stem_length,align=(Align.CENTER,Align.CENTER,Align.MAX))
thruster_7=hemisphere+stem
assert len(thruster_7.solids())==1
bounds=thruster_7.bounding_box()
assert abs(bounds.size.X-thruster_7_diameter)<1e-5
assert abs(bounds.size.Z-(r+thruster_7_stem_length))<1e-5
thruster_7.color=Color(0.49,0.54,0.59)
publish("thruster_7",thruster_7,"独立推进器 7",material="petg")
