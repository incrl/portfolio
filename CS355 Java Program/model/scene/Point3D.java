package cs355.model.scene;

/**
 * A simple 3D point used in Line3D and Scenes.
 */
public class Point3D {

	// Coordinates as doubles.
	public double x;
	public double y;
	public double z;

	/**
	 * Basic constructor. Puts the Point at the origin.
	 */
	public Point3D() {
		x = 0.0;
		y = 0.0;
		z = 0.0;
	}

	/**
	 * Basic constructor.
	 * @param x = the x coordinate of the new point.
	 * @param y = the y coordinate of the new point.
	 * @param z = the z coordinate of the new point.
	 */
	public Point3D(double x, double y, double z) {
		this.x = x;
		this.y = y;
		this.z = z;
	}

	double length() {
		return Math.sqrt(x * x + y * y + z * z);
	}

	@Override
	public String toString() {
		return "[X: "+ x + ", Y: " + y + ", Z:" + z + ']';
	}

	void normalize() {
		double denominator = Math.sqrt(x*x+y*y+z*z);
		x /= denominator;
		y /= denominator;
		z /= denominator;
	}
}
