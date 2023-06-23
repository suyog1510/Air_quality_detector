import tkinter as tk
from PIL import ImageTk, Image
import requests
import json 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

root = tk.Tk()
root.title("Air Quality Index")

# Load the image and resize it to fit the GUI
img = Image.open("C:\Codes\Aqi Detector\images (1) (1).jpeg.jpg")
img = img.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.ANTIALIAS)
photo = ImageTk.PhotoImage(img)

# Create a label to display the image
image_label = tk.Label(root, image=photo)
image_label.place(x=0,y=0)

# # Load the image and resize it to fit the GUI
img2 = Image.open("AQI)Chart_US (1).png")
img2 = img2.resize((650, 350), Image.ANTIALIAS)
photo2 = ImageTk.PhotoImage(img2)

# Create a label to display the image
image_label = tk.Label(root, image=photo2)
image_label.pack()



label = tk.Label(root, text="Enter the name of the city:",font=("Arial", 20),)
label.pack(pady=20)

entry = tk.Entry(root,font=("Arial", 20))
entry.pack(pady=5)

label2 = tk.Label(root, text="NOTE:First Letter of the city should be capital",font=("Arial", 10),fg="Red")
label2.pack(pady=5)

city_name=""
def check_aqi():
    global city_name
    city_name = entry.get()
    url = "https://api.openaq.org/v1/latest?city={}".format(city_name)
    response = requests.get(url)
    data = json.loads(response.text)

    if data['results']:
        aqi = data['results'][0]['measurements'][0]['value']
        if aqi <= 50:
            result_label.config(text="Good\nAQI: {}".format(aqi),font=("Arial",20),  fg="green")
        elif aqi <= 100:
            result_label.config(text="Moderate\nAQI: {}".format(aqi),font=("Arial",20), fg="yellow")
        elif aqi <= 150:
            result_label.config(text="Unhealthy for Sensitive Groups\nAQI: {}".format(aqi),font=("Arial",20), fg="orange")
        elif aqi <= 200:
            result_label.config(text="Unhealthy\nAQI: {}".format(aqi),font=("Arial",20), fg="red") 
        elif aqi <= 300:
            result_label.config(text="Very Unhealthy\nAQI: {}".format(aqi),font=("Arial",20), fg="purple")       
        elif aqi<=500:
            result_label.config(text="Hazardous\nAQI: {}".format(aqi),font=("Arial", 20), fg="red")
        else:
            result_label.config(text="Wrong city or server issue\nAQI: {}".format(aqi),font=("Arial", 20), fg="red")
    else:
        result_label.config(text="Sorry, AQI data for {} is not available.".format(city),font=("Arial", 20), fg="Brown")

def graph():
    root = tk.Tk()
    root.title("AQI Line Graph")
    root.geometry("600x400")

    canvas = tk.Canvas(root)
    canvas.pack(fill="both", expand=True)
    url = f"https://api.openaq.org/v1/measurements?city={city_name}&parameter=pm25"

    response = requests.get(url)
    data = response.json()["results"]

    label3 = tk.Label(root, text="Graph of{}" .format(city_name),font=("Arial", 20),fg="Red")
    label3.pack(pady=5)

    dates = []
    aqi_values = []

    for reading in data:
        dates.append(reading["date"]["local"])
        aqi_values.append(reading["value"])

    fig = Figure(figsize=(6, 4), dpi=100)
    subplot = fig.add_subplot(111)
    subplot.plot(dates, aqi_values)

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

    root.mainloop()



check_button = tk.Button(root, text="Check AQI", font=("Arial", 20),command=check_aqi)
check_button.pack(pady=10)
check_graph = tk.Button(root, text="Check Graph", font=("Arial", 20),command=graph)
check_graph.pack(pady=10)

result_label = tk.Label(root, text="")
result_label.pack(pady=10)

root.mainloop()
