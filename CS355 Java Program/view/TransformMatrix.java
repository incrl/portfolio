package cs355.view;

import cs355.model.scene.Point3D;

public class TransformMatrix {

	private double[][] matrix;
	
	public TransformMatrix() {
		matrix = new double[4][4];
	}
	
	public TransformMatrix(double[][] matrix) {
		this.matrix = matrix;	
	}
	
	public double[][] getMatrix() {
		return matrix;
	}
	
	//Multiplies the current matrix on the left side of the given matrix
	public void multiplyMatrix(TransformMatrix rhs) {
		
		double[][] A = matrix;
		double[][] B = rhs.getMatrix();
		double[][] C = new double[4][4];
		
		for (int i = 0; i < 4; i++)
			   for (int j = 0; j < 4; j++)
			      for (int k = 0; k < 4; k++)
			         C[i][j] += A[i][k] * B[k][j];
		
		//Set the current matrix the computed matrix
		matrix = C;
	}
	
	public Point4D multiplyPoint(Point3D pt) {
		
		//Make homogenous point
		double[] B = new double[4];
		B[0] = pt.x;
		B[1] = pt.y;
		B[2] = pt.z;
		B[3] = 1.0;
		double[] C = new double[4];
		
		for (int i = 0; i < 4; i++)
			 for (int k = 0; k < 4; k++)
			     C[i] += matrix[i][k] * B[k];
		
		Point4D result = new Point4D(C);
		return result;
	}
	
public Point4D multiplyPoint(Point4D pt) {
		
		//Make homogenous point
		double[] B = new double[4];
		B[0] = pt.x;
		B[1] = pt.y;
		B[2] = pt.z;
		B[3] = pt.w;
		double[] C = new double[4];
		
		for (int i = 0; i < 4; i++)
			 for (int k = 0; k < 4; k++)
			     C[i] += matrix[i][k] * B[k];
		
		Point4D result = new Point4D(C);
		return result;
	}
}
