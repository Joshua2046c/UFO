
from bd_warehouse.thread import Thread
from screwjoint import make_screw_joint_v1, ScrewJointNotApplicableV1
from math import sin,cos,pi
body_diameter=param("body_diameter",150.0)
body_height=param("body_height",32.0)
body_wall=param("body_wall",2.4)
body_hub_diameter=param("body_hub_diameter",80.0)
body_rim_height=param("body_rim_height",13.0)
body_rim_band=param("body_rim_band",2.0)
spigot_diameter=param("spigot_diameter",68.0)
spigot_length=param("spigot_length",10.0)
body_socket_clearance=param("body_socket_clearance",0.3)
body_socket_headroom=param("body_socket_headroom",0.8)
body_lamp_clearance=param("body_lamp_clearance",0.5)
body_seat_thickness=param("body_seat_thickness",2.2)
body_light_aperture=param("body_light_aperture",56.0)
body_lamp_headroom=param("body_lamp_headroom",1.0)
thread_major=param("thread_major",72.0)
thread_depth=param("thread_depth",1.8)
thread_pitch=param("thread_pitch",3.0)
thread_length=param("thread_length",9.0)
thread_root_width=param("thread_root_width",2.2)
thread_tip_width=param("thread_tip_width",0.6)
body_thread_clearance=param("body_thread_clearance",0.35)
body_thread_axial_clearance=param("body_thread_axial_clearance",0.25)
body_wire_diameter=param("body_wire_diameter",6.0)
body_wire_radius=param("body_wire_radius",32.0)
body_porthole_diameter=param("body_porthole_diameter",11.0)
body_porthole_depth=param("body_porthole_depth",0.65)
body_porthole_radius=param("body_porthole_radius",56.0)
body_porthole_count=param("body_porthole_count",8)
# User supplied lamp envelope, no purchased model invented.
LAMP_D=60.0
LAMP_T=8.0
r=body_diameter/2
hub=body_hub_diameter/2
h=body_height
z=body_rim_height
socket=spigot_diameter/2+body_socket_clearance
seat=spigot_length+body_socket_headroom+body_seat_thickness
pocket=LAMP_D/2+body_lamp_clearance
bore=thread_major/2-thread_depth+body_thread_clearance
with BuildPart() as p:
    with BuildSketch(Plane.XZ):
        Polygon((socket,0),(hub+2,0),(r-1,z-3),(r,z-1),(r,z+1),(r-3,z+4),(hub+4,h-2),(hub,h),(bore,h),(bore,seat+LAMP_T+body_lamp_headroom),(pocket,seat+LAMP_T+body_lamp_headroom),(pocket,seat),(body_light_aperture/2,seat),(body_light_aperture/2,spigot_length+body_socket_headroom),(socket,spigot_length+body_socket_headroom),align=None)
    revolve(axis=Axis.Z)
body=p.part
with BuildPart() as c:
    with BuildSketch(Plane.XZ):
        Polygon((hub+0.5,-1),(r-body_wall-0.5,-1),(r-body_wall-0.5,z-2),(hub+3,h-body_wall-2),(hub+0.5,h-body_wall-2),align=None)
    revolve(axis=Axis.Z)
body=body-c.part
# Large hollow cap topology is outside the M2-M8 screw kit.
try:
    make_screw_joint_v1(size="M72",at=Location((0,0,h)),through=[],engage_depth=thread_length,into=body,label="dome_thread")
except ScrewJointNotApplicableV1 as e:
    print("dome_thread free implementation:",str(e))
else:
    raise AssertionError("Unexpected kit match for hollow cap")
t=Thread(apex_radius=thread_major/2+body_thread_clearance,apex_width=thread_tip_width+2*body_thread_axial_clearance,root_radius=bore,root_width=thread_root_width+2*body_thread_axial_clearance,pitch=thread_pitch,length=thread_length,end_finishes=("square","square"))
body=body-Pos(0,0,h-thread_length-0.5)*t
body=body-Pos(body_wire_radius,0,spigot_length)*Cylinder(body_wire_diameter/2,h-spigot_length,align=(Align.CENTER,Align.CENTER,Align.MIN))
# Shallow spherical porthole engravings on upper cone, all one printed body.
pr=body_porthole_radius
surface=(z+4)+(r-3-pr)*((h-2)-(z+4))/((r-3)-(hub+4))
for i in range(int(body_porthole_count)):
    a=2*pi*i/int(body_porthole_count)
    body=body-Pos(pr*cos(a),pr*sin(a),surface+body_porthole_diameter/2-body_porthole_depth)*Sphere(body_porthole_diameter/2)
assert len(body.solids())==1
assert seat+LAMP_T < h-thread_length-0.5
print("Lamp pocket diameter/depth:",2*pocket,LAMP_T+body_lamp_headroom,"seat z:",seat,"socket:",2*socket)
body.color=Color(0.57,0.62,0.67)
publish("body",body,"飞船本体",material="petg")
