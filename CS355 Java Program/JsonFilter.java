package cs355;

import java.io.File;
import javax.swing.filechooser.FileFilter;

/**
 * A FileFilter for .json files.
 * @author gavin
 */
public class JsonFilter extends FileFilter {

	// The description of the file that this filter accepts.
	private static final String DESC = "JSON Files (*.json)";

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

		// Test for the .json extension.
		return FileUtils.getExtension(file).equals(FileUtils.json);
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
