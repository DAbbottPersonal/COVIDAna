from OrganizeFrames import organize_frame


frame = organize_frame("US", 3, by="state")
print (frame)

frame = organize_frame("US", 3, by="country")
print (frame)

frame = organize_frame("France", 3, by="country")
print (frame)

frame = organize_frame("China", 3, by="country")
print (frame)


