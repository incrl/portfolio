package cs355.model.scene;

import java.awt.Color;

/**
 * One instance of a model in a scene, including
 * where the model is and how it's rotated.
 * @author gavin
 */
public class Instance {

	// The color to draw the lines.
	private Color color;

	// The position of the model in 3D space.
	private Point3D position;

	// The rotation of the model around the y-axis.
	private double rotAngle;

	// The scale of the model.
	private double scale;

	// The actual model.
	private WireFrame model;

	/**
	 * A default instance with no model.
	 */
	public Instance() {
		color = Color.WHITE;
		position = new Point3D();
		rotAngle = 0.0;
		scale = 1.0;
		model = new WireFrame();
	}

	/**
	 * A constructor that takes one parameter per field.
	 * @param color the color of this instance.
	 * @param pos the position of this instance in 3D space.
	 * @param angle the rotation angle of this instance
	 *				around the y-axis.
	 * @param scale the scale of the model.
	 * @param model the actual model.
	 */
	public Instance(Color color, Point3D pos, double angle, double scale, WireFrame model)
	{
		this.color = color;
		this.position = pos;
		this.rotAngle = angle;
		this.scale = scale;
		this.model = model;
	}

	/**
	 * Getter for this Instance's drawing color.
	 * @return the color that this Instance should be drawn with.
	 */
	public Color getColor() {
		return color;
	}

	/**
	 * Setter for this Instance's drawing color.
	 * @param color the new color that this
	 *				Instance should be drawn with.
	 */
	public void setColor(Color color) {
		this.color = color;
	}

	/**
	 * Getter for this Instance's position in the 3D world.
	 * @return the 3D position of this Instance.
	 */
	public Point3D getPosition() {
		return position;
	}

	/**
	 * Setter for this Instance's position in the 3D world.
	 * @param pos the new 3D position of this Instance.
	 */
	public void setPosition(Point3D pos) {
		position = pos;
	}

	/**
	 * Getter for this Instance's rotation angle (y-axis).
	 * @return this Instance's rotation angle around the y-axis.
	 */
	public double getRotAngle() {
		return rotAngle;
	}

	/**
	 * Setter for this Instance's rotation angle (y-axis).
	 * @param angle the new rotation angle around the y-axis.
	 */
	public void setRotAngle(double angle) {
		rotAngle = angle;
	}

	/**
	 * Getter for this Instance's scale.
	 * @return the scale of this instance.
	 */
	public double getScale() {
		return scale;
	}

	/**
	 * Setter for this Instance's scale.
	 * @param scale the new scale for this Instance.
	 */
	public void setScale(double scale) {
		this.scale = scale;
	}

	/**
	 * Getter for this Instance's WireFrame model.
	 * @return the model of this Instance.
	 */
	public WireFrame getModel() {
		return model;
	}

	/**
	 * Setter for this Instance's Wireframe model.
	 * @param model the new model for this Instance.
	 */
	public void setModel(WireFrame model) {
		this.model = model;
	}
}
