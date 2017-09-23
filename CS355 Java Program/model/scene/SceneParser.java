package cs355.model.scene;

import java.awt.Color;
import java.io.File;
import java.io.FileInputStream;
import java.util.ArrayList;
import java.util.Scanner;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author gavin
 */
public class SceneParser {

	// Valid options for a camera (eye).
	private static final char[] EYE_OPTS = { 'r', 't' };

	// Valid options for an instance.
	private static final char[] INST_OPTS = { 'c', 'r', 's', 't' };

	// The file that will be parsed.
	private final File file;

	/**
	 * Basic constructor.
	 * @param file = the file to be parsed.
	 */
	public SceneParser(File file) {
		this.file = file;
	}

	/**
	 * Parse the file and build a scene from it.
	 * This method will use the ObjParser to open
	 * and parse .obj files, which are how we
	 * store models.
	 * @return the newly created scene.
	 * @throws java.lang.Exception when the file is invalid.
	 */
	public CS355Scene parse() throws Exception {

		// Build the scene and needed lists.
		CS355Scene scene = new CS355Scene();
		ArrayList<InstParse> pairs = new ArrayList<>();
		ArrayList<WireFrame> models = new ArrayList<>();

		try (Scanner s = new Scanner(file)) {

			String line;

			// While there is input on the scanner...
			while (s.hasNextLine()) {

				// Grab the next line.
				line = s.nextLine();

				// Valid lines have to be greater than 0 chars long.
				if (line.length() < 1) {
					continue;
				}

				// Find out what type of line we're parsing.
				switch (line.charAt(0)) {
					case 'c':
						throw new IllegalStateException("Color defined in root of scene description");
					case 'e':
						EyeParse eye = parseEye(line, s);
						scene.setCameraPosition(eye.pos);
						scene.setCameraRotation(eye.angle);
						break;
					case 'i':
						pairs.add(parseInstance(line, s));
						break;
					case 'o':
						models.add(parseObj(line));
						break;
					case 'r':
						throw new IllegalStateException("Rotation defined in root of scene description");
					case 's':
						throw new IllegalStateException("Scale defined in root of scene description");
					case 't':
						throw new IllegalStateException("Position defined in root of scene description");
					default:
				}
			}
		}
		catch(Exception ex) {
			Logger.getLogger(SceneParser.class.getName()).log(Level.SEVERE, null, ex);
			Exception e = new Exception("Invalid scene description", ex);
			throw e;
		}

		Instance inst;
		int i;

		// Resolve object indices into the appropriate Instances.
		for (InstParse ip : pairs) {
			i = ip.idx;

			// This would be an invalid index.
			if (i >= models.size()) {
				throw new IllegalStateException("Invalid object index");
			}

			// Set the Instance's model and add it to the scene.
			inst = ip.inst;
			inst.setModel(models.get(i));
			scene.instances().add(inst);
		}

		return scene;
	}

	/**
	 * Parse a color from one line of text.
	 * @param line = the line of text to parse.
	 * @return the resulting color as INT_RGB.
	 */
	private Color parseColor(String line) {

		// Split the line on whitespace.
		String[] elems = line.split("\\s+");

		// Create a default color.
		int[] rgb = new int[3];
		rgb[0] = rgb[1] = rgb[2] = 255;

		// Error checking.
		if (elems.length != 4) {
			throw new IllegalStateException("Invalid color");
		}

		// Iterate over the split line and parse the integers.
		// Remember that the first element is the char at the
		// beginning of the line, so we skip that one.
		for (int i = 0; i < 3; ++i) {
			rgb[i] = Integer.parseInt(elems[i + 1]);
		}

		return new Color(rgb[0], rgb[1], rgb[2]);
	}

	/**
	 * Parse a rotation (angle and vector) from one
	 * line of text.
	 * @param line = the line of text to parse.
	 * @return the angle to rotate as a double. The
	 *		   rotation vector is implicitly [0, 1, 0].
	 */
	private double parseRotation(String line) {

		// Split the line on whitespace.
		String[] elems = line.split("\\s+");

		// Error checking.
		if (elems.length != 2) {
			throw new IllegalStateException("Invalid rotation");
		}

		// Pull the double angle out of the split line.
		// Remember that the first element is the char
		// at the beginning, so we skip that one.
		return Double.parseDouble(elems[1]);
	}

	/**
	 * Parse a point from one line of text.
	 * @param line = the line of text to parse.
	 * @return the resulting Point3D.
	 */
	private Point3D parsePosition(String line) {

		// Split the line on whitespace.
		String[] elems = line.split("\\s+");

		// Error checking.
		if (elems.length != 4) {
			throw new IllegalStateException("Invalid rotation");
		}

		// Pull the various elements out of the split line.
		// Remember that the first element is the char at
		// the beginning, so we skip that one.
		double x = Double.parseDouble(elems[1]);
		double y = Double.parseDouble(elems[2]);
		double z = Double.parseDouble(elems[3]);

		return new Point3D(x, y, z);
	}

	/**
	 * Parse a .obj file to create a WireFrame.
	 * @param line = the line of text to parse.
	 *				 We only need the filename.
	 * @return the WireFrame parsed from the file.
	 * @throws Exception if the .obj file is invalid.
	 */
	private WireFrame parseObj(String line) throws Exception {

		// Find the starting index of the filename.
		int i = 1;
		char c = line.charAt(i);
		while (c != '"') {
			c = line.charAt(++i);
		}
		++i;

		// Get the filename.
		String name = line.substring(i, line.indexOf('"', i + 1));

		// The filename is relative, so we need to
		// use the parent file to resolve it.
		File f = new File(file.getParentFile(), name);

		// Parse the thing.
		ObjParser op = new ObjParser(new FileInputStream(f));
		return op.parse();
	}

	/**
	 * Parse a camera position and orientation from some lines of text.
	 * This will continue parsing more lines, not just its own. That's
	 * because the eye has position <i>and</i> rotation.
	 * @param line = the first line of text to parse.
	 * @param s = the scanner (we may need more lines).
	 * @return the parsed camera position and orientation.
	 */
	private EyeParse parseEye(String line, Scanner s) {

		// Create a default eye.
		EyeParse eye = new EyeParse();

		// While there is input *and* the
		// input is valid for the eye...
		while (s.hasNextLine() && nextIsValid(s, EYE_OPTS)) {

			// Grab the next line.
			line = s.nextLine();

			// Valid lines are greater than 2 chars long.
			if (line.length() <= 2) {
				continue;
			}

			// Figure out what kind of line
			// it is and act accordingly.
			switch (line.charAt(0)) {
				case 'r':
					eye.angle = parseRotation(line);
					break;
				case 't':
					eye.pos = parsePosition(line);
					break;
			}
		}

		return eye;
	}

	/**
	 * Parse an instance from some lines of text. This
	 * will continue parsing more lines, not just its
	 * own. That's because an instance has position,
	 * rotation, color, a model, and scale.
	 * @param line = the first line of text to parse.
	 * @param s = the Scanner with more input.
	 * @return an InstParse that we'll use later to
	 *		   resolve the reference to a WireFrame.
	 */
	private InstParse parseInstance(String line, Scanner s) {

		// Create a default instance.
		Instance inst = new Instance();

		// Split the first line on whitespace.
		String[] elems = line.split("\\s+");

		// Error checking.
		if (elems.length != 2) {
			throw new IllegalStateException("Invalid instance declaration");
		}

		// Get the WireFrame index from the line.
		int index = Integer.parseInt(elems[1]) - 1;

		// While we have valid input.
		while (s.hasNextLine() && nextIsValid(s, INST_OPTS)) {
			line = s.nextLine();
			if (line.length() <= 2) {
				continue;
			}

			// Figure out what kind of line
			// it is and act accordingly.
			switch (line.charAt(0)) {
				case 'c':
					inst.setColor(parseColor(line));
					break;
				case 'r':
					inst.setRotAngle(parseRotation(line));
					break;
				case 's':
					elems = line.split("\\s+");
					if (elems.length != 2) {
						throw new IllegalStateException("Invalid scale");
					}
					inst.setScale(Double.parseDouble(elems[1]));
					break;
				case 't':
					inst.setPosition(parsePosition(line));
					break;
			}
		}

		return new InstParse(inst, index);
	}

	/**
	 * Figures out if the next line of input is valid
	 * for the current parse situation. It does so
	 * <i>without</i> advancing the Scanner, which
	 * is very important.
	 * @param s = the Scanner with the input.
	 * @param options = the valid options.
	 * @return true if the next line has valid
	 *		   input, false otherwise.
	 */
	private boolean nextIsValid(Scanner s, char[] options) {

		// Set up the flag.
		boolean valid = false;

		// Loop over the options and test each.
		for (int i = 0; !valid && i < options.length; ++i) {
			valid = s.hasNext(options[i] + ".*");
		}

		return valid;
	}

	/**
	 * Small class that lets us resolve references
	 * to WireFrames at the end of parsing.
	 */
	private class InstParse {

		// The instance.
		public Instance inst;

		// Index of the Instance's WireFrame.
		public int idx;

		public InstParse(Instance inst, int idx) {
			this.inst = inst;
			this.idx = idx;
		}
	}

	/**
	 * Small class that allows me to parse the default camera.
	 */
	private class EyeParse {

		// The position of the camera.
		public Point3D pos;

		// The rotation angle (around [0, 1, 0]).
		public double angle;

		public EyeParse() {
			this.pos = new Point3D();
			this.angle = 0.0;
		}
	}
}
