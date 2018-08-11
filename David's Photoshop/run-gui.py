import tkinter as tk
import tkinter.filedialog
from PIL import ImageTk, Image
from photoshop import *
import numpy as np
from os.path import exists
import imageio
from time import sleep

class MyDialog:
	def __init__(self, asker, question):
		top = self.top = tk.Toplevel(asker)
		self.myLabel = tk.Label(top, text=question)
		self.myLabel.pack()

		self.myEntryBox = tk.Entry(top)
		self.myEntryBox.pack()

		self.mySubmitButton = tk.Button(top, text='Submit', command=self.send)
		self.mySubmitButton.pack()
		
		self.asker = asker

	def send(self):
		self.asker.dialog_value = self.myEntryBox.get()
		self.top.destroy()

class Application(tk.Frame):
	
    def __init__(self, master=None):
        super().__init__(master)

        self.pack()
        self.master = master
        self.buffer = None
        self.original_image = None
        self.photo = None
        self.filename = None
        self.pack()
        self.dialog_value = 0
        self.get_points = False
        self.four_points = []
        self.selecting_foreground = False
        self.selecting_background = False
        self.foreground = []
        self.background = []
        self.last_x = None
        self.last_y = None
        self.pressed = False
        self.create_widgets()
        
    def mouse_down(self,event):
        if self.selecting_foreground:
            self.last_x = event.x
            self.last_y = event.y
            self.foreground.append((self.last_y,self.last_x))
            
        elif self.selecting_background:
            self.last_x = event.x
            self.last_y = event.y
            self.background.append((self.last_y,self.last_x))
            
        self.pressed = True
        
    def mouse_drag(self,event):
        
        if self.pressed:
        
            x = event.x
            y = event.y

            if self.selecting_foreground:
                self.img_panel.create_line(self.last_x, self.last_y, x, y, fill = "Red")
                
                self.foreground.append((y,x))
                
            if self.selecting_background:
                self.img_panel.create_line(self.last_x, self.last_y, x, y, fill = "Blue")
                
                self.background.append((y,x))
                
            self.last_x = x
            self.last_y = y
    
    def mouse_up(self,event):
        self.pressed = False
        
        if self.get_points:
            self.four_points.append((event.y,event.x))
            
            if len(self.four_points) == 1:
                self.master.title("Select Top Right")

            elif len(self.four_points) == 2:
                self.master.title("Select Bottom Right")
                
            elif len(self.four_points) == 3:
                self.master.title("Select Bottom Left")

            elif len(self.four_points) == 4:
                self.buffer = performHomography(self.buffer, self.four_points[0],self.four_points[1],self.four_points[2],self.four_points[3])
                self.master.title("David's Photoshop")
                self.update_image()
        
    def create_widgets(self):
        self.top_frame = tk.Frame(self)
        self.top_frame.pack(fill=tk.X, side=tk.TOP)

        self.right_frame = tk.Frame(self)
        self.right_frame.pack(fill=tk.Y, side=tk.RIGHT)

        self.load_image_btn = tk.Button(self.top_frame, text="Load Image", command=self.load_image)
        self.load_image_btn.pack(side='left')

        self.reset_btn = tk.Button(self.top_frame, text='Reset', command=self.reset_image)
        self.reset_btn.pack(side='left')

        self.save_btn = tk.Button(self.top_frame, text='Save', command=self.save_image)
        self.save_btn.pack(side='left')

        self.gray_btn = tk.Button(self.right_frame, text='Grayscale', command=self.gray_scale)
        self.gray_btn.pack(side='top')

        self.bright_btn = tk.Button(self.right_frame, text='Brightness', command=self.adjust_brightness)
        self.bright_btn.pack(side='top')

        self.contrast_btn = tk.Button(self.right_frame, text='Contrast', command=self.adjust_contrast)
        self.contrast_btn.pack(side='top')

        #self.median_btn = tk.Button(self.right_frame, text='Median Blur', command=self.median_blur)
        #self.median_btn.pack(side='top')

        self.average_btn = tk.Button(self.right_frame, text='Blur', command=self.average_blur)
        self.average_btn.pack(side='top')

        self.sharpen_btn = tk.Button(self.right_frame, text='Sharpen', command=self.sharpen_im)
        self.sharpen_btn.pack(side='top')

        self.edge_btn = tk.Button(self.right_frame, text='Edge Detection', command=self.edge_detection)
        self.edge_btn.pack(side='top')

        self.seam_btn = tk.Button(self.right_frame, text='Seam Carving', command=self.seam_carving)
        self.seam_btn.pack(side='top')
        
        self.homography_btn = tk.Button(self.right_frame, text='Homography', command=self.homography)
        self.homography_btn.pack(side='top')
        
        self.graphcut_btn = tk.Button(self.right_frame, text='Graph Cut', command=self.graph_cut)
        self.graphcut_btn.pack(side='top')

        self.st1_btn = tk.Button(self.right_frame, text='Van Gogh', command=self.style_transfer_van_gogh)
        self.st1_btn.pack(side='top')

        self.st2_btn = tk.Button(self.right_frame, text='Candy', command=self.style_transfer_candy)
        self.st2_btn.pack(side='top')

        self.st3_btn = tk.Button(self.right_frame, text='Mosaic', command=self.style_transfer_mosaic)
        self.st3_btn.pack(side='top')

        self.st4_btn = tk.Button(self.right_frame, text='Udnie', command=self.style_transfer_udnie)
        self.st4_btn.pack(side='top')

        self.img_panel = tk.Canvas(self)
        self.img_panel.bind("<Button-1>", self.mouse_down)
        self.img_panel.bind("<B1-Motion>", self.mouse_drag)
        self.img_panel.bind("<ButtonRelease-1>", self.mouse_up)
        self.img_panel.pack()

        #self.quit_btn = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)
        #self.quit_btn.pack(side='bottom'

    def gray_scale(self):
        self.buffer = toGrayScale(self.buffer)
        self.update_image()

    def adjust_brightness(self):
        inputDialog = MyDialog(self,"How much? (Between -100 and 100)")
        self.wait_window(inputDialog.top)

        self.buffer = brightnessAdjust(self.buffer,int(self.dialog_value))
        self.update_image()
        self.dialog_value = 0

    def adjust_contrast(self):
        inputDialog = MyDialog(self,"How much? (Between -100 and 100)")
        self.wait_window(inputDialog.top)

        self.buffer = contrastAdjust(self.buffer,int(self.dialog_value))
        self.update_image()
        self.dialog_value = 0

    def median_blur(self):
        self.buffer = medianBlur(self.buffer)
        self.update_image()

    def average_blur(self):
        self.buffer = averageBlur(self.buffer)
        self.update_image()

    def sharpen_im(self):
        self.buffer = sharpen(self.buffer)
        self.update_image()

    def edge_detection(self):
        self.buffer = edgeDetect(self.buffer)
        self.update_image()

    def seam_carving(self):
        inputDialog = MyDialog(self,"How much X?")
        self.wait_window(inputDialog.top)
        dx = int(self.dialog_value)
        self.dialog_value = 0

        inputDialog = MyDialog(self,"How much Y?")
        self.wait_window(inputDialog.top)
        dy = int(self.dialog_value)
        self.dialog_value = 0

        inputDialog = MyDialog(self,"Forward Energy? (Y/N)")
        self.wait_window(inputDialog.top)
        choice = self.dialog_value
        self.dialog_value = 0

        if choice == "Y" or choice == "y" or choice == "yes":
            forwardEnergy = True
        else:
            forwardEnergy = False

        for _ in range(dx):
            image, marked = seamCarveX(self.buffer,forwardEnergy)
            photo = ImageTk.PhotoImage(Image.fromarray(marked))
            self.img_panel.create_image(0, 0, anchor=tk.NW, image=photo)
            self.update()
            sleep(.25)
            self.buffer = image
            photo = ImageTk.PhotoImage(Image.fromarray(self.buffer))
            self.photo = photo
            self.img_panel.create_image(0, 0, anchor=tk.NW, image=photo)
            self.update()

        for _ in range(dy):
            image, marked = seamCarveY(self.buffer,forwardEnergy)
            photo = ImageTk.PhotoImage(Image.fromarray(marked))
            self.img_panel.create_image(0, 0, anchor=tk.NW, image=photo)
            self.update()
            sleep(.25)
            self.buffer = image
            photo = ImageTk.PhotoImage(Image.fromarray(self.buffer))
            self.photo = photo
            self.img_panel.create_image(0, 0, anchor=tk.NW, image=photo)
            self.update()
            
        self.update_image()

    def homography(self):
        self.get_points=True
        self.master.title("Select Top Left")
        
    def graph_cut(self):
        
        if not self.selecting_foreground and not self.selecting_background:
        
            self.selecting_foreground = True
            self.master.title("Select Foreground, Then Click Graph Cut")
            
        elif self.selecting_foreground:
            self.selecting_foreground = False
            self.selecting_background = True
            self.master.title("Select Background, Then Click Graph Cut")
            
        elif self.selecting_background:
            # Complete Graph Cut
            self.buffer = graphCut(self.buffer, self.foreground, self.background)
            self.master.title("David's Photoshop")
            self.update_image()
        
    def style_transfer_van_gogh(self):
        self.buffer = styleTransfer(self.buffer,"Models/starry-night.pth")
        self.update_image()

    def style_transfer_candy(self):
        self.buffer = styleTransfer(self.buffer,"Models/candy.pth")
        self.update_image()

    def style_transfer_mosaic(self):
        self.buffer = styleTransfer(self.buffer,"Models/mosaic.pth")
        self.update_image()

    def style_transfer_udnie(self):
        self.buffer = styleTransfer(self.buffer,"Models/udnie.pth")
        self.update_image()


    def save_image(self):
        save_filename = tk.filedialog.asksaveasfilename(initialdir='.', title=self.filename, filetypes=[('image files', ('.png', '.jpg'))])
        imageio.imwrite(save_filename,self.buffer)

    def load_image(self):
        self.filename = tk.filedialog.askopenfilename(initialdir='.', title='select image', filetypes=[('image files',('.png','.jpg'))])
        if exists(self.filename):
            self.buffer = imageio.imread(self.filename)[:,:,:3]
            self.original_image = self.buffer.copy()
            self.update_image()
        else:
            print("File not found:", self.filename)

    def reset_image(self):
        self.buffer = self.original_image.copy()
        self.update_image()

    def update_image(self):
        # Turn off any values from other functions
        self.four_points = []
        self.get_points = False
        self.selecting_foreground = False
        self.selecting_background = False
        self.pressed=False
        self.foreground = []
        self.background = []
        self.master.title("David's Photoshop")
        
        # Update image and reload panel
        photo = ImageTk.PhotoImage(Image.fromarray(self.buffer))
        h, w, c = self.buffer.shape
        self.photo = photo
        self.img_panel.create_image(0, 0, anchor=tk.NW, image=photo)
        self.img_panel.configure(width=w, height=h)
        self.update()

	
def main():
    root = tk.Tk()
    root.title("David's Photoshop")
    app = Application(root)
    app.mainloop()

if __name__ == '__main__':
    main()
