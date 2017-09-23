package cs355.model.scene;

import java.io.File;
import java.util.ArrayList;
import java.util.Observable;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 * The Scene that you will render as a 3D overlay.
 * @author gavin
 */
public class CS355Scene extends Observable {

	// The list of Instances.
	private ArrayList<Instance> insts;

	// The default camera items.
	private Point3D camPos;
	private double camRot;

	/**
	 * Creates an empty Scene with no Instances.
	 */
	public CS355Scene() {
		insts = new ArrayList<>();
		camPos = new Point3D();
		camRot = 0.0;
	}

	/**
	 * Open a file and create a scene from it.
	 * This uses SceneParser to parse the file.
	 * @param f the file to open.
	 * @return true if successful, false otherwise.
	 */
	public boolean open(File f) {

		try {
			// Pass it to the SceneParser.
			SceneParser sp = new SceneParser(f);
			CS355Scene s = sp.parse();

			// Populate the object with the new data.
			this.camPos = s.camPos;
			this.camRot = s.camRot;
			this.insts = s.insts;
		}
		catch (Exception ex) {
			Logger.getLogger(CS355Scene.class.getName()).log(Level.SEVERE, null, ex);
			return false;
		}

		return true;
	}

	/**
	 * Gets the list of Instances in the scene.
	 * @return the list of Instances in the scene.
	 */
	public ArrayList<Instance> instances() {
		return insts;
	}

	/**
	 * Get the default camera position.
	 * @return the position of the default camera.
	 */
	public Point3D getCameraPosition() {
		return camPos;
	}

	/**
	 * Sets the camera default position.
	 * @param pos the default position for the camera.
	 */
	public void setCameraPosition(Point3D pos) {
		camPos = pos;
	}

	/**
	 * Get the rotation angle of the default camera.
	 * @return the rotation angle of the default camera.
	 */
	public double getCameraRotation() {
		return camRot;
	}

	/**
	 * Sets the camera's rotation.
	 * @param rot the new rotation for the camera.
	 *			  This is normalized.
	 */
	public void setCameraRotation(double rot) {
		camRot = normalizeRot(rot);
	}

	/**
	 * Normalizes an angle to be between 0 and 360.
	 * @param rot the angle to normalize;
	 * @return the normalized angle.
	 */
	private double normalizeRot(double rot) {

		// While the rotation is less than 0...
		while (rot < 0.0) {

			// Add 360 to the rotation.
			rot += 360.0;
		}

		// While the rotation is greater than 360...
		while (rot >= 360.0) {

			// Subtract 360 from the rotation.
			rot -= 360.0;
		}

		return rot;
	}
}
