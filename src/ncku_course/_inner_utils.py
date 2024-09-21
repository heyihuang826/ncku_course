def get_time(times):
    frame = [0 for i in range(112)]
    
    def to_frame(date, start_time, end_time):
        move = 0
        dic_time = {'0':0, 
               '1':1, 
               '2':2, 
               '3':3, 
               '4':4, 
               'N':5, 
               '5':6, 
               '6':7, 
               '7':8, 
               '8':9, 
               '9':10, 
               'A':11, 
               'B':12, 
               'C':13, 
               'D':14, 
               'E':15
               }
        
        start_time = dic_time[start_time]
        end_time = dic_time[end_time]
        for i in range(start_time, end_time + 1):
            frame[(date - 1) * 16 + i + move] = 1
            
    for i in times:
        if (i == ''):
            return [0 for i in range(112)]
        if (i[0] != '['):
            continue
        i = i[1:].split(']')
        date = int(i[0])
        time = i[1].split('~')
        if (len(time) == 2):
            to_frame(date, time[0], time[1])
        elif (len(time) == 1):
            if (time[0] == ''):
                return [0 for i in range(112)]
            to_frame(date, time[0], time[0])
        else:
            raise Exception("程式發生錯誤, 請聯絡開發者(錯誤代碼:0x00000004)")
    return frame