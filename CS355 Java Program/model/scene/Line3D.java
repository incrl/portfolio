package cs355.model.scene;

/**
 * A simple line used in making models.
 */
public class Line3D {

	// The start point of the line.
	public Point3D start;

	// The ending point of the line.
	public Point3D end;

	/**
	 * Basic constructor.
	 * @param s = the starting point of the new line.
	 * @param e = the ending point of the new line.
	 */
	public Line3D(Point3D s, Point3D e) {
		start = s;
		end = e;
	}
}
