from math import sin, cos, pi
body_diameter=param("body_diameter",150.0)
body_height=param("body_height",32.0)
body_wall=param("body_wall",2.4)
body_hub_diameter=param("body_hub_diameter",80.0)
body_rim_height=param("body_rim_height",13.0)
body_edge_wall=param("body_edge_wall",4.8)
body_edge_scale=param("body_edge_scale",0.5)
upper_wire_exit_width=param("upper_wire_exit_width",6.0)
upper_wire_exit_height=param("upper_wire_exit_height",4.0)
upper_wire_exit_radius=param("upper_wire_exit_radius",73.8)
body_split_height=param("body_split_height",16.0)
body_lamp_clearance=param("body_lamp_clearance",0.5)
body_lamp_headroom=param("body_lamp_headroom",1.0)
body_seat_z=param("body_seat_z",7.0)
cockpit_locator_diameter=param("cockpit_locator_diameter",68.4)
body_cockpit_clearance=param("body_cockpit_clearance",0.35)
body_locator_height=param("body_locator_height",5.0)
body_locator_wall=param("body_locator_wall",2.4)
body_locator_leadin=param("body_locator_leadin",0.5)
body_porthole_diameter=param("body_porthole_diameter",11.0)
body_porthole_depth=param("body_porthole_depth",0.65)
body_porthole_radius=param("body_porthole_radius",56.0)
body_porthole_count=param("body_porthole_count",8)
magnet_spacing=param("magnet_spacing",92.0)
magnet_socket_diameter=param("magnet_socket_diameter",7.1)
magnet_socket_depth=param("magnet_socket_depth",2.2)
body_socket_pad_width=param("body_socket_pad_width",14.0)
body_socket_pad_height=param("body_socket_pad_height",10.0)
# Envelope from user's light puck specification.
LAMP_D=60.0
LAMP_T=8.0
r=body_diameter/2
hub=body_hub_diameter/2
s=body_split_height
h=body_height
z=body_rim_height
bore=cockpit_locator_diameter/2+body_cockpit_clearance
pocket=LAMP_D/2+body_lamp_clearance
root=cockpit_locator_diameter/2
locator_inner=root-body_locator_wall
# Mirror the lower edge, scaling the straight band and bevel about the waist.
edge_band=(s-(z-1))*body_edge_scale
edge_top=s+edge_band
bevel_top=s+(s-(z-3))*body_edge_scale
assert edge_band>0
pts=[(r,s),(r,edge_top),(r-1,bevel_top),(hub+4,h-2),(hub,h),(root,h),(root,h+body_locator_height-body_locator_leadin),(root-body_locator_leadin,h+body_locator_height),(locator_inner,h+body_locator_height),(locator_inner,s),(hub-3,s),(hub-3,h-body_wall-2),(hub+3,h-body_wall-2),(r-body_edge_wall,edge_top),(r-body_edge_wall,s)]
with BuildPart() as upper_build:
    with BuildSketch(Plane.XZ):
        Polygon(*[(x,y-s) for x,y in pts],align=None)
    revolve(axis=Axis.Z)
body=upper_build.part
# Inner collar now reaches the same underside plane as the outer rim.
flush_annulus=Cylinder(hub-3,h-body_wall-s,align=(Align.CENTER,Align.CENTER,Align.MIN))-Cylinder(locator_inner,h-body_wall-s,align=(Align.CENTER,Align.CENTER,Align.MIN))
assert getattr(flush_annulus-body,"volume",0.0)<1e-5
assert abs(body.bounding_box().min.Z)<1e-6
print("Inner ledge extension:",h-body_wall-s,"mm; underside datum:",s,"mm")
# Upward locating ring is integral with the upper shell; cover has a flat bottom.
for x in [-magnet_spacing/2,magnet_spacing/2]:
    inner_end=hub-3-body_wall/2
    outer_end=abs(x)+body_socket_pad_width/2
    centre=(inner_end+abs(x))/2*(1 if x>0 else -1)
    bridge=Pos(centre,0,body_socket_pad_height/2)*Box(abs(x)-inner_end,body_socket_pad_width,body_socket_pad_height)
    round_seat=Pos(x,0,body_socket_pad_height/2)*Cylinder(body_socket_pad_width/2,body_socket_pad_height)
    body=body+bridge+round_seat
    body=body-Pos(x,0,magnet_socket_depth/2)*Cylinder(magnet_socket_diameter/2,magnet_socket_depth)
# Upper half of rectangular cable exit, centered on the waist seam.
pr=body_porthole_radius
surface=bevel_top+(r-1-pr)*((h-2)-bevel_top)/((r-1)-(hub+4))
for i in range(int(body_porthole_count)):
    a=2*pi*i/int(body_porthole_count)
    body=body-Pos(pr*cos(a),pr*sin(a),surface+body_porthole_diameter/2-body_porthole_depth-s)*Sphere(body_porthole_diameter/2)
assert len(body.solids())==1
# Kernel section verifies the widened radial edge wall, clear of connector pads.
edge_section=section(body,section_by=Plane.XY.offset(edge_band/2))
# Isolate the outer annulus in the section, so central hub area does not enter this check.
outer_annulus=Cylinder(r,edge_band,align=(Align.CENTER,Align.CENTER,Align.MIN))-Cylinder(r-body_edge_wall,edge_band,align=(Align.CENTER,Align.CENTER,Align.MIN))
assert getattr(outer_annulus-body,"volume",0.0)<1e-5
exit_tool=Pos(0,-upper_wire_exit_radius,0)*Box(upper_wire_exit_width,4*body_wall,upper_wire_exit_height)
body=body-exit_tool
exit_check=Pos(0,-upper_wire_exit_radius,0)*Rot(90,0,0)*Cylinder((min(upper_wire_exit_width,upper_wire_exit_height)-0.4)/2,4*body_wall)
assert getattr(body & exit_check,"volume",0.0)<1e-5
assert len(body.solids())==1
print("Upper rim straight band height",edge_band,"radial wall",body_edge_wall,"bevel height",bevel_top-edge_top)
lamp_envelope=Pos(0,0,body_seat_z-s)*Cylinder(LAMP_D/2,LAMP_T,align=(Align.CENTER,Align.CENTER,Align.MIN))
assert getattr(body & lamp_envelope,"volume",0.0) < 1e-5
assert abs(body.bounding_box().max.Z-(h-s+body_locator_height))<1e-5
for x in [-magnet_spacing/2,magnet_spacing/2]:
    magnet_check=Pos(x,0,magnet_socket_depth/2)*Cylinder(magnet_socket_diameter/2,magnet_socket_depth)
    assert getattr(body & magnet_check,"volume",0.0)<1e-5
    floor_check=Pos(x,0,magnet_socket_depth+body_wall/2)*Cylinder(magnet_socket_diameter/2,body_wall)
    assert getattr(floor_check-body,"volume",0.0)<1e-5
body.color=Color(0.57,0.62,0.67)
publish("body",body,"飞碟上壳",material="petg")
