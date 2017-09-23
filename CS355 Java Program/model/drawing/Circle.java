package cs355.model.drawing;

import java.awt.Color;
import java.awt.geom.AffineTransform;
import java.awt.geom.Point2D;

/**
 * Add your circle code here. You can add fields, but you cannot
 * change the ones that already exist. This includes the names!
 */
public class Circle extends Shape {

	// The radius.
	private double radius;

	/**
	 * Basic constructor that sets all fields.
	 * @param color the color for the new shape.
	 * @param center the center of the new shape.
	 * @param radius the radius of the new shape.
	 */
	public Circle(Color color, Point2D.Double center, double radius) {

		// Initialize the superclass.
		super(color, center);

		// Set the field.
		this.radius = radius;
	}

	/**
	 * Getter for this Circle's radius.
	 * @return the radius of this Circle as a double.
	 */
	public double getRadius() {
		return radius;
	}

	/**
	 * Setter for this Circle's radius.
	 * @param radius the new radius of this Circle.
	 */
	public void setRadius(double radius) {
		this.radius = radius;
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
		//Radius Test
		if(x*x + y*y <= radius*radius)
			return true;
		
		return false;
	}

}
