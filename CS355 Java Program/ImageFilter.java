package cs355;

import java.io.File;
import javax.swing.filechooser.FileFilter;

/**
 * A FileFilter for image files (png and jpg).
 * @author gavin
 */
public class ImageFilter extends FileFilter {

	// The description of the file that this filter accepts.
	private static final String DESC = "Image Files";

	/**
	 * Decides whether to accept a file or not.
	 * @param file = the file to accept or reject.
	 * @return true on acceptance, false otherwise.
	 */
	@Override
	public boolean accept(File file) {

		// Make sure to include directories.
		if (file.isDirectory()) {
			return true;
		}

		// Test against all image types.
		String ext = FileUtils.getExtension(file);
		return (ext.equals(FileUtils.png) ||
				ext.equals(FileUtils.jpg) ||
				ext.equals(FileUtils.jpeg));
	}

	/**
	 * Returns a string description of the
	 * file type accept by this filter.
	 * @return the file type description.
	 */
	@Override
	public String getDescription() {
		return DESC;
	}

}
