package cs355.model.drawing;

import java.awt.Color;
import java.awt.geom.AffineTransform;
import java.awt.geom.Point2D;

/**
 * Add your square code here. You can add fields, but you cannot
 * change the ones that already exist. This includes the names!
 */
public class Square extends Shape {

	// The size of this Square.
	private double size;

	/**
	 * Basic constructor that sets all fields.
	 * @param color the color for the new shape.
	 * @param center the center of the new shape.
	 * @param size the size of the new shape.
	 */
	public Square(Color color, Point2D.Double center, double size) {

		// Initialize the superclass.
		super(color, center);

		// Set the field.
		this.size = size;
	}

	/**
	 * Getter for this Square's size.
	 * @return the size as a double.
	 */
	public double getSize() {
		return size;
	}

	/**
	 * Setter for this Square's size.
	 * @param size the new size.
	 */
	public void setSize(double size) {
		this.size = size;
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
		if(x>=(-size/2) && x<=(size/2)) {
			if(y>=(-size/2) && y<=(size/2)) {
				return true;
			}
		}
		
		return false;
	}

}
