from math import sin, cos, pi
body_diameter=param("body_diameter",150.0)
body_height=param("body_height",32.0)
body_wall=param("body_wall",2.4)
body_hub_diameter=param("body_hub_diameter",80.0)
body_rim_height=param("body_rim_height",13.0)
body_split_height=param("body_split_height",16.0)
body_lamp_clearance=param("body_lamp_clearance",0.5)
body_lamp_headroom=param("body_lamp_headroom",1.0)
body_seat_z=param("body_seat_z",13.0)
cockpit_locator_diameter=param("cockpit_locator_diameter",68.4)
body_cockpit_clearance=param("body_cockpit_clearance",0.35)
body_porthole_diameter=param("body_porthole_diameter",11.0)
body_porthole_depth=param("body_porthole_depth",0.65)
body_porthole_radius=param("body_porthole_radius",56.0)
body_porthole_count=param("body_porthole_count",8)
key_spacing=param("key_spacing",92.0)
key_socket_width=param("key_socket_width",8.3)
key_socket_depth=param("key_socket_depth",5.4)
body_socket_pad_width=param("body_socket_pad_width",14.0)
body_socket_pad_height=param("body_socket_pad_height",9.0)
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
# Closed upper shell; base frame is the waist mating plane.
pts=[(r,s),(r-3,z+4),(hub+4,h-2),(hub,h),(bore,h),(bore,s),(hub-3,s),(hub-3,h-body_wall-2),(hub+3,h-body_wall-2),(r-6,s)]
with BuildPart() as upper_build:
    with BuildSketch(Plane.XZ):
        Polygon(*[(x,y-s) for x,y in pts],align=None)
    revolve(axis=Axis.Z)
body=upper_build.part
# Smooth cylindrical locating bore for the lift-off cockpit cover.
for x in [-key_spacing/2,key_spacing/2]:
    body=body+Pos(x,0,body_socket_pad_height/2)*Box(body_socket_pad_width,body_socket_pad_width,body_socket_pad_height)
    body=body-Pos(x,0,key_socket_depth/2)*Box(key_socket_width,key_socket_width,key_socket_depth)
# Cable is laid into the lower shell; upper shell closes the open notch.
pr=body_porthole_radius
surface=(z+4)+(r-3-pr)*((h-2)-(z+4))/((r-3)-(hub+4))
for i in range(int(body_porthole_count)):
    a=2*pi*i/int(body_porthole_count)
    body=body-Pos(pr*cos(a),pr*sin(a),surface+body_porthole_diameter/2-body_porthole_depth-s)*Sphere(body_porthole_diameter/2)
assert len(body.solids())==1
lamp_envelope=Pos(0,0,body_seat_z-s)*Cylinder(LAMP_D/2,LAMP_T,align=(Align.CENTER,Align.CENTER,Align.MIN))
assert (body & lamp_envelope).volume < 1e-5
body.color=Color(0.57,0.62,0.67)
publish("body",body,"飞碟上壳",material="petg")
