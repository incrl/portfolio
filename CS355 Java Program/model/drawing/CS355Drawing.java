package cs355.model.drawing;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonSyntaxException;
import cs355.JsonShape;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Observable;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 * This is the abstract base class for the model.
 * Make sure your model implements and extends
 * this. Also <b>MAKE SURE YOU STORE SHAPES IN
 * BACK-TO-FRONT ORDER!</b> That means that the
 * shape in the very back should be at index 0.
 */
public abstract class CS355Drawing extends Observable {

	// This is used to write out shapes to JSON.
	// The call to registerTypeAdapter() is essential
	// for allowing us to distinguish between shapes.
	// Also, we want pretty indenting.
	private static final Gson gson = new GsonBuilder().setPrettyPrinting()
			.registerTypeAdapter(Shape.class, new JsonShape()).create();

	/**
	 * Get a shape at a certain index.
	 * @param index = the index of the desired shape.
	 * @return the shape at the provided index.
	 */
	public abstract Shape getShape(int index);

	// Adding and deleting.

	/**
	 * Add a shape to the <b>FRONT</b> of the list.
	 * @param s = the shape to add.
	 * @return the index of the shape.
	 */
	public abstract int addShape(Shape s);

	/**
	 * Delete the shape at a certain index.
	 * @param index = the index of the shape to delete.
	 */
	public abstract void deleteShape(int index);

	// Moving commands.

	/**
	 * Move the shape at a certain index to the front of the list.
	 * @param index = the index of the shape to move to the front.
	 */
	public abstract void moveToFront(int index);

	/**
	 * Move the shape at a certain index to the back of the list.
	 * @param index = the index of the shape to move to the back.
	 */
	public abstract void movetoBack(int index);

	/**
	 * Move the shape at a certain index forward one slot.
	 * @param index = the index of the shape to move forward.
	 */
	public abstract void moveForward(int index);

	/**
	 * Move the shape at a certain index backward one slot.
	 * @param index = the index of the shape to move backward.
	 */
	public abstract void moveBackward(int index);

	// Whole list operations.

	/**
	 * Get the list of the shapes in this model.
	 * @return the list of shapes.
	 */
	public abstract List<Shape> getShapes();

	/**
	 * Get the reversed list of the shapes in this model.
	 * This is for doing click tests (front first).
	 * @return the reversed list of shapes.
	 */
	public abstract List<Shape> getShapesReversed();

	/**
	 * Sets the list of shapes in this model.
	 * This should overwrite the current list.
	 * @param shapes = the new list of shapes
	 *				   for the model.
	 */
	public abstract void setShapes(List<Shape> shapes);

	// Implemented methods.

	/**
	 * Opens a drawing from a Json file and populate
	 * this drawing with the shapes in that file.
	 * @param f = the handle of the file to open.
	 * @return true if successful, false otherwise.
	 */
	public boolean open(File f) {

		// Make a blank list.
		List<Shape> shapes = null;

		try {
			// Read the entire file in. I hate partial I/O.
			byte[] b = Files.readAllBytes(f.toPath());

			// Validation.
			if (b == null) {
				throw new IOException("Unable to read drawing");
			}

			// Convert it to text.
			String data = new String(b, StandardCharsets.UTF_8);

			// Use Gson to convert the text to a list of Shapes.
			Shape[] list = gson.fromJson(data, Shape[].class);
			shapes = new ArrayList<>(Arrays.asList(list));
		}
		catch (IOException | JsonSyntaxException ex) {
			Logger.getLogger(CS355Drawing.class.getName()).log(Level.SEVERE, null, ex);
			return false;
		}

		// Set the new shape list.
		setShapes(shapes);

		return true;
	}

	/**
	 * Save out this drawing's list of shapes to a
	 * Json file.
	 * @param f = the file to save to.
	 * @return true if successful, false otherwise.
	 */
	public boolean save(File f) {
		try (FileOutputStream fos = new FileOutputStream(f)) {

			// Get the list from the concrete class.
			List<Shape> data = getShapes();

			// Convert the List to an array.
			Shape[] shapes = new Shape[data.size()];
			data.toArray(shapes);

			// Convert to JSON text and write it out.
			String json = gson.toJson(shapes, Shape[].class);
			fos.write(json.getBytes());
		}
		catch (IOException ex) {
			Logger.getLogger(CS355Drawing.class.getName()).log(Level.SEVERE, null, ex);
			return false;
		}

		return true;
	}
}
