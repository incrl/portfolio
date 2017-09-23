package cs355.controller;

import java.awt.Color;
import java.awt.Point;
import java.awt.event.MouseEvent;
import java.awt.geom.AffineTransform;
import java.awt.geom.Point2D;
import java.awt.image.BufferedImage;
import java.io.File;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

import cs355.model.drawing.*;
import cs355.model.image.CS355Image;
import cs355.model.image.Image;
import cs355.model.scene.CS355Scene;
import cs355.model.scene.Point3D;
import cs355.GUIFunctions;

public class Controller implements CS355Controller {
	
	private Color color;
	private String tool;
	private Shape selected;
	private boolean drawing;
	private Point2D.Double start;
	private Point2D.Double current;
	private Model model;
	private int index = 0;
	private ArrayList<Point2D.Double> triangle = new ArrayList<>();
	private double tolerance = 6;
	private int handle_offset = 20;
	private int handle_size = 6;
	private boolean rotating;
	private String line_end;
	private int canvas_size = 2048;
	private int view_size = 512;
	private double scaling = 1;
	private int topleft_x = 0;
	private int topleft_y = 0;
	private int zoom_level = 0;
	private int max_zooms = 2;
	private boolean ignore = false;
	private CS355Scene scene = null;
	private boolean draw3D = false;
	private Image image;
	private boolean drawImage = false;
	
	private Point2D.Double makePoint(Point p) {
		double x = (double)p.x;
		double y = (double)p.y;
		Point2D.Double r = new Point2D.Double(x,y);
		return r;
	}
	
	public Controller(CS355Drawing model) {
		this.model = (Model)model;
		this.color = new Color(255,255,255);
	}
	
	@Override
	public void mouseClicked(MouseEvent e) {
		if(tool == "Triangle") {
			triangle.add(makePoint(e.getPoint()));
		}
		if(triangle.size() == 3) {
			
			//Retrieve the points
			Point2D.Double a = triangle.get(0); 
			Point2D.Double b = triangle.get(1);
			Point2D.Double c = triangle.get(2);
			
			//Transform points to world space
			a = goViewToWorld(a);
			b = goViewToWorld(b);
			c = goViewToWorld(c);
			
			//Calculate center
			double x = (a.getX() + b.getX() + c.getX())/3.0;
			double y = (a.getY() + b.getY() + c.getY())/3.0;
			Point2D.Double center = new Point2D.Double(x,y);
			
			//Adjust points relative to center
			Point2D.Double a_c = new Point2D.Double(a.getX()-x,a.getY()-y);
			Point2D.Double b_c = new Point2D.Double(b.getX()-x,b.getY()-y);
			Point2D.Double c_c = new Point2D.Double(c.getX()-x,c.getY()-y);
			
			Shape s = new Triangle(color, center, a_c, b_c, c_c);
			index = model.addShape(s);
			triangle.clear();
		}
	}

	@Override
	public void mousePressed(MouseEvent e) {
		start = makePoint(e.getPoint());
		
		if( tool == "Select")
			selectionTest();
		
	}

	@Override
	public void mouseReleased(MouseEvent e) {
		drawing = false;
		rotating = false;
	}

	@Override
	public void mouseEntered(MouseEvent e) {
		
	}

	@Override
	public void mouseExited(MouseEvent e) {
		
	}
	
	@Override
	public void mouseDragged(MouseEvent e) {
		
		current = makePoint(e.getPoint());
		
		Point2D.Double p1;
		Point2D.Double p2;
		
		//Transform the points into world space
		p1 = goViewToWorld(start);
		p2 = goViewToWorld(current);
		
		Shape s = currentShape();
		
		if(tool == "Line") {
			Line l = (Line)s;
			l.setColor(color);
			l.setCenter(p1);
			l.setEnd(p2);
		}
		
		if(tool == "Rectangle") {
			double width = Math.abs(p2.getX()-p1.getX());
			double height = Math.abs(p2.getY()-p1.getY());
			
			// Calculate the center
			double x = Math.min(p1.getX(), p2.getX());
			double y = Math.min(p1.getY(), p2.getY());
			Point2D.Double center = new Point2D.Double(x+width/2,y+height/2);
			
			Rectangle r = (Rectangle)s;
			r.setColor(color);
			r.setCenter(center);
			r.setHeight(height);
			r.setWidth(width);
			
		}
		
		if(tool == "Square") {
			//Calculate the length of the square (constrained)
			double length_x = Math.abs(p2.getX()-p1.getX());
			double length_y = Math.abs(p2.getY()-p1.getY());
			double length = Math.min(length_x, length_y);
			
			// Calculate the center
			double x = Math.min(p1.getX(), Math.max(p2.getX(), p1.getX()-length));
			double y = Math.min(p1.getY(), Math.max(p2.getY(), p1.getY()-length));
			Point2D.Double center = new Point2D.Double(x+length/2,y+length/2);
			
			Square sq = (Square)s;
			sq.setColor(color);
			sq.setCenter(center);
			sq.setSize(length);
		}
		
		if(tool == "Circle") {
			//Calculate the length of the circle (constrained)
			double length_x = Math.abs(p2.getX()-p1.getX());
			double length_y = Math.abs(p2.getY()-p1.getY());
			double diameter = Math.min(length_x, length_y);
			double radius = diameter/2.0;
			
			// Calculate the center
			double x = Math.min(p1.getX(), Math.max(p2.getX(), p1.getX()-diameter));
			double y = Math.min(p1.getY(), Math.max(p2.getY(), p1.getY()-diameter));
			Point2D.Double center = new Point2D.Double(x+radius,y+radius);
			
			Circle c = (Circle)s;
			c.setColor(color);
			c.setCenter(center);
			c.setRadius(radius);
		
		}
		
		if(tool == "Ellipse") {
			//Calculate the size of the ellipse
			double width = Math.abs(p2.getX()-p1.getX());
			double height = Math.abs(p2.getY()-p1.getY());
			
			//Calculate the center
			double x = Math.min(p1.getX(), p2.getX());
			double y = Math.min(p1.getY(), p2.getY());
			Point2D.Double center = new Point2D.Double(x+width/2,y+height/2);
			
			Ellipse el = (Ellipse)s;
			el.setColor(color);
			el.setCenter(center);
			el.setWidth(width);
			el.setHeight(height);
		}
		
		if(tool == "Select" && selected!=null) {
			
			//Rotate shape if handle selected
			if(rotating) {
				
				//Line extension
				if(selected instanceof Line) {
					if(line_end == "First") 
						selected.setCenter(p2);
					
					if(line_end == "Second")
						((Line) selected).setEnd(p2);
					
					model.shapeChanged();
					return;
				}
				
				double x = p2.getX() - selected.getCenter().getX();
				double y = p2.getY() - selected.getCenter().getY();
				
				double angle = 0;
				
				//Avoid divide by zero and get proper offset
				if(x > .001)
					angle = Math.atan(y/x) + Math.PI/2;
				if(x < -.001)
					angle = Math.atan(y/x) - Math.PI/2;
				selected.setRotation(angle);
			}
			//Otherwise drag shape
			else {
				//Calculate the offset from the current position
				double x = ((p2.getX() - p1.getX()) + selected.getCenter().getX());
				double y = ((p2.getY() - p1.getY()) + selected.getCenter().getY());
				
				Point2D.Double offset = new Point2D.Double(x,y);
				
				//Don't shift lines by selection
				if(!(selected instanceof Line))
					selected.setCenter(offset);
				
				start = current;
			}
		}
		
		//Drag the screen (Extra feature)
		if(tool == "Select" && selected == null) {
			double x = ((p2.getX() - p1.getX()));
			double y = ((p2.getY() - p1.getY()));
			
			topleft_x -= x;
			topleft_y -= y;
			
			//Check for out of bounds errors
			if(topleft_x < 0)
				topleft_x = 0;
			if(topleft_y < 0)
				topleft_y = 0;
			if(topleft_x > canvas_size - view_size)
				topleft_x = canvas_size - view_size;
			if(topleft_y > canvas_size - view_size)
				topleft_y = canvas_size - view_size;
			
			GUIFunctions.setHScrollBarPosit(topleft_x);
			GUIFunctions.setVScrollBarPosit(topleft_y);
			
			start = current;
		}
		
		//Notify the model it has changed
		model.shapeChanged();
	}
	
	@Override
	public void mouseMoved(MouseEvent e) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void colorButtonHit(Color c) {
		color = c;
		GUIFunctions.changeSelectedColor(color);
		if(tool == "Select" && selected != null) {
			selected.setColor(color);
			model.shapeChanged();
		}
	}

	@Override
	public void lineButtonHit() {
		tool = "Line";
	}

	@Override
	public void squareButtonHit() {
		tool = "Square";
	}

	@Override
	public void rectangleButtonHit() {
		tool = "Rectangle";
	}

	@Override
	public void circleButtonHit() {
		tool = "Circle";
	}

	@Override
	public void ellipseButtonHit() {
		tool = "Ellipse";
	}

	@Override
	public void triangleButtonHit() {
		tool = "Triangle";
		triangle.clear();
	}

	@Override
	public void selectButtonHit() {
		tool = "Select";
	}

	@Override
	public void zoomInButtonHit() {
		//Don't zoom in more than is allowed
		if(zoom_level >= max_zooms)
			return;
		
		zoom_level += 1;
		view_size /= 2;
		scaling *=2;
		
		//Zoom in on the center, adjust view corner
		topleft_x += view_size/2;
		topleft_y += view_size/2;
		
		//Set a flag to notify the listener to not
		//adjust for the newly created scroll bars
		ignore = true;
		
		//Set Scroll Bars Appropriately
		GUIFunctions.setHScrollBarKnob(view_size);
		GUIFunctions.setVScrollBarKnob(view_size);
		GUIFunctions.setHScrollBarPosit(topleft_x);
		GUIFunctions.setVScrollBarPosit(topleft_y);
		
		determineZoomText();
		
		ignore = false;
		GUIFunctions.printf("Top Left = " + Integer.toString(topleft_x) + "," + Integer.toString(topleft_y) );
		GUIFunctions.refresh();
	}

	@Override
	public void zoomOutButtonHit() {
		if(zoom_level <= -max_zooms)
			return;
		
		//Zoom out from the center, adjust view corner
		topleft_x -= view_size/2;
		topleft_y -= view_size/2;
		
		zoom_level -= 1;
		view_size *= 2;
		scaling /= 2;
		
		
		
		//Check for out of bounds errors
		if(topleft_x < 0)
			topleft_x = 0;
		if(topleft_y < 0)
			topleft_y = 0;
		if(topleft_x > canvas_size - view_size)
			topleft_x = canvas_size - view_size;
		if(topleft_y > canvas_size - view_size)
			topleft_y = canvas_size - view_size;
		
		//Set Scroll Bars Appropriately
		GUIFunctions.setHScrollBarPosit(topleft_x);
		GUIFunctions.setVScrollBarPosit(topleft_y);
		GUIFunctions.setHScrollBarKnob(view_size);
		GUIFunctions.setVScrollBarKnob(view_size);
		
		determineZoomText();
		
		GUIFunctions.printf("Top Left = " + Integer.toString(topleft_x) + "," + Integer.toString(topleft_y) );
		GUIFunctions.refresh();
	}

	@Override
	public void hScrollbarChanged(int value) {
		if(!ignore)
			topleft_x = value;
		GUIFunctions.printf("Top Left = " + Integer.toString(topleft_x) + "," + Integer.toString(topleft_y) );
		GUIFunctions.refresh();
	}

	@Override
	public void vScrollbarChanged(int value) {
		if(!ignore)
			topleft_y = value;
		GUIFunctions.printf("Top Left = " + Integer.toString(topleft_x) + "," + Integer.toString(topleft_y) );
		GUIFunctions.refresh();
	}

	@Override
	public void openScene(File file) {
		scene = new CS355Scene();
		scene.open(file);
		GUIFunctions.refresh();
	}

	@Override
	public void toggle3DModelDisplay() {
		//Toggle the flag
		draw3D = !draw3D;
		if(draw3D) {
			GUIFunctions.printf("In 3D Layer");
		}
		
		GUIFunctions.refresh();
	}

	@Override
	public void keyPressed(Iterator<Integer> iterator) {
		
		//Don't handle key presses if the 3D layer is off
		if(draw3D == false || scene == null){
			return;
		}
		
		while(iterator.hasNext()){
			int k = iterator.next();
			
			// w = 87 move forward
			if(k == 87) 
	        {
				Point3D camera = scene.getCameraPosition();
				double angle = scene.getCameraRotation();
	        	camera.z -= Math.cos(angle*Math.PI/180);
	        	camera.x -= Math.sin(angle*Math.PI/180);
	        	scene.setCameraPosition(camera);
	        }
	        // s = 83 move back
	        if(k == 83) 
	        {
	        	Point3D camera = scene.getCameraPosition();
				double angle = scene.getCameraRotation();
	        	camera.z += Math.cos(angle*Math.PI/180);
	        	camera.x += Math.sin(angle*Math.PI/180);
	        	scene.setCameraPosition(camera);
	        }
	        // a = 65 move left
	        if(k == 65) 
	        {
	        	Point3D camera = scene.getCameraPosition();
				double angle = scene.getCameraRotation();
	        	camera.z -= Math.sin(angle*Math.PI/180);
	        	camera.x += Math.cos(angle*Math.PI/180);
	        	scene.setCameraPosition(camera);
	        }
	        // d = 68 move right
	        if(k == 68)
	        {
	        	Point3D camera = scene.getCameraPosition();
				double angle = scene.getCameraRotation();
	        	camera.z += Math.sin(angle*Math.PI/180);
	        	camera.x -= Math.cos(angle*Math.PI/180);
	        	scene.setCameraPosition(camera);
	        }
	        // r = 82 move up
	        if(k == 82) 
	        {
	        	Point3D camera = scene.getCameraPosition();
	        	camera.y++;
	        	scene.setCameraPosition(camera);
	        }
	        // f = 70 move down
	        if(k == 70) 
	        {
	        	Point3D camera = scene.getCameraPosition();
	        	camera.y--;
	        	scene.setCameraPosition(camera);
	        }
	        // q = 81 rotate left
	        if(k == 81) 
	        {
	        	double angle = scene.getCameraRotation();
	        	angle -= 3;
	        	scene.setCameraRotation(angle);
	        }
	        // e = 69 rotate right
	        if(k == 69) 
	        {
	        	double angle = scene.getCameraRotation();
	        	angle += 3;
	        	scene.setCameraRotation(angle);
	        }
	        // h = 72 return home
	        if(k == 72) 
	        {
	        	Point3D camera = scene.getCameraPosition();
				double angle = scene.getCameraRotation();
	        	camera.x=0;
	        	camera.y=0;
	        	camera.z=10;
	        	angle=0;
	        	scene.setCameraPosition(camera);
	        	scene.setCameraRotation(angle);
	        }
		}
		
		GUIFunctions.refresh();
	}

	@Override
	public void openImage(File file) {
		image = new Image();
		image.open(file);
		GUIFunctions.refresh();
	}

	@Override
	public void saveImage(File file) {
		image.save(file);
	}

	@Override
	public void toggleBackgroundDisplay() {
		//Toggle the flag
		drawImage = !drawImage;
		GUIFunctions.refresh();
	}

	@Override
	public void saveDrawing(File file) {
		model.save(file);
	}

	@Override
	public void openDrawing(File file) {
		model.open(file);
	}

	@Override
	public void doDeleteShape() {
		if(tool == "Select" && selected != null) {
			model.deleteShape(index);
			selected = null;
			model.shapeChanged();
		}
	}

	@Override
	public void doEdgeDetection() {
		image.edgeDetection();
		GUIFunctions.refresh();
	}

	@Override
	public void doSharpen() {
		image.sharpen();
		GUIFunctions.refresh();
	}

	@Override
	public void doMedianBlur() {
		image.medianBlur();
		GUIFunctions.refresh();
	}

	@Override
	public void doUniformBlur() {
		image.uniformBlur();
		GUIFunctions.refresh();
	}

	@Override
	public void doGrayscale() {
		image.grayscale();
		GUIFunctions.refresh();
	}

	@Override
	public void doChangeContrast(int contrastAmountNum) {
		image.contrast(contrastAmountNum);
		GUIFunctions.refresh();
	}

	@Override
	public void doChangeBrightness(int brightnessAmountNum) {
		image.brightness(brightnessAmountNum);
		GUIFunctions.refresh();
	}

	@Override
	public void doMoveForward() {
		if(tool == "Select" && selected != null) {
			model.moveBackward(index);
			//Check to make sure the index isn't out of bounds
			if(index != model.getShapes().size()-1)
				index += 1;
		}
	}

	@Override
	public void doMoveBackward() {
		if(tool == "Select" && selected != null) {
			model.moveForward(index);
			//Check to make sure the index isn't out of bounds
			if(index != 0)
				index -= 1;
		}
	}

	@Override
	public void doSendToFront() {
		if(tool == "Select" && selected != null) {
			model.movetoBack(index);
			index = model.getShapes().size()-1;
		}
	}

	@Override
	public void doSendtoBack() {
		if(tool == "Select" && selected != null) {
			model.moveToFront(index);
			index = 0;
		}
	}
	
	public Shape getSelected() {
		if(tool == "Select" && selected != null)
			return selected;
		
		return null;
	}
	
	public int getHandleOffset() {
		return handle_offset;
	}
	
	public int getHandleSize() {
		return handle_size;
	}
	
	public int getTopLeftX() {
		return topleft_x;
	}
	
	public int getTopLeftY() {
		return topleft_y;
	}
	
	public double getScaling() {
		return scaling;
	}
	
	public CS355Scene getScene() {
		return scene;
	}
	
	public boolean getDraw3D() {
		return draw3D;
	}
	
	public boolean getDrawImage() {
		return drawImage;
	}
	
	public Image getImage() {
		return image;
	}
	
	private Shape currentShape() {
		if(!drawing && tool!="Selected") {
			drawing = true;
			//Return Null Shapes
			if(tool == "Line") {
				Shape s = new Line(color, start, start);
				index = model.addShape(s);
				return s;
			}
			if(tool == "Rectangle") {
				Shape s = new Rectangle(color, start, 0.0, 0.0);
				index = model.addShape(s);
				return s;
			}
			if(tool == "Square") {
				Shape s = new Square(color, start, 0.0);
				index = model.addShape(s);
				return s;
			}
			if(tool == "Circle") {
				Shape s = new Circle(color, start, 0.0);
				index = model.addShape(s);
				return s;
			}
			if(tool == "Ellipse") {
				Shape s = new Ellipse(color, start, 0.0, 0.0);
				index = model.addShape(s);
				return s;
			}
			else {
				drawing = false;
				return null;
			}
		}
		else {
			return model.getShape(index);
		}
		
	}
	
	//Check to see if the clicked point is a shape
	private void selectionTest() {
		
		//Check for rotation handle selection
		if(tool == "Select" && selected != null) {
			if(checkHandle()) {
				rotating = true;
				return;
			}
			
		}
		
		List<Shape> shapelist = model.getShapes();
		
		//Put point into world space
		
		//Go through the list in reverse order
		for(int i = shapelist.size()-1; i>=0; i--) {
			Shape s = shapelist.get(i);
			
			Point2D.Double p1;
			
			//Transform the points into world space
			p1 = goViewToWorld(start);

			//Run individual shape tests
			if(s.pointInShape(p1, tolerance/scaling)) {
				index = i;
				selected = s;
				break;
			}
			
			//If no shape was found
			if(i == 0) {
				selected = null;
			}
		}
		
		GUIFunctions.refresh();
		
	}
	
	private boolean checkHandle() {
		
		Point2D.Double p1;
		//Transform point to object space
		p1 = goViewToObject(start,selected);
		
		double x = p1.getX();
		double y = p1.getY();
		
		if( selected instanceof Line) {
			
			Line l = (Line)selected;
			p1 = goViewToWorld(start);
			Point2D.Double end1 = l.getCenter();
			if(Math.abs(p1.getX() - end1.getX()) <= tolerance/scaling && Math.abs(p1.getY() - end1.getY()) <= tolerance/scaling) {
				line_end = "First";
				return true;
			}
			
			Point2D.Double end2 = l.getEnd();
			if(Math.abs(p1.getX() - end2.getX()) <= tolerance/scaling && Math.abs(p1.getY() - end2.getY()) <= tolerance/scaling) {
				line_end = "Second";
				return true;
			}
				
			return false;
		}
		
		if( selected instanceof Rectangle) {
			Rectangle r = (Rectangle)selected;
			double height = r.getHeight();
			
			//Find the handle location
			double xcheck = 0; 
			double ycheck = - height/2 - handle_offset;

			if(Math.abs(x - xcheck) <= tolerance/scaling && Math.abs(y - ycheck) <= tolerance/scaling)
				return true;
			
			return false;
		}
		
		if( selected instanceof Square) {
			Square sq = (Square)selected;
			double length = sq.getSize();
			
			//Find the handle location
			double xcheck = 0; 
			double ycheck = - length/2 - handle_offset;

			if(Math.abs(x - xcheck) <= tolerance/scaling && Math.abs(y - ycheck) <= tolerance/scaling)
				return true;
			
			return false;
		}
		
		//Can't rotate a circle
		if( selected instanceof Circle) {
			return false;
		}
		
		if( selected instanceof Ellipse) {
			Ellipse el = (Ellipse)selected;
			double height = el.getHeight();
			
			//Find the handle location
			double xcheck = 0; 
			double ycheck = - height/2 - handle_offset;

			if(Math.abs(x - xcheck) <= tolerance/scaling && Math.abs(y - ycheck) <= tolerance/scaling)
				return true;
			
			return false;
		}
		
		if( selected instanceof Triangle) {
			//Triangle t = (Triangle)selected;
			
			//Find the handle location
			double xcheck = 0; 
			double ycheck = - 2*handle_offset;

			if(Math.abs(x - xcheck) <= tolerance/scaling && Math.abs(y - ycheck) <= tolerance/scaling)
				return true;
			
			if(Math.abs(start.getX() - x) <= tolerance/scaling && Math.abs(start.getY() - y) <= tolerance/scaling)
				return true;
			
			return false;
		}
		
		return false;
	}
	
	private void determineZoomText() {
		if(zoom_level == -2)
			GUIFunctions.setZoomText(.25);
		if(zoom_level == -1)
			GUIFunctions.setZoomText(.50);
		if(zoom_level == 0)
			GUIFunctions.setZoomText(1.00);
		if(zoom_level == 1)
			GUIFunctions.setZoomText(2.00);
		if(zoom_level == 2)
			GUIFunctions.setZoomText(4.00);
	}
	
	private Point2D.Double goViewToWorld(Point2D.Double viewPoint) {
		Point2D.Double p1 = new Point2D.Double();
		
		AffineTransform viewToWorld = new AffineTransform();
		
		//Transform the points into world space
		//viewToWorld.translate(topleft_x, topleft_y);
		//viewToWorld.scale(1/scaling, 1/scaling);
		
		AffineTransform translate = new AffineTransform(1, 0, 0, 1, 
				topleft_x, topleft_y);
		AffineTransform scale = new AffineTransform(1/scaling, 0, 0,
				1/scaling, 0, 0);
		
		viewToWorld.concatenate(translate);
		viewToWorld.concatenate(scale);
		
		viewToWorld.transform(viewPoint, p1);
		
		return p1;
	}
	
	private Point2D.Double goViewToObject(Point2D.Double viewPoint, Shape s) {
		Point2D.Double p1 = new Point2D.Double();
		double rotation = s.getRotation();
		Point2D.Double center = s.getCenter();
		
		AffineTransform viewToObject = new AffineTransform();
		
		//Transform the point into object space
		//viewToObject.rotate(-rotation);
		//viewToObject.translate(-center.getX(),-center.getY());
		
		AffineTransform rotate = 
				new AffineTransform(Math.cos(rotation),-Math.sin(rotation),
						Math.sin(rotation), Math.cos(rotation), 0, 0);
		AffineTransform translate1 = new AffineTransform(1, 0, 0, 1, -center.getX(), -center.getY());
		
		//Transform the point into world space
		//viewToObject.translate(topleft_x, topleft_y);
		//viewToObject.scale(1/scaling, 1/scaling);
		
		AffineTransform translate2 = new AffineTransform(1, 0, 0, 1, 
				topleft_x, topleft_y);
		AffineTransform scale = new AffineTransform(1/scaling, 0, 0,
				1/scaling, 0, 0);
		
		viewToObject.concatenate(rotate);
		viewToObject.concatenate(translate1);
		viewToObject.concatenate(translate2);
		viewToObject.concatenate(scale);
		
		viewToObject.transform(viewPoint, p1);
		
		return p1;
	}
	
}
