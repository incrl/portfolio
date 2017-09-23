package cs355.model.image;

import java.awt.image.BufferedImage;
import java.awt.image.WritableRaster;
import java.io.File;
import java.io.IOException;
import java.util.Observable;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.imageio.ImageWriter;
import javax.imageio.stream.ImageOutputStream;

public abstract class CS355Image extends Observable {

	// The pixel data.
	private Channel[] pixels;

	// Obvious.
	private int width;
	private int height;

	/**
	 * A constructor that initialized a blank image.
	 */
	public CS355Image() {
		pixels = null;
		width = 0;
		height = 0;
	}

	/**
	 * A constructor that creates an Image of a certain size.
	 * It is initialized to default black.
	 * @param width the width of the image to create.
	 * @param height the height of the image to create.
	 */
	public CS355Image(int width, int height) {
		initPixels(width, height);
	}

	/**
	 * Called from the ViewRefresher to get a BufferedImage for drawing.
	 * I would suggest that you make this as efficient as possible, or
	 * maybe you could try to only call it when necessary.
	 * @return the BufferedImage that will be drawn to the screen.
	 */
	public abstract BufferedImage getImage();

	/**
	 * Called from the controller to do edge detection.
	 */
	public abstract void edgeDetection();

	/**
	 * Called from the controller to do a sharpen operation.
	 */
	public abstract void sharpen();

	/**
	 * Called from the controller to do color median blur.
	 */
	public abstract void medianBlur();

	/**
	 * Called from the controller to do uniform blur.
	 */
	public abstract void uniformBlur();

	/**
	 * Called from the controller to make the image grayscale.
	 */
	public abstract void grayscale();

	/**
	 * Called from the controller to change the contrast.
	 * @param amount the amount of contrast to add (could be negative).
	 */
	public abstract void contrast(int amount);

	/**
	 * Called from the controller to change the brightness.
	 * @param amount the amount of brightness to add (could be negative).
	 */
	public abstract void brightness(int amount);

	// Implemented methods.

	/**
	 * Sets the data in this image to be the
	 * same as the provided CS355Image. Be
	 * warned: this does a shallow copy.
	 * @param img the CS355Image to copy.
	 */
	public void setPixels(CS355Image img) {
		this.pixels = img.pixels;
		this.width = img.width;
		this.height = img.height;
	}

	/**
	 * Sets the pixels according to the BufferedImage.
	 * This basically initializes the image.
	 * @param bi the BufferedImage whose data we want.
	 */
	public void setPixels(BufferedImage bi) {

		// Initialize the members.
		initPixels(bi.getWidth(), bi.getHeight());

		// Get the raster.
		WritableRaster r = bi.getRaster();

		// An extra element, just in
		// case the image is ARGB.
		int[] rgb = new int[4];

		// Convert each pixel.
		for (int y = 0; y < height; ++y) {
			for (int x = 0; x < width; ++x) {

				// Get the pixel data from the raster.
				r.getPixel(x, y, rgb);

				// I'll use a loop here. This method
				// won't be called that often.
				for (int i = 0; i < 3; ++i) {
					pixels[i].setPixel(x, y, rgb[i]);
				}
			}
		}
	}

	/**
	 * Get all three channels from a particular pixel.
	 * @param x the x coordinate of the pixel.
	 * @param y the y coordinate of the pixel.
	 * @param data an array of 3+ ints to hold the data.
	 *			   If null or too small, an array will be
	 *			   allocated and returned. Otherwise, data
	 *			   will be filled and returned.
	 * @return the filled data array or a new allocated array.
	 */
	public int[] getPixel(int x, int y, int[] data) {

		// Validate or allocate the incoming array.
		if (data == null || data.length < 3) {
			data = new int[3];
		}

		// I didn't do a loop for efficiency. This method
		// will be used a lot in tight inner loops, and
		// quite frankly, a loop would add a fair bit of
		// overhead that we don't need.
		data[0] = pixels[0].getPixel(x, y);
		data[1] = pixels[1].getPixel(x, y);
		data[2] = pixels[2].getPixel(x, y);

		return data;
	}

	/**
	 * Set a pixel's channels with the provided data.
	 * This method doesn't care if the provided array
	 * has a length greater than 3, but it will throw
	 * an exception if the length is less.
	 * @param x the x coordinate of the pixel to set.
	 * @param y the y coordinate of the pixel to set.
	 * @param data the data to put in the channels.
	 */
	public void setPixel(int x, int y, int[] data) {

		// Validation!
		if (data.length < 3) {
			throw new IllegalArgumentException("Pixel data must have at least three channels");
		}

		// Again, no loop for efficiency.
		pixels[0].setPixel(x, y, data[0]);
		pixels[1].setPixel(x, y, data[1]);
		pixels[2].setPixel(x, y, data[2]);
	}

	/**
	 * Get the red of a particular pixel.
	 * @param x the x coordinate of the pixel.
	 * @param y the y coordinate of the pixel.
	 * @return the red of the pixel between 0 and 255.
	 */
	public int getRed(int x, int y) {
		return pixels[0].getPixel(x, y);
	}

	/**
	 * Set the red of a particular pixel.
	 * @param x the x coordinate of the pixel.
	 * @param y the y coordinate of the pixel.
	 * @param red the new red for the pixel.
	 */
	public void setRed(int x, int y, int red) {
		pixels[0].setPixel(x, y, red);
	}

	/**
	 * Get the green of a particular pixel.
	 * @param x the x coordinate of the pixel.
	 * @param y the y coordinate of the pixel.
	 * @return the green of the pixel between 0 and 255.
	 */
	public int getGreen(int x, int y) {
		return pixels[1].getPixel(x, y);
	}

	/**
	 * Set the green of a particular pixel.
	 * @param x the x coordinate of the pixel.
	 * @param y the y coordinate of the pixel.
	 * @param green the new green for the pixel.
	 */
	public void setGreen(int x, int y, int green) {
		pixels[1].setPixel(x, y, green);
	}

	/**
	 * Get the blue of a particular pixel.
	 * @param x the x coordinate of the pixel.
	 * @param y the y coordinate of the pixel.
	 * @return the blue of the pixel between 0 and 255.
	 */
	public int getBlue(int x, int y) {
		return pixels[2].getPixel(x, y);
	}

	/**
	 * Set the blue of a particular pixel.
	 * @param x the x coordinate of the pixel.
	 * @param y the y coordinate of the pixel.
	 * @param blue the new blue for the pixel.
	 */
	public void setBlue(int x, int y, int blue) {
		pixels[2].setPixel(x, y, blue);
	}

	/**
	 * Get the width of the image.
	 * @return the width of the image.
	 */
	public int getWidth() {
		return width;
	}

	/**
	 * Get the height of the image.
	 * @return the height of the image.
	 */
	public int getHeight() {
		return height;
	}

	/**
	 * Opens an image file and converts it to the in-memory format.
	 * @param f the file to open.
	 * @return true if successful, false otherwise.
	 */
	public boolean open(File f) {

		BufferedImage img = null;
		try {
			// Read the file in.
			img = javax.imageio.ImageIO.read(f);

			// Complain if necessary.
			if (img == null) {
				throw new IOException("Unable to read image");
			}
		}
		catch (IOException ex) {
			Logger.getLogger(CS355Image.class.getName()).log(Level.SEVERE, null, ex);
			return false;
		}

		// Convert.
		setPixels(img);

		// Notify observers. Let this be an example to you.
		this.setChanged();
		this.notifyObservers();

		return true;
	}

	/**
	 * Saves an image file out to disk.
	 * @param f the file to save to.
	 * @return true if successful, false otherwise.
	 */
	public boolean save(File f) {

		// Figure out which image type it is.
		int dot = f.getName().lastIndexOf('.');
		String suffix = f.getName().substring(dot + 1);
		ImageWriter writer = javax.imageio.ImageIO.getImageWritersBySuffix(suffix).next();

		// Get the BufferedImage that
		// we'll write out to disk.
		BufferedImage img = this.getImage();

		// Write out the image.
		try (ImageOutputStream out = javax.imageio.ImageIO.createImageOutputStream(f)) {
			writer.setOutput(out);
			writer.write(img);
		}
		catch (IOException ex) {
			Logger.getLogger(CS355Image.class.getName()).log(Level.SEVERE, null, ex);
			return false;
		}

		return true;
	}

	/**
	 * A helper method to allocate the pixel data.
	 * @param width the width of the image to allocate.
	 * @param height the height of the image to allocate.
	 */
	private void initPixels(int width, int height) {

		// Standard assignments.
		this.width = width;
		this.height = height;

		// Create the channels.
		pixels = new Channel[] { new Channel(width, height),
								 new Channel(width, height),
								 new Channel(width, height) };
	}
}
