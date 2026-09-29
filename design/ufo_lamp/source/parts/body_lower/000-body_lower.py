body_diameter=param("body_diameter",150.0)
body_split_height=param("body_split_height",16.0)
lower_wall=param("lower_wall",2.4)
body_hub_diameter=param("body_hub_diameter",80.0)
body_rim_height=param("body_rim_height",13.0)
spigot_diameter=param("spigot_diameter",68.0)
spigot_length=param("spigot_length",10.0)
body_socket_clearance=param("body_socket_clearance",0.3)
body_socket_headroom=param("body_socket_headroom",0.8)
body_lamp_clearance=param("body_lamp_clearance",0.5)
body_seat_thickness=param("body_seat_thickness",2.2)
body_light_aperture=param("body_light_aperture",56.0)
body_lamp_headroom=param("body_lamp_headroom",1.0)
lower_holder_wall=param("lower_holder_wall",2.5)
body_wire_diameter=param("body_wire_diameter",6.0)
body_wire_z=param("body_wire_z",13.0)
lower_wire_exit_radius=param("lower_wire_exit_radius",63.0)
key_spacing=param("key_spacing",92.0)
key_socket_width=param("key_socket_width",8.3)
key_socket_depth=param("key_socket_depth",5.4)
lower_socket_pad_width=param("lower_socket_pad_width",14.0)
lower_socket_pad_base=param("lower_socket_pad_base",4.0)
# User supplied lamp envelope.
LAMP_D=60.0
LAMP_T=8.0
r=body_diameter/2
hub=body_hub_diameter/2
s=body_split_height
z=body_rim_height
socket=spigot_diameter/2+body_socket_clearance
seat=spigot_length+body_socket_headroom+body_seat_thickness
pocket=LAMP_D/2+body_lamp_clearance
pts=[(socket,0),(hub+2,0),(r-1,z-3),(r,z-1),(r,s),(r-lower_wall,s),(r-lower_wall,z-1),(hub+1.6,lower_wall),(hub-3,lower_wall),(hub-3,s),(pocket+lower_holder_wall,s),(pocket+lower_holder_wall,seat+LAMP_T+body_lamp_headroom),(pocket,seat+LAMP_T+body_lamp_headroom),(pocket,seat),(body_light_aperture/2,seat),(body_light_aperture/2,spigot_length+body_socket_headroom),(socket,spigot_length+body_socket_headroom)]
with BuildPart() as lower_build:
    with BuildSketch(Plane.XZ):
        Polygon(*pts,align=None)
    revolve(axis=Axis.Z)
body_lower=lower_build.part
for x in [-key_spacing/2,key_spacing/2]:
    body_lower=body_lower+Pos(x,0,(s+lower_socket_pad_base)/2)*Box(lower_socket_pad_width,lower_socket_pad_width,s-lower_socket_pad_base)
    body_lower=body_lower-Pos(x,0,s-key_socket_depth/2)*Box(key_socket_width,key_socket_width,key_socket_depth)
# Open internal U-groove stops in the annular cavity; the outer rim stays intact.
route_length=hub+lower_wall
route_top=seat+LAMP_T+body_lamp_headroom+lower_wall
body_lower=body_lower-Pos(0,-route_length/2,body_wire_z)*Rot(90,0,0)*Cylinder(body_wire_diameter/2,route_length)
body_lower=body_lower-Pos(0,-route_length/2,(body_wire_z+route_top)/2)*Box(body_wire_diameter,route_length,route_top-body_wire_z)
# Downward exit on the underside slope at the user's marked rear location.
exit_tool=Pos(0,-lower_wire_exit_radius,s/2)*Cylinder(body_wire_diameter/2,s+2*lower_wall)
body_lower=body_lower-exit_tool
assert len(body_lower.solids())==1
assert (body_lower & exit_tool).volume < 1e-5
# A cable smaller than the nominal 6 mm channel clears the lower route.
wire_check=Pos(0,-route_length/2,body_wire_z)*Rot(90,0,0)*Cylinder((body_wire_diameter-0.4)/2,route_length)
assert (body_lower & wire_check).volume < 1e-5
lamp_envelope=Pos(0,0,seat)*Cylinder(LAMP_D/2,LAMP_T,align=(Align.CENTER,Align.CENTER,Align.MIN))
assert (body_lower & lamp_envelope).volume < 1e-5
print("Lamp seat:",seat,"pocket diameter:",2*pocket,"light opening:",body_light_aperture)
body_lower.color=Color(0.49,0.54,0.59)
publish("body_lower",body_lower,"飞碟封闭下壳",material="petg")
