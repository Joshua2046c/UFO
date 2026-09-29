
shade_base_diameter = param("shade_base_diameter",114.0)
shade_top_diameter = param("shade_top_diameter",76.0)
shade_height = param("shade_height",140.0)
shade_wall = param("shade_wall",1.2)
shade_foot_height = param("shade_foot_height",3.0)
shade_foot_width = param("shade_foot_width",2.0)
spigot_diameter = param("spigot_diameter",68.0)
spigot_length = param("spigot_length",10.0)
shade_neck_wall = param("shade_neck_wall",2.5)
shade_blend_height = param("shade_blend_height",10.0)
shade_leadin = param("shade_leadin",0.5)
shade_cow_width=param("shade_cow_width",32.0)
shade_cow_height=param("shade_cow_height",24.0)
shade_cow_center_x=param("shade_cow_center_x",0.0)
shade_cow_center_z=param("shade_cow_center_z",38.0)
shade_cow_tilt_deg=param("shade_cow_tilt_deg",18.0)
shade_cow_tail_drop=param("shade_cow_tail_drop",7.5)
shade_cow_udder_width=param("shade_cow_udder_width",6.0)
shade_cow_udder_depth=param("shade_cow_udder_depth",3.8)
br=shade_base_diameter/2
tr=shade_top_diameter/2
sr=spigot_diameter/2
h=shade_height
pts=[(br,0),(br,shade_foot_height),(br-shade_foot_width,shade_foot_height),(tr,h),(sr,h),(sr,h+spigot_length-shade_leadin),(sr-shade_leadin,h+spigot_length),(sr-shade_neck_wall,h+spigot_length),(sr-shade_neck_wall,h),(tr-shade_wall,h-shade_blend_height),(br-shade_foot_width-shade_wall,shade_foot_height),(br-shade_foot_width-shade_wall,0)]
with BuildPart() as bp:
    with BuildSketch(Plane.XZ):
        Polygon(*pts,align=None)
    revolve(axis=Axis.Z)
shade=bp.part
# Original stylized cow silhouette from the user's reference: head right.
# Control points are normalized illustration proportions, not driving dimensions.
outline=[
[(-14,-10),(-16,-10),(-15.5,-7),(-15.5,-4)],
[(-15.5,-4),(-16.5,-2),(-16.5,1),(-16.4,3)],
# Downward tail: an open indentation separates it from the rump.
[(-16.4,3),(-17,3.5),(-17.2,3.5),(-17.3,2.5)],
[(-17.3,2.5),(-17.4,0),(-17.2,-2.5),(-18,-4.1)],
[(-18,-4.1),(-18.8,-5.2),(-20,-4.8),(-19.7,-3.5)],
[(-19.7,-3.5),(-19.4,0),(-19,3.5),(-18,5.0)],
[(-18,5.0),(-16,8),(-9,8),(-5,7.5)],
[(-5,7.5),(-1,7),(1,7),(4,7)],
[(4,7),(3,8.5),(1.5,11),(4,12)],
[(4,12),(5,12.3),(6,11),(7,10.5)],
[(7,10.5),(6,13),(6,16),(7.5,16)],
[(7.5,16),(9,16),(8.5,13),(9.5,12.5)],
[(9.5,12.5),(10.5,13),(11.5,13),(12,12.5)],
[(12,12.5),(12.5,14),(12.5,16),(14,15.5)],
[(14,15.5),(15,15),(13.8,12.5),(13.5,11.5)],
[(13.5,11.5),(16,13),(19,11),(16,9)],
[(16,9),(14.5,8),(15,7),(15.5,5)],
[(15.5,5),(16,3),(17.8,3),(18,1)],
[(18,1),(19,-3),(16,-5),(12,-4.5)],
[(12,-4.5),(10,-4),(9,-5),(9,-8)],
[(9,-8),(9,-10),(7,-10),(5.5,-10)],
[(5.5,-10),(4,-10),(4,-8),(4,-6)],
[(4,-6),(2,-5.5),(0.5,-5.3),(-0.5,-5.4)],
# Udder is part of the continuous cutout boundary; two rounded teats.
[(-0.5,-5.4),(-0.5,-6.2),(-0.9,-6.8),(-1.5,-7.0)],
[(-1.5,-7.0),(-1.4,-9.3),(-2.8,-9.4),(-2.9,-7.3)],
[(-2.9,-7.3),(-3.3,-7.5),(-3.8,-7.5),(-4.2,-7.3)],
[(-4.2,-7.3),(-4.1,-9.5),(-5.5,-9.5),(-5.6,-7.0)],
[(-5.6,-7.0),(-6.1,-6.7),(-6.7,-6.3),(-7,-5.7)],
[(-7,-5.7),(-7.4,-5.8),(-7.7,-5.9),(-8,-6)],
[(-8,-6),(-8,-8),(-8.5,-10),(-10,-10)],
[(-10,-10),(-11,-10),(-13,-10),(-14,-10)]
]
# Feature dimensions rescale normalized artwork locally, preserving its joins.
for i in [2,3,4,5,6]:
    outline[i]=[(x,3.5+(y-3.5)*shade_cow_tail_drop/7.5) if y<3.5 and x<=-17.2 else (x,y) for x,y in outline[i]]
for i,segment in enumerate(outline):
    outline[i]=[(-3.75+(x+3.75)*shade_cow_udder_width/6.0,
                 -5.4+(y+5.4)*shade_cow_udder_depth/3.8)
                if -7<=x<=-0.5 and y<=-5.4 else (x,y) for x,y in segment]
def cow_point(p):
    return (p[0]*shade_cow_width/36,(p[1]-3)*shade_cow_height/26)
with BuildPart() as cow_cut:
    with BuildSketch(Plane.XZ):
        with BuildLine():
            for segment in outline:
                Bezier(*[cow_point(p) for p in segment])
        make_face()
    # Plane.XZ normal is -Y: cut the front wall only, leaving the back intact.
    extrude(amount=br+shade_wall)
cow_tool=Pos(shade_cow_center_x,0,shade_cow_center_z)*Rot(0,-shade_cow_tilt_deg,0)*cow_cut.part
assert (shade & cow_tool).volume > 10
shade=shade-cow_tool
assert len(shade.solids())==1
shade.color=Color(0.23,0.8,0.08)
publish("shade",shade,"绿色光束灯罩",material="petg")
