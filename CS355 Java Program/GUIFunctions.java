package cs355;

import cs355.view.ViewRefresher;
import cs355.controller.CS355Controller;
import java.awt.Color;

/**
 * A collection of static functions that allow the
 * student's CS355Controller to control the window.
 * @author Talonos
 */
public class GUIFunctions {

	/**
	 * Refreshes the view by repainting the canvas. Call this
	 * any time the picture in the main view should change.
	 */
	public static void refresh() {
		RedrawRoutine.inst().refreshView();
	}

	/**
	 * Changes the main view so that the given color is shown
	 * in the color selector box.
	 * @param c = the color to show in the color selector box.
	 */
	public static void changeSelectedColor(Color c) {
		CS355Frame.inst().setSelectedColor(c);
	}

	/**
	 * Changes the amount the vertical scrollbar returns
	 * when it is all the way at the top.
	 * @param newMin = the new value to return when the
	 *				   vertical scrollbar is at the top.
	 */
	public static void setVScrollBarMin(int newMin) {
		CS355Frame.inst().setScrollAttribute(CS355Scrollbar.V_SCROLL_BAR, CS355ScrollbarAttr.MIN, newMin);
	}

	/**
	 * Changes the amount the horizontal scrollbar returns
	 * when it is all the way at the left.
	 * @param newMin = the new value to return when the
	 *				   horizontal scrollbar is at the left.
	 */
	public static void setHScrollBarMin(int newMin) {
		CS355Frame.inst().setScrollAttribute(CS355Scrollbar.H_SCROLL_BAR, CS355ScrollbarAttr.MIN, newMin);
	}

	/**
	 * Changes the amount the vertical scrollbar returns when
	 * it is all the way at the bottom. <b>Important</b>: See
	 * {@link #setVScrollBarKnob(int)} for further clarification!
	 * @param newMax = the new value to return when the
	 *				   horizontal scrollbar is at the bottom.
	 */
	public static void setVScrollBarMax(int newMax) {
		CS355Frame.inst().setScrollAttribute(CS355Scrollbar.V_SCROLL_BAR, CS355ScrollbarAttr.MAX, newMax);
	}

	/**
	 * Changes the amount the horizontal scrollbar returns when
	 * it is all the way at the left. <b>Important</b>: See
	 * {@link #setHScrollBarKnob(int)} for further clarification!
	 * @param newMax = the new value to return when the
	 *				   horizontal scrollbar is at the right.
	 */
	public static void setHScrollBarMax(int newMax) {
		CS355Frame.inst().setScrollAttribute(CS355Scrollbar.H_SCROLL_BAR, CS355ScrollbarAttr.MAX, newMax);
	}

	/**
	 * Sets the width of the scrollbar's knob. This is not just purely
	 * visual! If you have, for example, a knob width of 2 and a maximum
	 * value of 4, then the knob will "fill" the last half of the scroll
	 * bar and return a value of 2 if pushed all the way to the left!
	 * @param newKnob = the new width of the knob.
	 */
	public static void setVScrollBarKnob(int newKnob) {
		CS355Frame.inst().setScrollAttribute(CS355Scrollbar.V_SCROLL_BAR, CS355ScrollbarAttr.KNOB, newKnob);
	}

	/**
	 * Sets the width of the scrollbar's knob. This is not just purely
	 * visual! If you have, for example, a knob width of 2 and a maximum
	 * value of 4, then the knob will "fill" the last half of the scroll
	 * bar and return a value of 2 if pushed all the way to the left!
	 * @param newKnob = the new width of the knob.
	 */
	public static void setHScrollBarKnob(int newKnob) {
		CS355Frame.inst().setScrollAttribute(CS355Scrollbar.H_SCROLL_BAR, CS355ScrollbarAttr.KNOB, newKnob);
	}

	/**
	 * Sets the position of the scrollbar's knob. This
	 * will send an event to the student's controller!
	 * @param newPosit = the new position of the knob.
	 */
	public static void setHScrollBarPosit(int newPosit) {
		CS355Frame.inst().setScrollAttribute(CS355Scrollbar.H_SCROLL_BAR, CS355ScrollbarAttr.POSITION, newPosit);
	}

	/**
	 * Sets the position of the scrollbar's knob. This
	 * will send an event to the student's controller!
	 * @param newPosit = the new position of the knob.
	 */
	public static void setVScrollBarPosit(int newPosit) {
		CS355Frame.inst().setScrollAttribute(CS355Scrollbar.V_SCROLL_BAR, CS355ScrollbarAttr.POSITION, newPosit);
	}

	/**
	 * Creates a new CS355Frame. This is the first thing you should call.
	 * @param c = the CS355Controller you wish to receive button events.
	 * @param v = The view refresher used to draw the canvas.
	 */
	public static void createCS355Frame(CS355Controller c, ViewRefresher v) {
		CS355Frame.createCS355Frame(c, v);
	}
	
	/**
	 * Tells the frame that the user wants to set the zoom label.
	 * @param zoom = the new zoom level that should be printed.
	 */
	public static void setZoomText(double zoom) {
		CS355Frame.inst().setZoomText(zoom);
	}
	
	/**
	 * Outputs a string to the debugging label.
	 * @param fmt = the format string.
	 * @param args = the args for formatting.
	 */
	public static void printf(String fmt, Object... args) {
		CS355Frame.inst().setDebugText(fmt, args);
	}
}
