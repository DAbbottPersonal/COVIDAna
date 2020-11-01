from OrganizeFrames import organize_frame

days_to_analyse = 60
days_buffered   = 3

frames = []
for day in range(days_buffered, days_buffered+days_to_analyse):
    frame = organize_frame("US", day, by="country")
    print (frame)


