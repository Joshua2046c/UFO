from math import sin, cos, pi, atan, degrees, sqrt
body_diameter=param("body_diameter",150.0)
body_split_height=param("body_split_height",16.0)
lower_wall=param("lower_wall",2.4)
body_hub_diameter=param("body_hub_diameter",80.0)
body_rim_height=param("body_rim_height",13.0)
lower_edge_wall=param("lower_edge_wall",4.8)
lower_edge_scale=param("lower_edge_scale",0.5)
spigot_diameter=param("spigot_diameter",68.0)
spigot_length=param("spigot_length",4.0)
body_socket_clearance=param("body_socket_clearance",0.3)
body_socket_headroom=param("body_socket_headroom",0.8)
body_lamp_clearance=param("body_lamp_clearance",0.5)
body_seat_thickness=param("body_seat_thickness",2.2)
body_light_aperture=param("body_light_aperture",56.0)
body_lamp_headroom=param("body_lamp_headroom",1.0)
lower_reinforced_wall=param("lower_reinforced_wall",3.2)
body_wire_diameter=param("body_wire_diameter",6.0)
body_wire_z=param("body_wire_z",7.0)
lower_wire_exit_radius=param("lower_wire_exit_radius",73.8)
lower_wire_exit_width=param("lower_wire_exit_width",6.0)
lower_wire_exit_height=param("lower_wire_exit_height",4.0)
magnet_spacing=param("magnet_spacing",92.0)
magnet_socket_diameter=param("magnet_socket_diameter",7.1)
magnet_socket_depth=param("magnet_socket_depth",2.2)
lower_socket_pad_width=param("lower_socket_pad_width",14.0)
lower_socket_pad_base=param("lower_socket_pad_base",4.0)
lower_thruster_count=param("lower_thruster_count",8)
lower_thruster_diameter=param("lower_thruster_diameter",16.0)
lower_thruster_ring_radius=param("lower_thruster_ring_radius",60.0)
lower_thruster_phase_deg=param("lower_thruster_phase_deg",22.5)
lower_thruster_socket_depth=param("lower_thruster_socket_depth",1.5)
lower_thruster_socket_clearance=param("lower_thruster_socket_clearance",0.5)
lower_thruster_socket_back_wall=param("lower_thruster_socket_back_wall",1.2)
# User supplied lamp envelope.
LAMP_D=60.0
LAMP_T=8.0
r=body_diameter/2
hub=body_hub_diameter/2
s=body_split_height
z=body_rim_height
edge_bottom=s-(s-(z-1))*lower_edge_scale
bevel_bottom=s-(s-(z-3))*lower_edge_scale
socket=spigot_diameter/2+body_socket_clearance
seat=spigot_length+body_socket_headroom+body_seat_thickness
pocket=LAMP_D/2+body_lamp_clearance
assert abs(seat+LAMP_T+body_lamp_headroom-s)<1e-6, "Lamp holder top must be flush with lower shell rim"
assert body_wire_z-body_wire_diameter/2>=lower_wall
slope=bevel_bottom/((r-1)-(hub+2))
wall_offset=lower_reinforced_wall*sqrt(1+slope*slope)
reinforcement_radius=r-lower_edge_wall
reinforcement_top=(reinforcement_radius-(hub+2))*slope+wall_offset
assert reinforcement_top<s
pts=[(socket,0),(hub+2,0),(r-1,bevel_bottom),(r,edge_bottom),(r,s),(r-lower_edge_wall,s),(r-lower_edge_wall,reinforcement_top),(hub+2,wall_offset),(hub-3,lower_wall),(hub-3,s),(pocket,seat+LAMP_T+body_lamp_headroom),(pocket,seat),(body_light_aperture/2,seat),(body_light_aperture/2,spigot_length+body_socket_headroom),(socket,spigot_length+body_socket_headroom)]
with BuildPart() as lower_build:
    with BuildSketch(Plane.XZ):
        Polygon(*pts,align=None)
    revolve(axis=Axis.Z)
body_lower=lower_build.part
# Verify the full radial rim width at the seam before the cable notch.
rim_check=Pos(0,0,(s+reinforcement_top)/2)*(Cylinder(r,s-reinforcement_top)-Cylinder(r-lower_edge_wall,s-reinforcement_top))
assert getattr(rim_check-body_lower,"volume",0.0)<1e-5
print("Lower rim radial wall:",lower_edge_wall)
# Eight blind sockets for independent hemispheres, along the underside normal.
slope=bevel_bottom/((r-1)-(hub+2))
mount_z=(lower_thruster_ring_radius-(hub+2))*slope
dome_r=lower_thruster_diameter/2
socket_r=(lower_thruster_diameter+lower_thruster_socket_clearance)/2
socket_depth=lower_thruster_socket_depth
back_wall=lower_thruster_socket_back_wall
# Continuous conical reinforcement replaces separate circular pads.
socket_tool=Pos(0,0,(lower_wall-socket_depth)/2)*Cylinder(socket_r,socket_depth+lower_wall)
floor_check=Pos(0,0,-socket_depth-back_wall/2)*Cylinder(socket_r,back_wall)
hemi=Sphere(dome_r) & Box(2*dome_r,2*dome_r,dome_r,align=(Align.CENTER,Align.CENTER,Align.MIN))
plug_check=hemi+Cylinder(dome_r,socket_depth,align=(Align.CENTER,Align.CENTER,Align.MAX))
socket_locations=[]
for i in range(int(lower_thruster_count)):
    angle=lower_thruster_phase_deg+360*i/int(lower_thruster_count)
    a=angle*pi/180
    mount=Pos(lower_thruster_ring_radius*cos(a),lower_thruster_ring_radius*sin(a),mount_z)*Rot(0,0,angle)*Rot(0,180-degrees(atan(slope)),0)
    body_lower=body_lower-mount*socket_tool
    socket_locations.append(mount)
# Bound the connector supports by the original exterior cone.
support_envelope=Cone(hub+2,hub+2+s/slope,s,align=(Align.CENTER,Align.CENTER,Align.MIN))
for x in [-magnet_spacing/2,magnet_spacing/2]:
    inner_end=hub-3-lower_wall/2
    outer_end=abs(x)+lower_socket_pad_width/2
    centre=(inner_end+abs(x))/2*(1 if x>0 else -1)
    bridge=Pos(centre,0,(s+lower_socket_pad_base)/2)*Box(abs(x)-inner_end,lower_socket_pad_width,s-lower_socket_pad_base)
    round_seat=Pos(x,0,(s+lower_socket_pad_base)/2)*Cylinder(lower_socket_pad_width/2,s-lower_socket_pad_base)
    support=bridge+round_seat
    body_lower=body_lower+(support & support_envelope)
    body_lower=body_lower-Pos(x,0,s-magnet_socket_depth/2)*Cylinder(magnet_socket_diameter/2,magnet_socket_depth)
# Open rectangular internal groove stops in the annular cavity.
route_length=hub+lower_wall
route_top=seat+LAMP_T+body_lamp_headroom+lower_wall
route_bottom=body_wire_z-body_wire_diameter/2
route_cutter=Pos(0,-route_length/2,(route_bottom+route_top)/2)*Box(body_wire_diameter,route_length,route_top-route_bottom)
body_lower=body_lower-route_cutter
assert getattr(body_lower & route_cutter,"volume",0.0)<1e-5
# Rectangular open-top notch in the lower rim.
# Matching half-notch is in the upper shell; total exit height remains 4 mm.
exit_tool=Pos(0,-lower_wire_exit_radius,s)*Box(lower_wire_exit_width,4*lower_wall,lower_wire_exit_height)
assert (body_lower & exit_tool).volume > 1.0
body_lower=body_lower-exit_tool
assert len(body_lower.solids())==1
assert getattr(body_lower & exit_tool,"volume",0.0) < 1e-5
# A 3.6 mm round lead clears the default 6 x 4 mm rectangular opening.
exit_check=Pos(0,-lower_wire_exit_radius,s)*Rot(90,0,0)*Cylinder((min(lower_wire_exit_width,lower_wire_exit_height)-0.4)/2,4*lower_wall)
assert getattr(body_lower & exit_check,"volume",0.0) < 1e-5
# Internal notch is twice the lower rim half-notch depth.
groove_bottom=body_wire_z-body_wire_diameter/2
groove_depth=s-groove_bottom
assert abs(groove_depth-lower_wire_exit_height)<1e-6
wire_radius=(min(body_wire_diameter,groove_depth)-0.4)/2
wire_check=Pos(0,-route_length/2,(s+groove_bottom)/2)*Rot(90,0,0)*Cylinder(wire_radius,route_length)
assert (s+groove_bottom)/2+wire_radius<s
assert getattr(part("body").body & (Pos(0,0,-s)*wire_check),"volume",0.0)<1e-5
print("Internal groove depth:",groove_depth,"lower edge notch depth:",lower_wire_exit_height/2)
assert getattr(body_lower & wire_check,"volume",0.0) < 1e-5
lamp_envelope=Pos(0,0,seat)*Cylinder(LAMP_D/2,LAMP_T,align=(Align.CENTER,Align.CENTER,Align.MIN))
assert getattr(body_lower & lamp_envelope,"volume",0.0) < 1e-5
for mount in socket_locations:
    assert getattr(body_lower & (mount*plug_check), "volume", 0.0)<1e-5
    assert getattr((mount*floor_check)-body_lower, "volume", 0.0)<1e-5
for x in [-magnet_spacing/2,magnet_spacing/2]:
    magnet_check=Pos(x,0,s-magnet_socket_depth/2)*Cylinder(magnet_socket_diameter/2,magnet_socket_depth)
    assert getattr(body_lower & magnet_check,"volume",0.0)<1e-5
    magnet_floor=Pos(x,0,s-magnet_socket_depth-lower_wall/2)*Cylinder(magnet_socket_diameter/2,lower_wall)
    assert getattr(magnet_floor-body_lower,"volume",0.0)<1e-5
assert getattr(body_lower-support_envelope,"volume",0.0)<1e-5, "Supports must not protrude below the exterior cone"
print("Continuous reinforcement normal wall:",lower_reinforced_wall,"centre annulus top:",s)
print("Thruster sockets:",int(lower_thruster_count),"diameter:",2*socket_r,"axial depth:",socket_depth,"floor:",back_wall)
print("Lamp seat:",seat,"pocket diameter:",2*pocket,"light opening:",body_light_aperture)
body_lower.color=Color(0.49,0.54,0.59)
publish("body_lower",body_lower,"飞碟封闭下壳",material="petg")
