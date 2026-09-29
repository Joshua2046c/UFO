
from bd_warehouse.thread import Thread
cockpit_diameter=param("cockpit_diameter",80.0)
cockpit_height=param("cockpit_height",34.0)
cockpit_wall=param("cockpit_wall",2.4)
cockpit_flange_thickness=param("cockpit_flange_thickness",2.0)
cockpit_neck_inner_diameter=param("cockpit_neck_inner_diameter",63.0)
cockpit_leadin=param("cockpit_leadin",0.5)
thread_major=param("thread_major",72.0)
thread_depth=param("thread_depth",1.8)
thread_pitch=param("thread_pitch",3.0)
thread_length=param("thread_length",9.0)
thread_root_width=param("thread_root_width",2.2)
thread_tip_width=param("thread_tip_width",0.6)
r=cockpit_diameter/2
h=cockpit_height
R=(r*r+h*h)/(2*h)
cz=h-R
root=thread_major/2-thread_depth
inner=cockpit_neck_inner_diameter/2
neck_len=thread_length+cockpit_leadin
clip=Pos(0,0,h/2)*Box(3*r,3*r,h)
dome=(Pos(0,0,cz)*Sphere(R)) & clip
dome=dome-(Pos(0,0,cz)*Sphere(R-cockpit_wall))
flange=Cylinder(r,cockpit_flange_thickness,align=(Align.CENTER,Align.CENTER,Align.MIN))-Cylinder(inner,cockpit_flange_thickness,align=(Align.CENTER,Align.CENTER,Align.MIN))
neck=Pos(0,0,-neck_len)*Cylinder(root,neck_len+cockpit_flange_thickness,align=(Align.CENTER,Align.CENTER,Align.MIN))-Pos(0,0,-neck_len-1)*Cylinder(inner,neck_len+cockpit_flange_thickness+2,align=(Align.CENTER,Align.CENTER,Align.MIN))
thread=Thread(apex_radius=thread_major/2,apex_width=thread_tip_width,root_radius=root,root_width=thread_root_width,pitch=thread_pitch,length=thread_length,end_finishes=("fade","fade"))
cockpit=dome+flange+neck+Pos(0,0,-neck_len)*thread
assert len(cockpit.solids())==1
cockpit.color=Color(1.0,0.68,0.06)
publish("cockpit",cockpit,"旋拧圆顶座舱",material="petg")
