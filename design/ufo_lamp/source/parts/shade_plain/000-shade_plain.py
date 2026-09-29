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
shade_plain_blend_height = param("shade_plain_blend_height",10)
shade_plain_leadin = param("shade_plain_leadin",0.5)
br=shade_plain_base_diameter/2
tr=shade_plain_top_diameter/2
sr=shade_plain_spigot_diameter/2
h=shade_plain_height
pts=[(br,0),(br,shade_plain_foot_height),(br-shade_plain_foot_width,shade_plain_foot_height),(tr,h),(sr,h),(sr,h+shade_plain_spigot_length-shade_plain_leadin),(sr-shade_plain_leadin,h+shade_plain_spigot_length),(sr-shade_plain_neck_wall,h+shade_plain_spigot_length),(sr-shade_plain_neck_wall,h),(tr-shade_plain_wall,h-shade_plain_blend_height),(br-shade_plain_foot_width-shade_plain_wall,shade_plain_foot_height),(br-shade_plain_foot_width-shade_plain_wall,0)]
with BuildPart() as bp:
    with BuildSketch(Plane.XZ):
        Polygon(*pts,align=None)
    revolve(axis=Axis.Z)
shade_plain=bp.part
assert len(shade_plain.solids())==1
shade_plain.color=Color(0.23,0.8,0.08)
publish("shade_plain",shade_plain,"无镂空绿色灯罩",material="petg")
