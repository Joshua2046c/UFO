
def make_key(oid):
    w=param(oid+"_width",8.0)
    length=param(oid+"_length",10.0)
    lead=param(oid+"_lead_chamfer",0.5)
    rib_r=param(oid+"_rib_radius",0.4)
    rib_out=param(oid+"_rib_projection",0.14)
    rib_end=param(oid+"_rib_end_margin",1.0)
    key=Box(w,w,length)
    key=chamfer(key.edges(),length=lead)
    for x,y in [(w/2+rib_out-rib_r,0),(-w/2-rib_out+rib_r,0),(0,w/2+rib_out-rib_r),(0,-w/2-rib_out+rib_r)]:
        key=key+Pos(x,y,0)*Cylinder(rib_r,length-2*rib_end)
    assert len(key.solids())==1
    key.color=Color(0.25,0.27,0.3)
    publish(oid,key,"左连接方块" if oid=="key_left" else "右连接方块",material="petg")
make_key("key_left")
make_key("key_right")
