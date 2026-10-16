# cell: shade_plain
# cell: shade_plain

shade_plain_base_diameter = param("shade_plain_base_diameter",114)
shade_plain_top_diameter = param("shade_plain_top_diameter",76)
shade_plain_height = param("shade_plain_height",140)
shade_plain_wall = param("shade_plain_wall",1.2)
shade_plain_foot_height = param("shade_plain_foot_height",3)
shade_plain_foot_width = param("shade_plain_foot_width",2)
shade_plain_spigot_diameter = param("shade_plain_spigot_diameter",68)
shade_plain_spigot_length = param("shade_plain_spigot_length",10)
shade_plain_neck_wall = param("shade_plain_neck_wall",2.5)
shade_plain_leadin = param("shade_plain_leadin",0.5)
br=shade_plain_base_diameter/2
tr=shade_plain_top_diameter/2
sr=shade_plain_spigot_diameter/2
h=shade_plain_height
# Keep the inner cone parallel to the outer cone, referenced to the lower wall.
cone_slope=(br-shade_plain_foot_width-tr)/(h-shade_plain_foot_height)
shoulder_z=h-shade_plain_wall
inner_top_radius=tr+cone_slope*(h-shoulder_z)-shade_plain_wall
pts=[(br,0),(br,shade_plain_foot_height),(br-shade_plain_foot_width,shade_plain_foot_height),(tr,h),(sr,h),(sr,h+shade_plain_spigot_length-shade_plain_leadin),(sr-shade_plain_leadin,h+shade_plain_spigot_length),(sr-shade_plain_neck_wall,h+shade_plain_spigot_length),(sr-shade_plain_neck_wall,shoulder_z),(inner_top_radius,shoulder_z),(br-shade_plain_foot_width-shade_plain_wall,shade_plain_foot_height),(br-shade_plain_foot_width-shade_plain_wall,0)]
with BuildPart() as bp:
    with BuildSketch(Plane.XZ):
        Polygon(*pts,align=None)
    revolve(axis=Axis.Z)
shade_plain=bp.part
# Check actual kernel cross-section areas at five heights before the decorative cut.
from math import pi, sqrt
wall_samples=[]
for fraction in [0.01,0.25,0.5,0.75,0.99]:
    z=shade_plain_foot_height+fraction*(shoulder_z-shade_plain_foot_height)
    ro=br-shade_plain_foot_width-cone_slope*(z-shade_plain_foot_height)
    ring=section(shade_plain,section_by=Plane.XY.offset(z))
    measured=ro-sqrt(ro*ro-ring.area/pi)
    assert abs(measured-shade_plain_wall)<1e-5
    wall_samples.append((round(z,3),round(measured,6)))
cone_faces=[face for face in shade_plain.faces() if face.geom_type==GeomType.CONE and face.area>10000]
assert len(cone_faces)==2
normal_wall=cone_faces[0].distance_to(cone_faces[1])
assert abs(normal_wall-shade_plain_wall/sqrt(1+cone_slope**2))<1e-5
print("shade_plain: section z / radial wall mm",wall_samples,"normal wall mm",round(normal_wall,6))
assert len(shade_plain.solids())==1
shade_plain.color=Color(0.23,0.8,0.08)
publish("shade_plain",shade_plain,"无镂空绿色灯罩",material="petg")
