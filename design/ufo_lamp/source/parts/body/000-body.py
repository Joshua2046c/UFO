
from bd_warehouse.thread import Thread
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
thread_major=param("thread_major",72.0)
thread_depth=param("thread_depth",1.8)
thread_pitch=param("thread_pitch",3.0)
thread_length=param("thread_length",9.0)
thread_root_width=param("thread_root_width",2.2)
thread_tip_width=param("thread_tip_width",0.6)
body_thread_clearance=param("body_thread_clearance",0.35)
body_thread_axial_clearance=param("body_thread_axial_clearance",0.25)
body_wire_diameter=param("body_wire_diameter",6.0)
body_wire_z=param("body_wire_z",19.5)
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
bore=thread_major/2-thread_depth+body_thread_clearance
pocket=LAMP_D/2+body_lamp_clearance
# Closed upper shell; base frame is the waist mating plane.
pts=[(r,s),(r-3,z+4),(hub+4,h-2),(hub,h),(bore,h),(bore,body_seat_z+LAMP_T+body_lamp_headroom),(pocket,body_seat_z+LAMP_T+body_lamp_headroom),(pocket,s),(hub-3,s),(hub-3,h-body_wall-2),(hub+3,h-body_wall-2),(r-6,s)]
with BuildPart() as upper_build:
    with BuildSketch(Plane.XZ):
        Polygon(*[(x,y-s) for x,y in pts],align=None)
    revolve(axis=Axis.Z)
body=upper_build.part
# Existing free hollow cap thread, as qualified by prior M72 kit rejection.
thread_cutter=Thread(apex_radius=thread_major/2+body_thread_clearance,apex_width=thread_tip_width+2*body_thread_axial_clearance,root_radius=bore,root_width=thread_root_width+2*body_thread_axial_clearance,pitch=thread_pitch,length=thread_length,end_finishes=("square","square"))
body=body-Pos(0,0,h-thread_length-0.5-s)*thread_cutter
for x in [-key_spacing/2,key_spacing/2]:
    body=body+Pos(x,0,body_socket_pad_height/2)*Box(body_socket_pad_width,body_socket_pad_width,body_socket_pad_height)
    body=body-Pos(x,0,key_socket_depth/2)*Box(key_socket_width,key_socket_width,key_socket_depth)
# Cable exits to rear of saucer, clear of both keys and the shade.
body=body-Pos(0,-r/2,body_wire_z-s)*Rot(90,0,0)*Cylinder(body_wire_diameter/2,r+2)
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
