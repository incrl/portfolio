package cs355.model.drawing;

import java.awt.Color;
import java.awt.geom.AffineTransform;
import java.awt.geom.Point2D;

/**
 * Add your triangle code here. You can add fields, but you cannot
 * change the ones that already exist. This includes the names!
 */
public class Triangle extends Shape {

	// The three points of the triangle.
	private Point2D.Double a;
	private Point2D.Double b;
	private Point2D.Double c;

	/**
	 * Basic constructor that sets all fields.
	 * @param color the color for the new shape.
	 * @param center the center of the new shape.
	 * @param a the first point, relative to the center.
	 * @param b the second point, relative to the center.
	 * @param c the third point, relative to the center.
	 */
	public Triangle(Color color, Point2D.Double center, Point2D.Double a,
					Point2D.Double b, Point2D.Double c)
	{

		// Initialize the superclass.
		super(color, center);

		// Set fields.
		this.a = a;
		this.b = b;
		this.c = c;
	}

	/**
	 * Getter for the first point.
	 * @return the first point as a Java point.
	 */
	public Point2D.Double getA() {
		return a;
	}

	/**
	 * Setter for the first point.
	 * @param a the new first point.
	 */
	public void setA(Point2D.Double a) {
		this.a = a;
	}

	/**
	 * Getter for the second point.
	 * @return the second point as a Java point.
	 */
	public Point2D.Double getB() {
		return b;
	}

	/**
	 * Setter for the second point.
	 * @param b the new second point.
	 */
	public void setB(Point2D.Double b) {
		this.b = b;
	}

	/**
	 * Getter for the third point.
	 * @return the third point as a Java point.
	 */
	public Point2D.Double getC() {
		return c;
	}

	/**
	 * Setter for the third point.
	 * @param c the new third point.
	 */
	public void setC(Point2D.Double c) {
		this.c = c;
	}

	/**
	 * Add your code to do an intersection test
	 * here. You shouldn't need the tolerance.
	 * @param pt = the point to test against.
	 * @param tolerance = the allowable tolerance.
	 * @return true if pt is in the shape,
	 *		   false otherwise.
	 */
	@Override
	public boolean pointInShape(Point2D.Double pt, double tolerance) {
		
		AffineTransform worldToObj = new AffineTransform();
	
		//worldToObj.rotate(-rotation);
		//worldToObj.translate(-center.x,-center.y);
		
		AffineTransform rotate = 
				new AffineTransform(Math.cos(rotation),-Math.sin(rotation),
						Math.sin(rotation), Math.cos(rotation), 0, 0);
		AffineTransform translate = new AffineTransform(1, 0, 0, 1, -center.getX(), -center.getY());
		
		worldToObj.concatenate(rotate);
		worldToObj.concatenate(translate);
		
		//Apply Transformation
		Point2D.Double objCoord = new Point2D.Double();
		worldToObj.transform(pt,objCoord);
		
		double x = objCoord.getX();
		double y = objCoord.getY();
		
		//Run geometry test in object space
		//Normal vector test
		
		//Find the normal vector to each line: (-y,x)
		double nx1 = a.getY() - b.getY();
		double nx2 = b.getY() - c.getY();
		double nx3 = c.getY() - a.getY();
		double ny1 = b.getX() - a.getX();
		double ny2 = c.getX() - b.getX();
		double ny3 = a.getX() - c.getX();
		
		//Take the dot product of each normal with each point
		double da = a.getX()*nx1 + a.getY()*ny1;
		double db = b.getX()*nx2 + b.getY()*ny2;
		double dc = c.getX()*nx3 + c.getY()*ny3;
		
		//Take the dot product of each normal with the test point
		double d1 = x*nx1 + y*ny1;
		double d2 = x*nx2 + y*ny2;
		double d3 = x*nx3 + y*ny3;
		
		//Take the difference between all the distances
		double diff1 = d1-da;
		double diff2 = d2-db;
		double diff3 = d3-dc;
		
		//If all of them are positive or all of them are negative,
		//The point is in the triangle
		boolean allpos = diff1 >= 0 && diff2 >= 0 && diff3 >= 0;
		boolean allneg = diff1 <= 0 && diff2 <= 0 && diff3 <= 0;
		
		if(allpos || allneg)
			return true;
		
		return false;
	}

}
