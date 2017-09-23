package cs355.model.drawing;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/**
 *
 * @author david
 */
public class Model extends CS355Drawing {

    private ArrayList<Shape> shapelist = new ArrayList<>();
    
    @Override
    public Shape getShape(int index) {
    	if(index < shapelist.size()) {
    		return shapelist.get(index);
    	}
    	return null;
    }
    
    //Notify the model it has changed
    public void shapeChanged() {
    	setChanged();
        notifyObservers();
    }
    
    @Override
    public int addShape(Shape s) {
        int index = shapelist.size();
        shapelist.add(s);
        setChanged();
        notifyObservers();
        return index;
    }

    @Override
    public void deleteShape(int index) {
    	if(index < shapelist.size()) {
    		shapelist.remove(index);
    	}
    	setChanged();
    	notifyObservers();
    }

    @Override
    public void moveToFront(int index) {
        Shape s = shapelist.get(index);
        shapelist.remove(index);
        shapelist.add(0,s);
        setChanged();
        notifyObservers();
    }

    @Override
    public void movetoBack(int index) {
        Shape s = shapelist.get(index);
        shapelist.remove(index);
        shapelist.add(s);
        setChanged();
        notifyObservers();
    }

    @Override
    public void moveForward(int index) {
        if(index > 0)  {
            Shape s = shapelist.get(index);
            shapelist.remove(index);
            shapelist.add(index-1,s);
            setChanged();
            notifyObservers();
        }
    }

    @Override
    public void moveBackward(int index) {
        
        if(index < shapelist.size()-1)  {
            Shape s = shapelist.get(index);
            shapelist.remove(index);
            shapelist.add(index+1,s);
            setChanged();
            notifyObservers();
        }
    }

    @Override
    public List<Shape> getShapes() {
        return shapelist;
    }

    @Override
    public List<Shape> getShapesReversed() {
        
        //Reverse the list, copy it, put it back the way it was
        Collections.reverse(shapelist);
        List<Shape> reversed = new ArrayList<>(shapelist);
        Collections.reverse(shapelist);
        
        return reversed;
    }

    @Override
    public void setShapes(List<Shape> shapes) {
        shapelist = new ArrayList<>(shapes);
        setChanged();
        notifyObservers();
    }
    
    @Override
    public String toString() {
    	return shapelist.toString();
    }
    
}
