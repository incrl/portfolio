package cs355;

import java.awt.Canvas;
import java.awt.Graphics;

/**
 * This is the color indicator.
 * @author Talonos
 */
class CS355SmallCanvas extends Canvas {

	private static final long serialVersionUID = -3990858344157396014L;

	/**
	 * Allows us to force the frame to recolor the indicator.
	 * @param graphics = required param for overload.
	 */
	@Override
	public void paint(Graphics graphics) {
		if (CS355Frame.isInitialized()) {
			CS355Frame.inst().setSelectedColor();
		}
	}
}
