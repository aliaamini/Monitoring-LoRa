import tkinter as tk
import serial
import firebase_admin
from firebase_admin import credentials, db
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# ================= FIREBASE =================

cred = credentials.Certificate("firebase_key.json")

firebase_admin.initialize_app(cred,{
    'databaseURL':'https://loramonitoring-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

firebase_ref = db.reference("sensor_data")

# ================= SERIAL =================

ser = serial.Serial(
    port="COM8",
    baudrate=115200,
    timeout=1
)

# ================= DATA =================

temp_data=[]
hum_data=[]
soil_data=[]
light_data=[]

# ================= GUI =================

root=tk.Tk()
root.title("LoRa Telemetry Dashboard")
root.geometry("900x800")
root.configure(bg="#1f2138")

title=tk.Label(
    root,
    text="LORA TELEMETRY DASHBOARD",
    font=("Arial",20,"bold"),
    bg="#1f2138",
    fg="white"
)

title.pack(pady=15)

panel=tk.Frame(root,bg="#1f2138")
panel.pack(pady=20)

def create_box(name,col):

    frame=tk.Frame(panel,bg="#2b2f4a",width=120,height=70)
    frame.grid(row=0,column=col,padx=15)

    label=tk.Label(frame,text=name,bg="#2b2f4a",fg="white")
    label.pack()

    value=tk.Label(
        frame,
        text="0",
        font=("Arial",16,"bold"),
        bg="#2b2f4a",
        fg="cyan"
    )

    value.pack()

    return value


node_value=create_box("NODE",0)
temp_value=create_box("TEMPERATURE °C",1)
hum_value=create_box("HUMIDITY %",2)
soil_value=create_box("SOIL",3)

status_box=tk.Frame(panel,bg="#2b2f4a",width=120,height=70)
status_box.grid(row=0,column=4,padx=15)

tk.Label(status_box,text="STATUS",bg="#2b2f4a",fg="white").pack()
tk.Label(status_box,text="OK",font=("Arial",16,"bold"),bg="#2b2f4a",fg="cyan").pack()

# ================= GRAPH =================

fig,(ax1,ax2,ax3,ax4)=plt.subplots(4,1,figsize=(6,8))
fig.subplots_adjust(hspace=0.7)

graph_frame=tk.Frame(root,bg="#1f2138")
graph_frame.pack(pady=20)

canvas=FigureCanvasTkAgg(fig,master=graph_frame)
canvas.get_tk_widget().pack()

def update_graph():

    ax1.clear()
    ax2.clear()
    ax3.clear()
    ax4.clear()

    ax1.plot(temp_data)
    ax1.set_title("Temperature (°C)")

    ax2.plot(hum_data)
    ax2.set_title("Humidity (%)")

    ax3.plot(soil_data)
    ax3.set_title("Soil Moisture")

    ax4.plot(light_data)
    ax4.set_title("Light (Lux)")

    canvas.draw()


# ================= SERIAL READ =================

def read_serial():

    if ser.in_waiting:

        data=ser.readline().decode().strip()

        if "ID:" in data:

            try:

                parts=data.split(",")

                node=parts[0].split(":")[1]
                temp=float(parts[1].split(":")[1])
                hum=float(parts[2].split(":")[1])
                soil=int(parts[3].split(":")[1])
                light=int(parts[4].split(":")[1])

                node_value.config(text="NODE_"+node)
                temp_value.config(text=str(temp))
                hum_value.config(text=str(hum))
                soil_value.config(text=str(soil))

                temp_data.append(temp)
                hum_data.append(hum)
                soil_data.append(soil)
                light_data.append(light)

                if len(temp_data)>20:
                    temp_data.pop(0)
                    hum_data.pop(0)
                    soil_data.pop(0)
                    light_data.pop(0)

                update_graph()

                # ================= FIREBASE SEND =================

                firebase_ref.push({
                    "node":node,
                    "temperature":temp,
                    "humidity":hum,
                    "soil":soil,
                    "light":light
                })

            except:
                pass

    root.after(1000,read_serial)

read_serial()

root.mainloop()