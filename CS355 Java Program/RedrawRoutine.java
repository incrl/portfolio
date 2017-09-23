package cs355;

import cs355.view.ViewRefresher;
import java.awt.Canvas;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.GraphicsConfiguration;
import java.awt.GraphicsDevice;
import java.awt.GraphicsEnvironment;
import java.awt.image.BufferStrategy;
import java.awt.image.BufferedImage;
import java.util.concurrent.Semaphore;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 * A set of logic for redrawing the screen. Underneath the hood, this is
 * using double buffering and timing to draw as predictably as possible.
 * @author Talonos
 */
class RedrawRoutine implements Runnable {

	// Things used to draw.
	private Canvas screenCanvas;
	private BufferStrategy buffer;
	private Graphics2D g2d;
	private Graphics graphics;
	private BufferedImage bufImage;
	private GraphicsConfiguration gc;

	// The student's ViewRefresher.
	ViewRefresher viewRefresher;

    // If you ever need to make sure the view is not being redrawn
	// while you do work under the hood, you can use this semaphore.
	public Semaphore isDrawing = new Semaphore(1);

	// Private constants.
	private static final double FRAME_TIME = 200;

	// We don't want the user to have direct access to this class.
	private static RedrawRoutine instance;

	/**
	 * Grab the instance. Creates one if it doesn't exist.
	 * @return the current instance of this class.
	 */
	public static RedrawRoutine inst() {
		if (instance == null) {
			instance = new RedrawRoutine();
		}
		return instance;
	}

	/**
	 * Apparently, we don't need to do anything here.
	 */
	private RedrawRoutine() {
        // Set up the drawing area.
		// screenCanvas.setIgnoreRepaint(true);
	}

	/**
	 * Initialize with a Canvas and ViewRefresher.
	 * @param s = the canvas to draw to.
	 * @param v = the student's ViewRefresher
	 *			  that will control drawing.
	 */
	public void initialize(Canvas s, ViewRefresher v) {

		// Initialize fields.
		viewRefresher = v;
		screenCanvas = s;

		// Set double buffering and grab the resulting buffer.
		screenCanvas.createBufferStrategy(2);
		buffer = screenCanvas.getBufferStrategy();

		// Make sure we set the correct GraphicsConfiguration.
		GraphicsEnvironment ge = GraphicsEnvironment.getLocalGraphicsEnvironment();
		GraphicsDevice gd = ge.getDefaultScreenDevice();
		gc = gd.getDefaultConfiguration();
	}

	/**
	 * This is the drawing loop.
	 */
	@Override
	public void run() {
		double time = System.currentTimeMillis();
		try {
			isDrawing.acquire();
		}
		catch (InterruptedException ex) {
			Logger.getLogger(RedrawRoutine.class.getName()).log(Level.SEVERE, null, ex);
			System.exit(-1);
		}

		// Actual drawing loop.
		while (true) {
			try {
                // Make sure that if all else fails, you sleep for at least a millisecond
				// to let the other logic run.
				isDrawing.release();
				Thread.sleep(1l);
				if (time < FRAME_TIME) {
					Thread.sleep((long) (FRAME_TIME - time));
				}
				// When game logic relenquishes control, move forward.
				isDrawing.acquire();

				// Refresh the page, making sure to count how long it takes.
				time = System.currentTimeMillis();
				refreshView();
				time = System.currentTimeMillis() - time;

                // Display the time. Commented out, but you can see how long it
				// takes to render a frame by uncommenting the following line:
                // g2d.drawString(""+time, 10, 10);

				// Draw the image to the buffer.
				graphics = buffer.getDrawGraphics();
				graphics.drawImage(bufImage, 0, 0, null);

                // I don't know what this is for, but it's important.
				// I got it from sample code online, and still need
				// to figure out what this code's purpose is.
				if (!buffer.contentsLost()) {
					buffer.show();
				}
			}
			catch (InterruptedException ex) {
				Logger.getLogger(RedrawRoutine.class.getName()).log(Level.SEVERE, null, ex);
			}
		}
	}

	/**
	 * Refreshes the view. It does this by calling the
	 * refresh method on the provided ViewRefresher.
	 * @return the BufferedImage that the Graphics2d drew on.
	 *		   Used for the "Save Picture" option.
	 */
	public BufferedImage refreshView() {

		// Get an image, and the graphics of that image.
		bufImage = gc.createCompatibleImage(screenCanvas.getWidth(), screenCanvas.getHeight());
		g2d = bufImage.createGraphics();
		viewRefresher.refreshView(g2d);

		// Draw the image to the buffer.
		graphics = buffer.getDrawGraphics();
		graphics.drawImage(bufImage, 0, 0, null);

        // I don't know what this is for, but it's important. I
		// got it from sample code online, and still need to figure out
		// what this code's purpose is.
		if (!buffer.contentsLost()) {
			buffer.show();
		}

		return bufImage;
	}
}
