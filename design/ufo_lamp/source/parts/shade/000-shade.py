
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
shade_cable_width = param("shade_cable_width",6.0)
shade_cable_height = param("shade_cable_height",6.0)
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
shade=shade-Pos(0,-br,shade_cable_height/2)*Box(shade_cable_width,2*(shade_foot_width+shade_wall+shade_cable_height),shade_cable_height)
shade_neck_cable_width=param("shade_neck_cable_width",6.0)
shade_neck_cable_depth=param("shade_neck_cable_depth",7.0)
shade=shade-Pos(sr,0,h+spigot_length-shade_neck_cable_depth/2)*Box(2*(shade_neck_wall+shade_neck_cable_width),shade_neck_cable_width,shade_neck_cable_depth)
assert len(shade.solids())==1
shade.color=Color(0.23,0.8,0.08)
publish("shade",shade,"绿色光束灯罩",material="petg")
