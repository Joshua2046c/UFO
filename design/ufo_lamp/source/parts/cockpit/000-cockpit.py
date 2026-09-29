
cockpit_diameter=param("cockpit_diameter",80.0)
cockpit_height=param("cockpit_height",34.0)
cockpit_wall=param("cockpit_wall",2.4)
cockpit_flange_thickness=param("cockpit_flange_thickness",2.0)
cockpit_neck_inner_diameter=param("cockpit_neck_inner_diameter",63.0)
cockpit_leadin=param("cockpit_leadin",0.5)
cockpit_locator_diameter=param("cockpit_locator_diameter",68.4)
cockpit_neck_length=param("cockpit_neck_length",5.0)
r=cockpit_diameter/2
h=cockpit_height
R=(r*r+h*h)/(2*h)
cz=h-R
root=cockpit_locator_diameter/2
inner=cockpit_neck_inner_diameter/2
neck_len=cockpit_neck_length
clip=Pos(0,0,h/2)*Box(3*r,3*r,h)
dome=(Pos(0,0,cz)*Sphere(R)) & clip
dome=dome-(Pos(0,0,cz)*Sphere(R-cockpit_wall))
flange=Cylinder(r,cockpit_flange_thickness,align=(Align.CENTER,Align.CENTER,Align.MIN))-Cylinder(inner,cockpit_flange_thickness,align=(Align.CENTER,Align.CENTER,Align.MIN))
# Smooth drop-in skirt with a short lead-in chamfer, open through the centre.
neck=Pos(0,0,-neck_len+cockpit_leadin)*Cylinder(root,neck_len-cockpit_leadin+cockpit_flange_thickness,align=(Align.CENTER,Align.CENTER,Align.MIN))
neck=neck+Pos(0,0,-neck_len)*Cone(root-cockpit_leadin,root,cockpit_leadin,align=(Align.CENTER,Align.CENTER,Align.MIN))
neck=neck-Pos(0,0,-neck_len-cockpit_wall)*Cylinder(inner,neck_len+cockpit_flange_thickness+2*cockpit_wall,align=(Align.CENTER,Align.CENTER,Align.MIN))
cockpit=dome+flange+neck
assert len(cockpit.solids())==1
cockpit.color=Color(1.0,0.68,0.06)
publish("cockpit",cockpit,"落座圆顶座舱",material="petg")
