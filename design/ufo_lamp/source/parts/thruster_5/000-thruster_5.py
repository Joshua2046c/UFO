thruster_5_diameter=param("thruster_5_diameter",16.0)
thruster_5_stem_length=param("thruster_5_stem_length",1.5)
r=thruster_5_diameter/2
hemisphere=Sphere(r) & Box(2*r,2*r,r,align=(Align.CENTER,Align.CENTER,Align.MIN))
stem=Cylinder(r,thruster_5_stem_length,align=(Align.CENTER,Align.CENTER,Align.MAX))
thruster_5=hemisphere+stem
assert len(thruster_5.solids())==1
bounds=thruster_5.bounding_box()
assert abs(bounds.size.X-thruster_5_diameter)<1e-5
assert abs(bounds.size.Z-(r+thruster_5_stem_length))<1e-5
thruster_5.color=Color(0.49,0.54,0.59)
publish("thruster_5",thruster_5,"独立推进器 5",material="petg")
