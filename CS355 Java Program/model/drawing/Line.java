package cs355.model.drawing;

import java.awt.Color;
import java.awt.geom.Point2D;

/**
 * Add your line code here. You can add fields, but you cannot
 * change the ones that already exist. This includes the names!
 */
public class Line extends Shape {

	// The ending point of the line.
	private Point2D.Double end;

	/**
	 * Basic constructor that sets all fields.
	 * @param color the color for the new shape.
	 * @param start the starting point.
	 * @param end the ending point.
	 */
	public Line(Color color, Point2D.Double start, Point2D.Double end) {

		// Initialize the superclass.
		super(color, start);

		// Set the field.
		this.end = end;
	}

	/**
	 * Getter for this Line's ending point.
	 * @return the ending point as a Java point.
	 */
	public Point2D.Double getEnd() {
		return end;
	}

	/**
	 * Setter for this Line's ending point.
	 * @param end the new ending point for the Line.
	 */
	public void setEnd(Point2D.Double end) {
		this.end = end;
	}

	/**
	 * Add your code to do an intersection test
	 * here. You <i>will</i> need the tolerance.
	 * @param pt = the point to test against.
	 * @param tolerance = the allowable tolerance.
	 * @return true if pt is in the shape,
	 *		   false otherwise.
	 */
	@Override
	public boolean pointInShape(Point2D.Double pt, double tolerance) {
		
		double x = pt.getX();
		double y = pt.getY();
		
		//Performing Bounding Box Test
		//This also removes infinite line problems
		if(Math.abs(center.getX()-x) > Math.abs(center.getX()-end.getX())) {
			if(Math.abs(center.getY()-y) > Math.abs(center.getY()-end.getY())) {
				return false;
			}
		}
		
		//Get the normal vector
		double nx = center.getY() - end.getY();
		double ny = end.getX() - center.getX();
		
		//Normalize the vector
		double magnitude = Math.sqrt(nx*nx + ny*ny);
		nx = nx/magnitude;
		ny = ny/magnitude;
		
		//Find the line distance to the origin
		double d = center.getX()*nx + center.getY()*ny; 
		
		//Find the distance to the line and see if it's within tolerance
		double distance = Math.abs(x*nx + y*ny - d);
		if(distance <= tolerance)
			return true;
		
		return false;
	}

}
