package cs355;

import java.awt.Canvas;
import java.awt.Graphics;

/**
 * Allows us to send paint calls to the student's code.
 * @author Talonos
 */
class CS355Canvas extends Canvas {

	private static final long serialVersionUID = -5026275619826889323L;

	/**
	 * Sends the paint call to the student's code via RedrawRoutine.
	 * @param graphics = the required Graphics object for the override.
	 */
	@Override
	public void paint(Graphics graphics) {
		if (CS355Frame.isInitialized()) {
			RedrawRoutine.inst().refreshView();
		}
	}
}
