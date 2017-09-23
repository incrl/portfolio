package cs355.view;

import java.awt.Graphics2D;
import java.util.Observer;

/**
 * This is the interface for the view. Make
 * sure your view implements this interface.
 */
public interface ViewRefresher extends Observer {

	/**
	 * Called when the view needs to be redrawn.
	 * @param g2d = the Graphics2D object to draw with.
	 */
	void refreshView(Graphics2D g2d);
}
