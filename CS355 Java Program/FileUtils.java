package cs355;

import java.io.File;

/**
 *
 * @author gavin
 */
public class FileUtils {

	// Various file types that we use.
	public static final String png = "png";
	public static final String jpg = "jpg";
	public static final String jpeg = "jpeg";
	public static final String json = "json";
	public static final String scn = "scn";

	/**
	 * Get the extension of a file.
	 * @param f = the file whose extension we want.
	 * @return the extension of the file.
	 */
	public static String getExtension(File f) {

		// Grab the name and find the index of the extension.
		String name = f.getName();
		int i = name.lastIndexOf('.') + 1;

		// Error checking.
		if (i < 0 || i >= name.length()) {
			return null;
		}

		// We want all extensions in lowercase.
		return name.substring(i).toLowerCase();
	}
}
