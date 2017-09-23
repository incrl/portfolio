package cs355.view;

import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Graphics2D;
import java.awt.Stroke;
import java.awt.geom.AffineTransform;
import java.awt.geom.Point2D;
import java.awt.image.BufferedImage;
import java.awt.image.RescaleOp;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.Observable;

import cs355.GUIFunctions;
import cs355.controller.Controller;
import cs355.model.drawing.CS355Drawing;
import cs355.model.drawing.Circle;
import cs355.model.drawing.Ellipse;
import cs355.model.drawing.Line;
import cs355.model.drawing.Rectangle;
import cs355.model.drawing.Shape;
import cs355.model.drawing.Square;
import cs355.model.drawing.Triangle;
import cs355.model.image.Image;
import cs355.model.scene.CS355Scene;
import cs355.model.scene.Instance;
import cs355.model.scene.Line3D;
import cs355.model.scene.Point3D;
import cs355.model.scene.WireFrame;

public class Viewer implements ViewRefresher {

	private CS355Drawing model;
	private Controller control;
	private int handle_offset;
	private int handle_size;
	//90 degree field of view viewing angle
	private double fov = 90;
	//Near plane and far plane values
	private double np = 1;
	private double fp = 10000;
	
	public Viewer(CS355Drawing model, Controller control) {
		this.model = model;
		this.control = control;
		this.handle_offset = control.getHandleOffset();
		this.handle_size = control.getHandleSize();
		model.addObserver(this);
	}
	
	@Override
	public void update(Observable o, Object arg) {
		GUIFunctions.refresh();
	}

	@Override
	public void refreshView(Graphics2D g2d) {
		
		//Transform world coordinates to view coordinates
		//AffineTransform worldToView = new AffineTransform();
		//worldToView.scale(control.getScaling(), control.getScaling());
		//worldToView.translate(-control.getTopLeftX(), -control.getTopLeftY());
		
		//Draw images first
		if(control.getDrawImage() && control.getImage() != null) {
			Image image = control.getImage();
			BufferedImage buf = image.getImage();
			
			//Scale the drawing appropriately for the canvas
			AffineTransform wToView = makeTransform(0,0,0);
			g2d.setTransform(wToView);
			
			int width = image.getHeight();
			int height = image.getWidth();
			
			int x = 1024 - width/2;
			int y = 1024 - height/2;
			
			//Draw image in center
			g2d.drawImage(buf, null, y, x);
		}
		
		//Setup stuff for drawing shapes (scaling, colors, etc.)
		Stroke stroke1 = new BasicStroke(2);
		Color highlight = new Color(195,255,0);
		Stroke stroke2 = new BasicStroke((int)(5/control.getScaling()));
		int hs = (int)(handle_size/control.getScaling());
		List<Shape> shapelist = model.getShapes();
		
		for(int i = 0; i < shapelist.size(); i++) {
			Shape s = shapelist.get(i);
			g2d.setColor(s.getColor());
			g2d.setStroke(stroke1);
			
			if( s instanceof Line) {
				
				//There is no translation or rotation for a line
				AffineTransform objToView = makeTransform(0,0,0);
				g2d.setTransform(objToView);
				
				Line l = (Line)s;
				Point2D.Double start = l.getCenter();
				Point2D.Double end = l.getEnd();
				g2d.drawLine((int)start.getX(), (int)start.getY(), (int)end.getX(), (int)end.getY());
				
				
			}
			
			else if( s instanceof Rectangle) {
				Rectangle r = (Rectangle)s;
				Point2D.Double center = r.getCenter();
				int width = (int)r.getWidth();
				int height = (int)r.getHeight();
				
				//Get the center for translation
				int x = (int)center.getX();
				int y = (int)center.getY();

				//Translation and Rotation
				AffineTransform objToView = makeTransform(x,y,r.getRotation());
				g2d.setTransform(objToView);
				g2d.fillRect(-width/2, -height/2, width, height);
				
			}
			
			else if( s instanceof Square) {
				Square sq = (Square)s;
				Point2D.Double center = sq.getCenter();
				int length = (int)sq.getSize();
				
				//Get the center for translation
				int x = (int)center.getX();
				int y = (int)center.getY();
				
				//Translation and Rotation
				AffineTransform objToView = makeTransform(x,y,sq.getRotation());
				g2d.setTransform(objToView);
				g2d.fillRect(-length/2, -length/2, length, length);
				
			}
			
			else if( s instanceof Circle) {
				Circle c = (Circle)s;
				Point2D.Double center = c.getCenter();
				double radius = c.getRadius();
				int diameter = (int)(2*radius);
				int x = (int)center.getX();
				int y = (int)center.getY();
				
				//Translation and Rotation
				AffineTransform objToView = makeTransform(x,y,c.getRotation());
				g2d.setTransform(objToView);
				g2d.fillOval((int)-radius, (int)-radius, diameter, diameter);
				
			}
			
			else if( s instanceof Ellipse) {
				Ellipse el = (Ellipse)s;
				Point2D.Double center = el.getCenter();
				int width = (int)el.getWidth();
				int height = (int)el.getHeight();
				int x = (int)center.getX();
				int y = (int)center.getY();
				
				//Translation and Rotation
				AffineTransform objToView = makeTransform(x,y,el.getRotation());
				g2d.setTransform(objToView);
				g2d.fillOval(-width/2, -height/2, width, height);
			
			}
			
			else if( s instanceof Triangle) {
				Triangle t = (Triangle)s;
				Point2D.Double p1 = t.getA();
				Point2D.Double p2 = t.getB();
				Point2D.Double p3 = t.getC();
				
				//Get the center for translation
				int x = (int)t.getCenter().getX();
				int y = (int)t.getCenter().getY();
				
				//Make point arrays
				int[] xPoints = new int[3];
				int[] yPoints = new int[3];
				
				xPoints[0] = (int)p1.getX();
				xPoints[1] = (int)p2.getX();
				xPoints[2] = (int)p3.getX();
				yPoints[0] = (int)p1.getY();
				yPoints[1] = (int)p2.getY();
				yPoints[2] = (int)p3.getY();
				
				//Translation and Rotation
				AffineTransform objToView = makeTransform(x,y,t.getRotation());
				g2d.setTransform(objToView);
				g2d.fillPolygon(xPoints, yPoints, 3);
				
			}
		}
		
		//Draw the handle and highlight for the selected shape
		Shape h = control.getSelected();
		if(h!=null) {
			g2d.setColor(highlight);
			g2d.setStroke(stroke2);
			
			if( h instanceof Line) {
				
				//There is no translation or rotation for a line
				AffineTransform objToView = makeTransform(0,0,0);
				g2d.setTransform(objToView);
				
				Line l = (Line)h;
				Point2D.Double start = l.getCenter();
				Point2D.Double end = l.getEnd();

				g2d.drawRect((int)start.getX()-hs/2, (int)start.getY()-hs/2, hs, hs);
				g2d.drawRect((int)end.getX()-hs/2, (int)end.getY()-hs/2, hs, hs);
				
				
			}
			
			else if( h instanceof Rectangle) {
				Rectangle r = (Rectangle)h;
				Point2D.Double center = r.getCenter();
				int width = (int)r.getWidth();
				int height = (int)r.getHeight();
				
				//Get the center for translation
				int x = (int)center.getX();
				int y = (int)center.getY();

				//Translation and Rotation
				AffineTransform objToView = makeTransform(x,y,r.getRotation());
				g2d.setTransform(objToView);

				g2d.drawRect(-width/2, -height/2, width, height);
				g2d.drawOval(0, -height/2 - handle_offset, hs, hs);
				
			}
			
			else if( h instanceof Square) {
				Square sq = (Square)h;
				Point2D.Double center = sq.getCenter();
				int length = (int)sq.getSize();
				
				//Get the center for translation
				int x = (int)center.getX();
				int y = (int)center.getY();
				
				//Translation and Rotation
				AffineTransform objToView = makeTransform(x,y,sq.getRotation());
				g2d.setTransform(objToView);

				g2d.drawRect(-length/2, -length/2, length, length);
				g2d.drawOval(0, -length/2 - handle_offset, hs, hs);
				
			}
			
			else if( h instanceof Circle) {
				Circle c = (Circle)h;
				Point2D.Double center = c.getCenter();
				double radius = c.getRadius();
				int diameter = (int)(2*radius);
				int x = (int)center.getX();
				int y = (int)center.getY();
				
				//Translation and Rotation
				AffineTransform objToView = makeTransform(x,y,c.getRotation());
				g2d.setTransform(objToView);

				g2d.drawOval((int)-radius, (int)-radius, diameter, diameter);
				
			}
			
			else if( h instanceof Ellipse) {
				Ellipse el = (Ellipse)h;
				Point2D.Double center = el.getCenter();
				int width = (int)el.getWidth();
				int height = (int)el.getHeight();
				int x = (int)center.getX();
				int y = (int)center.getY();
				
				//Translation and Rotation
				AffineTransform objToView = makeTransform(x,y,el.getRotation());
				g2d.setTransform(objToView);

				g2d.drawOval(-width/2, -height/2, width, height);
				g2d.drawOval(0, -height/2 - handle_offset, hs, hs);
			
			}
			
			else if( h instanceof Triangle) {
				Triangle t = (Triangle)h;
				Point2D.Double p1 = t.getA();
				Point2D.Double p2 = t.getB();
				Point2D.Double p3 = t.getC();
				
				//Get the center for translation
				int x = (int)t.getCenter().getX();
				int y = (int)t.getCenter().getY();
				
				//Make point arrays
				int[] xPoints = new int[3];
				int[] yPoints = new int[3];
				
				xPoints[0] = (int)p1.getX();
				xPoints[1] = (int)p2.getX();
				xPoints[2] = (int)p3.getX();
				yPoints[0] = (int)p1.getY();
				yPoints[1] = (int)p2.getY();
				yPoints[2] = (int)p3.getY();
				
				//Translation and Rotation
				AffineTransform objToView = makeTransform(x,y,t.getRotation());
				g2d.setTransform(objToView);

				g2d.drawPolygon(xPoints, yPoints, 3);
				g2d.drawOval(0, -2*handle_offset, hs, hs);
				
			}
		}
		
		//If the 3D viewer is enabled, draw the 3D model
		if(control.getDraw3D()) {
			CS355Scene scene = control.getScene();
			if(scene == null)
				return;
			
			//Get World-to-Camera transformation
			Point3D pos = scene.getCameraPosition();
			double angle = scene.getCameraRotation()+180;
			
			double[][] t = {{1, 0, 0, -pos.x},
							{0, 1, 0, -pos.y},
							{0, 0, 1, -pos.z},
							{0, 0, 0, 1}};
			
			double v1 = Math.cos(angle*Math.PI/180);
			double v2 = Math.sin(angle*Math.PI/180);
			
			double[][] r = {{v1, 0, -v2, 0},
							{0 , 1, 0  , 0},
							{v2, 0, v1 , 0},
							{0 , 0, 0  , 1}};
			
			//Get Camera to Clip Coordinates
			double zoom = 1/Math.tan(fov/2); 
					
			double[][] c = {{zoom, 0   , 0               , 0                 },
							{0   , zoom, 0               , 0                 },
							{0   , 0   , (fp+np)/(fp-np) , (-2*np*fp)/(fp-np)},
							{0   , 0   , 1               , 0                 }};
			
			//Put it all into one transformation
			TransformMatrix rotate = new TransformMatrix(r);
			TransformMatrix translate = new TransformMatrix(t);
			TransformMatrix worldToClip = new TransformMatrix(c);
			worldToClip.multiplyMatrix(rotate);
			worldToClip.multiplyMatrix(translate);
			
			
			//Build a viewing transformation for later
			double[][] v = {{1028, 0    , 0, 1028},
							{0   , -1028, 0, 1028},
							{0   , 0    , 0  , 0},
							{0   , 0    , 0  , 1}};
			
			TransformMatrix cToView = new TransformMatrix(v);
			
			//Iterate through each object in the scene
			Iterator<Instance> objs = scene.instances().iterator();
			while(objs.hasNext()) {
				
				//Get the next object
				Instance next = objs.next();
				
				g2d.setColor(next.getColor());
				
				//Get the object location
				Point3D place = next.getPosition();
				double rot = next.getRotAngle();
				
				//Build Object to World transformation
				double[][] tr = { {1, 0, 0, -place.x},
								  {0, 1, 0, place.y},
								  {0, 0, 1, place.z},
								  {0, 0, 0, 1} };
				
				double vc = Math.cos(rot*Math.PI/180);
				double vs = Math.sin(rot*Math.PI/180);
				
				double[][] rt = {{vc, 0, -vs, 0},
								{0 , 1, 0  , 0},
								{vs, 0, vc , 0},
								{0 , 0, 0  , 1}};
				
				TransformMatrix objToWorld = new TransformMatrix(tr);
				TransformMatrix temp = new TransformMatrix(rt);
				objToWorld.multiplyMatrix(temp);
						
				//Iterate through all the lines in the object
				Iterator<Line3D> obj = next.getModel().getLines().iterator();
				
				//For each line in the object
				while( obj.hasNext() ) {
					
					Line3D line = obj.next();
					Point3D p1 = line.start;
					Point3D p2 = line.end;
					
					//Apply Transformation to get to World Coordinates
					Point4D w1 = objToWorld.multiplyPoint(p1);
					Point4D w2 = objToWorld.multiplyPoint(p2);

					//Apply Transformation to get to Clip Coordinates
					Point4D h1 = worldToClip.multiplyPoint(w1);
					Point4D h2 = worldToClip.multiplyPoint(w2);
					
					//Check to see if the line is in view
					if(isInView(h1,h2)) {
						//Canonicalize the point
						Point4D c1 = canonicalize(h1);
						Point4D c2 = canonicalize(h2);
						
						//Transform the point into view coordinates
						Point4D start = cToView.multiplyPoint(c1);
						Point4D end =  cToView.multiplyPoint(c2);
					
						//Draw the line on the screen
						int x1 = (int)start.x;
						int x2 = (int)end.x;
						int y1 = (int)start.y;
						int y2 = (int)end.y;
						
						//Scale the drawing appropriately for the canvas
						AffineTransform wToView = makeTransform(0,0,0);
						g2d.setTransform(wToView);
						
						
						//Draw the lines
						g2d.setStroke(stroke1);
						g2d.drawLine(x1, y1, x2, y2);
					}
				}
			}
		}
	}
	
	private AffineTransform makeTransform(int x, int y, double rotation) {
		AffineTransform objToView = new AffineTransform();
		//Do world to view transformation
		//objToView.scale(control.getScaling(), control.getScaling());
		//objToView.translate(-control.getTopLeftX(),-control.getTopLeftY());
		
		AffineTransform scale = new AffineTransform(control.getScaling(), 0, 0,
				control.getScaling(), 0, 0);
		AffineTransform translate1 = new AffineTransform(1, 0, 0, 1, 
				-control.getTopLeftX(), -control.getTopLeftY());
		
		//Do object to world transformation
		//objToView.translate(x, y);
		//objToView.rotate(rotation);
		
		AffineTransform translate2 = new AffineTransform(1, 0, 0, 1, x, y);
		AffineTransform rotate = 
				new AffineTransform(Math.cos(rotation),Math.sin(rotation),
						-Math.sin(rotation), Math.cos(rotation), 0, 0);
		
		objToView.concatenate(scale);
		objToView.concatenate(translate1);
		objToView.concatenate(translate2);
		objToView.concatenate(rotate);
		
		return objToView;
	}
	
	private boolean isInView(Point4D p1, Point4D p2) {
		
		double x1 = p1.x; double x2 = p2.x;
		double y1 = p1.y; double y2 = p2.y;
		double z1 = p1.z; double z2 = p2.z;
		double w1 = p1.w; double w2 = p2.w;
		
		//Perform Clipping Tests
		if(x1 > w1 && x2 > w2)
			return false;
		if(x1 < -w1 && x2 < -w2)
			return false;
		if(y1 > w1 && y2 > w2)
			return false;
		if(y1 < -w1 && y2 < -w2)
			return false;
		if(z1 > w1 && z2 > w2)
			return false;
		//Fail if either point fails the near point test
		if(z1 < -w1 || z2 < -w2)
			return false;
		
		return true;
	}

	private Point4D canonicalize(Point4D pt){
		
		double x = pt.x; 
		double y = pt.y;
		double z = pt.z;
		double w = pt.w;
		
		Point4D result = new Point4D(x/w, y/w, z/w, 1.0);
		return result;
	}

}