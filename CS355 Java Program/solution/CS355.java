package cs355.solution;

import cs355.GUIFunctions;
//import cs355.controller.CS355Controller;
import cs355.controller.Controller;
import cs355.model.drawing.CS355Drawing;
import cs355.model.drawing.Model;
import cs355.view.*;

/**
 * This is the main class. The program starts here.
 * Make you add code below to initialize your model,
 * view, and controller and give them to the app.
 */
public class CS355 {

	private static int canvas_size = 2048;
	private static int view_size = 512;
	
	/**
	 * This is where it starts.
	 * @param args = the command line arguments
	 */
	public static void main(String[] args) {

		// Create Instances of the MVC
		CS355Drawing drawing = new Model();
		Controller control = new Controller(drawing);
		ViewRefresher view = new Viewer(drawing, control);
		
		GUIFunctions.createCS355Frame(control, view);

		//Get the Scroll Bars initialized
		GUIFunctions.setHScrollBarMin(0);
		GUIFunctions.setHScrollBarMax(canvas_size);
		GUIFunctions.setVScrollBarMin(0);
		GUIFunctions.setVScrollBarMax(canvas_size);
		GUIFunctions.setVScrollBarKnob(view_size);
		GUIFunctions.setHScrollBarKnob(view_size);
				//*/
		
		GUIFunctions.refresh();
	}
}
