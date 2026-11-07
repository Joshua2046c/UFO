cockpit_diameter=param("cockpit_diameter",80.0)
cockpit_height=param("cockpit_height",34.0)
cockpit_wall=param("cockpit_wall",2.4)
cockpit_flange_thickness=param("cockpit_flange_thickness",2.0)
cockpit_locator_diameter=param("cockpit_locator_diameter",68.4)
cockpit_socket_clearance=param("cockpit_socket_clearance",0.35)
cockpit_socket_depth=param("cockpit_socket_depth",5.5)
r=cockpit_diameter/2
h=cockpit_height
R=(r*r+h*h)/(2*h)
cz=h-R
socket=cockpit_locator_diameter/2+cockpit_socket_clearance
clip=Pos(0,0,h/2)*Box(3*r,3*r,h)
dome=(Pos(0,0,cz)*Sphere(R)) & clip
dome=dome-(Pos(0,0,cz)*Sphere(R-cockpit_wall))
flange=Cylinder(r,cockpit_flange_thickness,align=(Align.CENTER,Align.CENTER,Align.MIN))-Cylinder(socket,cockpit_flange_thickness,align=(Align.CENTER,Align.CENTER,Align.MIN))
# Internal guide wall only: nothing projects below the flat bearing face z=0.
guide=Cylinder(socket+cockpit_wall,cockpit_socket_depth,align=(Align.CENTER,Align.CENTER,Align.MIN))-Cylinder(socket,cockpit_socket_depth,align=(Align.CENTER,Align.CENTER,Align.MIN))
cockpit=dome+flange+guide
assert len(cockpit.solids())==1
assert abs(cockpit.bounding_box().min.Z)<1e-6
assert abs(cockpit.bounding_box().max.Z-h)<1e-6
socket_check=Cylinder(socket,cockpit_socket_depth,align=(Align.CENTER,Align.CENTER,Align.MIN))
assert getattr(cockpit & socket_check,"volume",0.0)<1e-5
cockpit.color=Color(1.0,0.68,0.06)
publish("cockpit",cockpit,"平底落座圆顶",material="petg")
