package cs355.model.image;

import java.awt.Color;
import java.awt.image.BufferedImage;
import java.util.Arrays;

import cs355.GUIFunctions;

public class Image extends CS355Image {

	
	
	@Override
	public BufferedImage getImage() {
		
		int width = super.getWidth();
		int height = super.getHeight();
		
		BufferedImage result = new BufferedImage(width,height,BufferedImage.TYPE_INT_RGB);
		
		for(int i=0; i<width; i++){
			for(int j=0; j<height; j++) {
				
				int[] rgb = new int[3];
				rgb = super.getPixel(i, j, rgb);
				//Get the color as a single integer
				int color = (rgb[0] << 16) | (rgb[1] << 8) | rgb[2];
				result.setRGB(i, j, color);
			}
		}
		
		return result;
	}

	@Override
	public void edgeDetection() {
		int width = super.getWidth();
		int height = super.getHeight();
		
		// Preallocate the arrays.
		int[] rgb = new int[3];
		float[] hsb = new float[3];
		float[][] result = new float[width][height];
		
		for(int i=1; i<width-1; i++){
			for(int j=1; j<height-1; j++) {
				
				float total = 0;
				float result_x = 0;
				float result_y = 0;
				
				//Apply the kernel for the x direction
				for(int x = -1; x<=1; x+=2) {
					for(int y = -1; y<=1; y++) {
						
						super.getPixel(i+x,j+y,rgb);
						
						// Convert to HSB.
						Color.RGBtoHSB(rgb[0], rgb[1], rgb[2], hsb);
						
						//Work in brightness
						if(y == 0)
							total += 2*hsb[2]*x;
						else
							total += hsb[2]*x;
					}
				}
				
				result_x = total/8;
				
				
				total = 0;
				
				//Apply the kernel for the y direction
				for(int y = -1; y<=1; y+=2) {
					for(int x = -1; x<=1; x++) {
						
						super.getPixel(i+x,j+y,rgb);
						
						// Convert to HSB.
						Color.RGBtoHSB(rgb[0], rgb[1], rgb[2], hsb);
						
						//Work in brightness
						if(x == 0)
							total += 2*hsb[2]*y;
						else
							total += hsb[2]*y;
					}
				}
				
				result_y = total/8;
				
				//Put the gradient magnitude into result
				result[i][j] = (float) Math.sqrt(Math. pow(result_x, 2) + Math.pow(result_y,2));
			}
		}
		
		//Set the original image with the values in the result buffer
		for(int i=1; i<width-1; i++){
			for(int j=1; j<height-1; j++) {
			
				//Put back into rgb value
				int v = (int) (result[i][j]*255);
				int[] pixel = {v, v, v};
				
				super.setPixel(i, j, pixel);
			
			}
		}
	}

	@Override
	public void sharpen() {
		int width = super.getWidth();
		int height = super.getHeight();
		
		// Preallocate the arrays.
		int[] rgb = new int[3];
		
		int[][][] result = new int[width][height][3];
		
		for(int i=1; i<width-1; i++){
			for(int j=1; j<height-1; j++) {
				
				int[] total = {0,0,0};
				
				//Apply the kernel
				for(int x = -1; x<=1; x+=2) {
					for(int y = -1; y<=1; y+=2) {
						
						super.getPixel(i+x,j+y,rgb);
						
						total[0] -= rgb[0];
						total[1] -= rgb[1];
						total[2] -= rgb[2];
						
					}
				}
				
				//Grab the central pixel
				super.getPixel(i, j, rgb);
				
				total[0] += 6*rgb[0];
				total[1] += 6*rgb[1];
				total[2] += 6*rgb[2];
				
				
				int[] normal = new int[3];
				
				//Normalize the pixel values and make sure the y are in range
				normal[0] = (int)Math.min(Math.max((total[0]/2.0),0),255);
				normal[1] = (int)Math.min(Math.max((total[1]/2.0),0),255);
				normal[2] = (int)Math.min(Math.max((total[2]/2.0),0),255);

				// Set the pixel.
				result[i][j][0] =  normal[0];
				result[i][j][1] =  normal[1];
				result[i][j][2] =  normal[2];
			}
		}
		
		//Set the original image with the values in the result buffer
		for(int i=1; i<width-1; i++){
			for(int j=1; j<height-1; j++) {
			
				super.setPixel(i, j, result[i][j]);
			
			}
		}
		
		//Set the edges with zeros
		int[] z = {0,0,0};
		for(int i=0; i<width; i++){
			super.setPixel(i, 0, z);
			super.setPixel(i, height-1, z);
		}
		for(int j=0; j<height; j++){
			super.setPixel(0, j, z);
			super.setPixel(width-1, j, z);
		}
	}

	@Override
	public void medianBlur() {
		int width = super.getWidth();
		int height = super.getHeight();
		
		// Preallocate the arrays.
		int[] rgb = new int[3];
		
		int[][][] result = new int[width][height][3];
		
		for(int i=1; i<width-1; i++){
			for(int j=1; j<height-1; j++) {
				
				int[][] vals = new int[3][9];
				
				int count = 0;
				
				//Apply the kernel
				for(int x = -1; x<=1; x++) {
					for(int y = -1; y<=1; y++) {
						
						super.getPixel(i+x,j+y,rgb);
						
						vals[0][count] += rgb[0];
						vals[1][count] += rgb[1];
						vals[2][count] += rgb[2];
						
						count ++;
					}
				}
				
				int[] reds = new int[9];
				int[] greens = new int[9];
				int[] blues = new int[9];
				
				reds   = vals[0];
				greens = vals[1];
				blues  = vals[2];
				
				//Find the median color
				Arrays.sort(reds);
				Arrays.sort(greens);
				Arrays.sort(blues);
				
				//Grab median value
				int red   = reds[4];
				int green = greens[4];
				int blue  = blues[4];
				
				int r = 0;
				int g = 0;
				int b = 0;
				
				double best = 3* Math.pow(255, 2); //Maximum square value
				
				//Grab the pixel that is closest to this value;
				for(int x = -1; x<=1; x++) {
					for(int y = -1; y<=1; y++) {
						
						super.getPixel(i+x,j+y,rgb);
						
						int v1 = rgb[0] - red;
						int v2 = rgb[1] - green;
						int v3 = rgb[2] - blue;
						
						//Least Squares Error
						double error = v1*v1 + v2*v2 + v3*v3;
						
						//Grab the best matching pixel
						if(error <= best) {
							best = error;
							r = rgb[0];
							g = rgb[1];
							b = rgb[2];
						}
					}
				}
				
				// Set the pixel.
				result[i][j][0] =  r;
				result[i][j][1] =  g;
				result[i][j][2] =  b;
			}
		}
		
		//Set the original image with the values in the result buffer
		for(int i=1; i<width-1; i++){
			for(int j=1; j<height-1; j++) {
			
				super.setPixel(i, j, result[i][j]);
			
			}
		}
	}

	@Override
	public void uniformBlur() {
		int width = super.getWidth();
		int height = super.getHeight();
		
		// Preallocate the arrays.
		int[] rgb = new int[3];
		
		int[][][] result = new int[width][height][3];
		
		for(int i=1; i<width-1; i++){
			for(int j=1; j<height-1; j++) {
				
				int[] total = {0,0,0};
				
				//Apply the kernel
				for(int x = -1; x<=1; x++) {
					for(int y = -1; y<=1; y++) {
						
						super.getPixel(i+x,j+y,rgb);
						
						total[0] += rgb[0];
						total[1] += rgb[1];
						total[2] += rgb[2];
						
					}
				}
				
				int[] average = new int[3];
				
				//Average the pixel values
				average[0] = (int)(total[0]/9.0);
				average[1] = (int)(total[1]/9.0);
				average[2] = (int)(total[2]/9.0);

				// Set the pixel.
				result[i][j][0] =  average[0];
				result[i][j][1] =  average[1];
				result[i][j][2] =  average[2];
			}
		}
		
		//Set the original image with the values in the result buffer
		for(int i=1; i<width-1; i++){
			for(int j=1; j<height-1; j++) {
			
				super.setPixel(i, j, result[i][j]);
			
			}
		}
	}

	@Override
	public void grayscale() {
		int width = super.getWidth();
		int height = super.getHeight();
		
		// Preallocate the arrays.
		int[] rgb = new int[3];
		float[] hsb = new float[3];
		
		for(int i=0; i<width; i++){
			for(int j=0; j<height; j++) {

				super.getPixel(i, j, rgb);
				// Convert to HSB.
				Color.RGBtoHSB(rgb[0], rgb[1], rgb[2], hsb);
				
				// Set the saturation to zero to grayscale
				hsb[1] = 0;
				
				//Convert back to RGB
				Color c = Color.getHSBColor(hsb[0], hsb[1], hsb[2]);
				rgb[0] = c.getRed();
				rgb[1] = c.getGreen();
				rgb[2] = c.getBlue();
				// Set the pixel.
				setPixel(i, j, rgb);
			}
		}
	}

	@Override
	public void contrast(int amount) {
		int width = super.getWidth();
		int height = super.getHeight();
		
		// Preallocate the arrays.
		int[] rgb = new int[3];
		float[] hsb = new float[3];
		
		for(int i=0; i<width; i++){
			for(int j=0; j<height; j++) {

				super.getPixel(i, j, rgb);
				// Convert to HSB.
				Color.RGBtoHSB(rgb[0], rgb[1], rgb[2], hsb);
				
				//Change the contrast according to the formula
				hsb[2] = (float) (Math.pow((amount + 100.0)/100.0,4) * (hsb[2] - 0.5) + 0.5);
				
				//Make sure it is between 0 and 1
				hsb[2] = (float) Math.min(Math.max(hsb[2],0.0), 1.0);
				
				//Convert back to RGB
				Color c = Color.getHSBColor(hsb[0], hsb[1], hsb[2]);
				rgb[0] = c.getRed();
				rgb[1] = c.getGreen();
				rgb[2] = c.getBlue();
				// Set the pixel.
				setPixel(i, j, rgb);
			}
		}
	}

	@Override
	public void brightness(int amount) {
		//Scale into the appropriate range
		float adjustment = (float)(amount/100.0);
		
		int width = super.getWidth();
		int height = super.getHeight();
		
		// Preallocate the arrays.
		int[] rgb = new int[3];
		float[] hsb = new float[3];
		
		for(int i=0; i<width; i++){
			for(int j=0; j<height; j++) {
				
				super.getPixel(i, j, rgb);
				// Convert to HSB.
				Color.RGBtoHSB(rgb[0], rgb[1], rgb[2], hsb);
				
				//Add to the brightness channel, make sure it is between 0 and 1
				hsb[2] = (float)Math.min(Math.max(hsb[2] + adjustment, 0.0),1.0);
				
				//Convert back to RGB
				Color c = Color.getHSBColor(hsb[0], hsb[1], hsb[2]);
				
				rgb[0] = c.getRed();
				rgb[1] = c.getGreen();
				rgb[2] = c.getBlue();
				// Set the pixel.
				super.setPixel(i, j, rgb);
			}
		}
	}

}
