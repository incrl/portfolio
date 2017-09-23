package cs355.model.scene;

import java.util.ArrayList;
import java.util.List;

/**
 * A simple class that just holds
 * a list of Line3D objects.
 */
public class WireFrame {

	// This is the list of Line3D's that make this WireFrame.
	// This can be final, thank goodness.
	private final ArrayList<Line3D> lines;

	/**
	 * Basic constructor. Makes an empty list of lines.
	 */
	public WireFrame() {
		lines = new ArrayList<>();
	}

	/**
	 * Basic constructor. Sets the list of lines to the provided one.
	 * @param lines the list of lines that make up the new WireFrame.
	 */
	public WireFrame(ArrayList<Line3D> lines) {
		this.lines = lines;
	}

	/**
	 * Get the list of lines.
	 * @return the list of Line3D objects.
	 */
	public List<Line3D> getLines() {
		return lines;
	}
}
