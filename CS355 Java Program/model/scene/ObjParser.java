package cs355.model.scene;

import java.io.FileInputStream;
import java.util.ArrayList;
import java.util.Scanner;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 * A parser for .obj files.
 * @author gavin
 */
public class ObjParser {

	// The input stream that we'll pull from.
	private final FileInputStream fs;

	/**
	 * Simple constructor. Sets the one field.
	 * @param fs the FileInputStream that we'll get input from.
	 */
	public ObjParser(FileInputStream fs) {
		this.fs = fs;
	}

	/**
	 * Parses the obj file.
	 * @return the resulting WireFrame.
	 * @throws Exception when the file is invalid in any way.
	 */
	public WireFrame parse() throws Exception {

		// Various lists that we'll need.
		ArrayList<Point3D> verts = new ArrayList<>();
		ArrayList<int[]> faces = new ArrayList<>();
		ArrayList<Integer> lineIndices = new ArrayList<>();

		// Create a Scanner on the input.
		try (Scanner s = new Scanner(fs)) {
			String line;

			// While there are more lines...
			while (s.hasNextLine()) {

				// Get a line.
				line = s.nextLine();

				// Make sure the line is valid.
				if (line.length() <= 2) {
					continue;
				}

				// Figure out what kind of line it is
				// and do the appropriate parse.
				switch (line.charAt(0)) {
					case 'f':
						faces.add(parseFace(line));
						break;
					case 'l':
						int[] indices = parseLine(line);
						for (int i : indices) {
							lineIndices.add(i);
						}
						break;
					case 'v':
						if (line.charAt(1) == ' ') {
							verts.add(parseVert(line));
						}
						break;
					default:
				}
			}
		}
		catch(Exception ex) {
			Exception e = new Exception("Invalid .obj file", ex);
			Logger.getLogger(SceneParser.class.getName()).log(Level.SEVERE, null, e);
			throw e;
		}

		// Various needed variables.
		ArrayList<Line3D> lines = new ArrayList<>();
		Point3D pt1, pt2;
		int i1, i2;

		// Go over the lineIndices ArrayList and create the lines.
		for (int i = 0; i < lineIndices.size() - 1; i += 2) {

			// Get the indices.
			i1 = lineIndices.get(i);
			i2 = lineIndices.get(i + 1);

			// Throw up if they're invalid.
			if (i1 >= verts.size() || i2 >= verts.size()) {
				throw new IllegalStateException("Invalid vertex index on a line");
			}

			// Get the two vertices and create a line from them.
			pt1 = verts.get(i1);
			pt2 = verts.get(i2);
			lines.add(new Line3D(pt1, pt2));
		}

		// Needed for the next phase.
		int next;

		// Now get the lines from the faces.
		for (int[] list : faces) {

			// Loop over every line in the face.
			for (int i = 0; i < list.length; ++i) {
				next = i < list.length - 1 ? i + 1 : 0;

				// Throw up if invalid.
				if (list[i] >= verts.size() || list[next] >= verts.size()) {
					throw new IllegalStateException("Invalid vertex index on a face");
				}

				// Get the vertices and create a line.
				pt1 = verts.get(list[i]);
				pt2 = verts.get(list[next]);
				lines.add(new Line3D(pt1, pt2));
			}
		}

		return new WireFrame(lines);
	}

	/**
	 * Parses a face.
	 * @param line the line of input with the vertices' indices.
	 * @return a list of vertex indices.
	 */
	private int[] parseFace(String line) {

		// Split the line on whitespace.
		String[] elems = line.split("\\s+");
		String[] subs;

		// Throw up if invalid.
		if (elems.length < 4) {
			throw new IllegalStateException("Invalid face; not enough vertices");
		}

		// Create a list of indices with the right size.
		int[] indices = new int[elems.length - 1];

		// Loop over the elements in the line (except for the first,
		// which is the 'f' character), and get the indices.
		for (int i = 0; i < indices.length; ++i) {

			// Make sure to split on slashes (see .obj format).
			subs = elems[i + 1].split("/+");

			// Throw up if invalid.
			if (subs.length == 0) {
				throw new IllegalStateException("Invalid face; no reference to vertex");
			}

			// Parse the first integer, which should be the index.
			indices[i] = Integer.parseInt(subs[0]) - 1;
		}

		return indices;
	}

	/**
	 * Parse a vertex.
	 * @param line the line of input with the vertex.
	 * @return the vertex as a Point3D.
	 */
	private Point3D parseVert(String line) {

		// Allocate coordinates and split the line on whitespace.
		double[] coords = new double[3];
		String[] elems = line.split("\\s+");

		// Throw up if invalid.
		if (elems.length != 4) {
			throw new IllegalStateException("Invalid point");
		}

		// Loop over the coordinates in the line and parse them.
		for (int i = 0; i < 3; ++i) {
			coords[i] = Double.parseDouble(elems[i + 1]);
		}

		return new Point3D(coords[0], coords[1], coords[2]);
	}

	/**
	 * Parses a line (two vertices).
	 * @param line the line of input to parse.
	 * @return the line as two vertex indices.
	 */
	private int[] parseLine(String line) {

		// Allocate a list of indices and split the line on whitespace.
		int[] indices = new int[2];
		String[] elems = line.split("\\s+");

		// Throw up if invalid.
		if (elems.length != 3) {
			throw new IllegalStateException("Invalid line");
		}

		// Parse the indices.
		for (int i = 0; i < 2; ++i) {
			indices[i] = Integer.parseInt(elems[i + 1]) - 1;
		}

		return indices;
	}
}
