
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
shade_cow_bridge_width=param("shade_cow_bridge_width",1.2)
shade_cow_eye_diameter=param("shade_cow_eye_diameter",1.8)
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
[(-15.5,-4),(-16.8,-1),(-17,1),(-17,3)],
[(-17,3),(-19,5),(-17,6),(-15,3)],
[(-15,3),(-15,8),(-9,8),(-5,7.5)],
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
[(4,-6),(0,-5),(-5,-5),(-8,-6)],
[(-8,-6),(-8,-8),(-8.5,-10),(-10,-10)],
[(-10,-10),(-11,-10),(-13,-10),(-14,-10)]
]
def cow_point(p):
    return (p[0]*shade_cow_width/36,(p[1]-3)*shade_cow_height/26)
with BuildPart() as cow_cut:
    with BuildSketch(Plane.XZ):
        with BuildLine():
            for segment in outline:
                Bezier(*[cow_point(p) for p in segment])
        make_face()
        # Retained coat patch joins the surrounding wall at the back, avoiding an island.
        patch=[
            [(-8.5,9.5),(-6,10),(-2.5,10),(-1.5,9)],
            [(-1.5,9),(-2,7),(-0.5,4),(-1.5,2)],
            [(-1.5,2),(-3,-0.5),(-7,-0.5),(-8,2)],
            [(-8,2),(-9,4),(-8,7),(-8.5,9.5)]
        ]
        with BuildLine():
            for segment in patch:
                Bezier(*[cow_point(p) for p in segment])
        make_face(mode=Mode.SUBTRACT)
        # One eye is supported by a stencil bridge to the forehead.
        eye_x,eye_z=cow_point((11.5,8))
        root_x,root_z=cow_point((11.5,14.5))
        with Locations((eye_x,eye_z)):
            Circle(shade_cow_eye_diameter/2,mode=Mode.SUBTRACT)
        with Locations((eye_x,(eye_z+root_z)/2)):
            Rectangle(shade_cow_bridge_width,root_z-eye_z,mode=Mode.SUBTRACT)
    # Plane.XZ normal is -Y: cut the front wall only, leaving the back intact.
    extrude(amount=br+shade_wall)
cow_tool=Pos(shade_cow_center_x,0,shade_cow_center_z)*Rot(0,-shade_cow_tilt_deg,0)*cow_cut.part
assert (shade & cow_tool).volume > 10
shade=shade-cow_tool
assert len(shade.solids())==1
shade.color=Color(0.23,0.8,0.08)
publish("shade",shade,"绿色光束灯罩",material="petg")
