thruster_6_diameter=param("thruster_6_diameter",16.0)
thruster_6_stem_length=param("thruster_6_stem_length",1.5)
r=thruster_6_diameter/2
hemisphere=Sphere(r) & Box(2*r,2*r,r,align=(Align.CENTER,Align.CENTER,Align.MIN))
stem=Cylinder(r,thruster_6_stem_length,align=(Align.CENTER,Align.CENTER,Align.MAX))
thruster_6=hemisphere+stem
assert len(thruster_6.solids())==1
bounds=thruster_6.bounding_box()
assert abs(bounds.size.X-thruster_6_diameter)<1e-5
assert abs(bounds.size.Z-(r+thruster_6_stem_length))<1e-5
thruster_6.color=Color(0.49,0.54,0.59)
publish("thruster_6",thruster_6,"独立推进器 6",material="petg")
