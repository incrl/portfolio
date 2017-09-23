package cs355;

import java.io.File;
import javax.swing.filechooser.FileFilter;

/**
 * A FileFilter for .scn files.
 * @author gavin
 */
public class SceneFilter extends FileFilter {

	// The description of the file that this filter accepts.
	private static final String DESC = "Scene description files (*.scn)";

	/**
	 * Decides whether to accept a file or not.
	 * @param f = the file to accept or reject.
	 * @return true on acceptance, false otherwise.
	 */
	@Override
	public boolean accept(File f) {

		// Compare against the file extension we're looking for.
		// Make sure to include directories.
		return f.isDirectory() || FileUtils.getExtension(f).equals(FileUtils.scn);
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
