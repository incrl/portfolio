package cs355.view;

public class Point4D {
	
	public double x;
	public double y;
	public double z;
	public double w;
	
	public Point4D() {
		this.x = 0;
		this.y = 0;
		this.z = 0;
		this.w = 0;
	}
	
	public Point4D(double x, double y, double z, double w) {
		this.x = x;
		this.y = y;
		this.z = z;
		this.w = w;
	}
	
	public Point4D(double[] C) {
		this.x = C[0];
		this.y = C[1];
		this.z = C[2];
		this.w = C[3];
	}
}
