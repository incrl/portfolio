package cs355.model.image;

/**
 * This class represents one color channel of an image.
 * It is package-visible for a reason. Do not make it public.
 * @author gavin
 */
class Channel {

	// The data for this Channel. It is one-dimensional
	// for efficiency, and the getters and setters handle
	// the conversion automatically.
	private final int[] pixels;

	// Obvious.
	private final int width;
	private final int height;

	/**
	 * Basic constructor that contructs a channel for
	 * an image of the provided width and height.
	 * @param width the image width.
	 * @param height the image height.
	 */
	public Channel(int width, int height) {
		pixels = new int[width * height];
		this.width = width;
		this.height = height;
		for (int i = 0; i < pixels.length; ++i) {
			pixels[i] = 255;
		}
	}

	/**
	 * Gets the data in this Channel at a particular pixel.
	 * @param x the x coordinate of the pixel.
	 * @param y the y coordinate of the pixel.
	 * @return the data in the Channel at the specified coordinates.
	 */
	public int getPixel(int x, int y) {
		validateBounds(x, y);
		return pixels[width * y + x];
	}

	/**
	 * Sets the data for a particular pixel in this Channel.
	 * @param x the x coordinate of the pixel.
	 * @param y the y coordinate of the pixel.
	 * @param data the new data for the pixel.
	 */
	public void setPixel(int x, int y, int data) {
		validateBounds(x, y);
		validateData(data);
		pixels[width * y + x] = data;
	}

	/**
	 * Validates coordinates from the user. Throws an Exception
	 * with an appropriate message if they are not valid.
	 * @param x the x coordinate to test.
	 * @param y the y coordinate to test.
	 */
	private void validateBounds(int x, int y) {
		if (x >= width) {
			throw new IndexOutOfBoundsException("Index is greater than the width of the image");
		}
		if (y >= height) {
			throw new IndexOutOfBoundsException("Index is greater than the height of the image");
		}
	}

	/**
	 * Validates data from the user. Throws an Exception
	 * with an appropriate message if it is not valid.
	 * @param data the data to test.
	 */
	private void validateData(int data) {
		if (data > 255) {
			throw new IllegalStateException("Value for image channel is greater than 255");
		}
		if (data < 0) {
			throw new IllegalStateException("Value for image channel is less than 0");
		}
	}

}
