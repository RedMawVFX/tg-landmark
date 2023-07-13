from tkinter import *
import terragen_rpc as tg

gui = Tk()
gui.title("tg_landmark")
gui.geometry("500x250")

# Frame setup
frame1 = LabelFrame(gui,text="Add landmark at origin",padx=5,pady=5) 
frame2 = LabelFrame(gui,text="Add landmark at coordinates",padx=5,pady=5)
frame3 = LabelFrame(gui,relief=FLAT,bg="#FFF9EC") # Errors and messages

gui.grid_columnconfigure(0,weight=1)
gui.grid_columnconfigure(1,weight=1)
gui.grid_rowconfigure(0,weight=1)
gui.grid_rowconfigure(1,weight=2)

frame1.grid(row=0,column = 0,sticky='nsew')
frame2.grid(row=0,column = 1,sticky='nsew')
frame3.grid(row=1,column = 0,columnspan=2,sticky='nsew')


def add_landmark(x):    
    scale = [2, 20, 200, 2000]
    landmark_values = [] #name, scale, postion, colour
    landmark_values.append("Landmark " + str(scale[x-1]) + "m")
    landmark_values.append(scale[x-1])        
    landmark_values.append((0, 0, 0))
    landmark_values.append((0, 1, 0))
    rpc_landmark(landmark_values)        
    if rpc_error.get() == False:
        message.set(landmark_values[0] + " added at origin")

def add_landmark_at(x):  # Create landmark at clipboard coordinates        
    clipboard_text = gui.clipboard_get()    
    if clipboard_text[0:4] == "xyz:":
        trimmed_text = clipboard_text[5:] # trim off xyz: from front of string        
        split_text = trimmed_text.split(",")
        position = str(split_text[0] + " " + split_text[1] + " " + split_text[2])      
        scale = [2, 20, 200, 2000]
        landmark_values = [] #name, scale, postion, colour
        landmark_values.append("Landmark " + str(scale[x-1]) + "m")
        landmark_values.append(scale[x-1])        
        landmark_values.append(position)
        landmark_values.append((0, 0, 1))
        rpc_landmark(landmark_values)
        if rpc_error.get() == False:                        
            message.set(landmark_values[0]+" added at coordinates "+landmark_values[2])            
    else:
        message.set("Invalid coordinates in clipboard.")
        

def rpc_landmark(landmark_values): # pass all the stuff in one list        
    try:
        project = tg.root()
        new_landmark = tg.create_child(project,'landmark')
        new_landmark.set_param('name', landmark_values[0])
        new_landmark.set_param('position',landmark_values[2])
        new_landmark.set_param('scale',landmark_values[1])
        new_landmark.set_param('colour',landmark_values[3])
        rpc_error.set(False)
    except ConnectionError as e:        
        formatted_message = format_message("Terragen RPC connection error: " + str(e))   
        message.set(formatted_message) 
        rpc_error.set(True)        
    except TimeoutError as e:
        message.set("Terragen RPC timeout error: " + str(e))        
        rpc_error.set(True)        
    except tg.ReplyError as e:
        message.set("Terragen RPC server reply error: " + str(e))        
        rpc_error.set(True)
    except tg.ApiError:
        message.set("Terragen RPC API error")
        rpc_error.set(True)        
        raise

def set_rb_origin(x):
    rb_origin.set(x)

def set_rb_coordinates(x):
    rb_coordinates.set(x)

# Splits a very long error message across two lines of the label widget
def format_message(text):    
    formatted_text = text    
    if len(text) >= 80:
        n = int(len(text) / 2)
        formatted_text = text[:n] + " \n" + text[n:]    
    return(formatted_text)

#variables
error_message = StringVar()
info_message = StringVar()
rpc_error = BooleanVar(gui,False)
rb_origin = IntVar() # radio button selected for add landmark at origin
rb_origin.set(1) 
rb_coordinates = IntVar()# radio button selected for add landmark at coordinates
rb_coordinates.set(1)
message = StringVar()

# Add Landmark gui
r1 = Radiobutton(frame1,text = '2m',variable=rb_origin, value=1,command=lambda: set_rb_origin(rb_origin.get())).grid(row=1,column=0)
r2 = Radiobutton(frame1,text = '20m',variable=rb_origin, value=2,command=lambda: set_rb_origin(rb_origin.get())).grid(row=1,column=1)
r3 = Radiobutton(frame1,text = '200m',variable=rb_origin, value=3,command=lambda: set_rb_origin(rb_origin.get())).grid(row=1,column=2)
r4 = Radiobutton(frame1,text = '2km',variable=rb_origin, value=4,command=lambda: set_rb_origin(rb_origin.get())).grid(row=1,column=3)

r5 = Radiobutton(frame2,text = '2m',variable=rb_coordinates, value=1,command=lambda: set_rb_coordinates(rb_coordinates.get())).grid(row=1,column=0)
r6 = Radiobutton(frame2,text = '20m',variable=rb_coordinates, value=2,command=lambda: set_rb_coordinates(rb_coordinates.get())).grid(row=1,column=1)
r7 = Radiobutton(frame2,text = '200m',variable=rb_coordinates, value=3,command=lambda: set_rb_coordinates(rb_coordinates.get())).grid(row=1,column=2)
r8 = Radiobutton(frame2,text = '2km',variable=rb_coordinates, value=4,command=lambda: set_rb_coordinates(rb_coordinates.get())).grid(row=1,column=3)

label1 = Label(frame1,text=" ").grid(row=2,columnspan=4)
label2 = Label(frame2,text="Copy coordinates to clipboard first!",fg="blue").grid(row=2,columnspan=4)

button1 = Button(frame1,text="Add landmark",bg="green",fg="white",command=lambda: add_landmark(rb_origin.get())).grid(row=3,columnspan=4)
button2 = Button(frame2,text="Add landmark",bg="blue",fg="white",command=lambda: add_landmark_at(rb_coordinates.get())).grid(row=3,columnspan=4)

# Message section -----
label3 = Label(frame3,text="Messages: ",bg="#FFF9EC").grid(row=0,column=0,pady=5,sticky='w')
Label4 = Label(frame3,textvariable=message,bg="#FFF9EC").grid(row=1,column=0,stick='w',)

gui.mainloop()

