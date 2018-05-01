// RaytracerOriginal.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"

#include "math.h"
#include <iostream>
#include <fstream>
#include "CImg.h"

#define PI 3.14159265358979323846  /* pi */
#define maxCount 5
#define maxNum 10000000
#define indexOfRefraction 1.52
#define epsilon .001
#define jit 0.01
#define sub_jit 0.001
#define num_rays 100
#define num_sub_rays 2
#define dilution .5
#define the_scene scene1
#define the_res 256

/*
################################################Structs and Functions########################################
*/

using namespace cimg_library;

double random()
{
	return (double)rand() / (double)RAND_MAX;
}

struct vec { 
	double x;
	double y; 
	double z;

	vec operator + (vec B) {
		return vec{ x + B.x, y + B.y, z + B.z };
	}

	vec operator - (vec B) {
		return vec{ x - B.x, y - B.y, z - B.z };
	}

	vec operator - () {
		return vec{ -x, -y, -z };
	}

	vec operator * (vec B) {
		return vec{ x * B.x, y * B.y, z * B.z };
	}

	vec operator * (double coef) {
		return vec{ coef * x, coef * y, coef * z };
	}

	vec operator / (double num) {
		return vec{ x / num, y / num, z / num };
	}
};

vec operator * (double coef, vec A) {
	return vec{ coef * A.x, coef * A.y, coef * A.z };
}

vec normalize(vec A) {
	double norm = sqrt(A.x*A.x + A.y*A.y + A.z*A.z);
	return vec{ A.x / norm , A.y / norm, A.z / norm };
}

vec clip(vec A, double lower, double upper) {
	return vec{ fmax(fmin(A.x, upper), lower), fmax(fmin(A.y, upper),lower), fmax(fmin(A.z, upper),lower) };
}

double mag(vec A) {
	return A.x*A.x + A.y*A.y + A.z*A.z;
}

double norm(vec A) {
	return sqrt(A.x*A.x + A.y*A.y + A.z*A.z);
}

double vDot(vec A, vec B) {
	return A.x * B.x + A.y * B.y + A.z * B.z;
}

vec vCross(vec A, vec B) {
	return vec{ A.y*B.z - A.z*B.y, A.z*B.x - A.x*B.z, A.x*B.y - A.y*B.x };
}

vec jitter(vec A,double amount) {
	return normalize(vec{ A.x + amount*(random() - .5), A.y + amount*(random() - .5), A.z + amount*(random() - .5) });
}

vec toVec(double* data) {
	return vec{ data[0], data[1], data[2] };
}

vec pathDiffuse(vec n) {
	vec rd = normalize(vec{ random() - .5, random() - .5, random() - .5 });
	if (vDot(rd, n) < 0)
		rd = -rd;
	return rd;
}

vec pathSpecular(vec n, vec dir) {
	// Calculate the reflection vector and specular dot product
	vec reflection = normalize(dir - (n * 2.0 * vDot(dir, n)));
	return jitter(reflection, sub_jit);
}

vec pathTransparent(vec n, vec dir) {
	// Refraction Direction Calculation
	double angle = vDot(-normalize(dir), normalize(n));
	double nit = 1 / indexOfRefraction;

	// Flip index if exiting
	if (angle < 0) {
		nit = 1 / nit;
		angle = -angle;
	}

	vec refractDir = normalize(nit * normalize(dir) + (nit*angle - sqrt(1 + nit*nit*(angle*angle - 1)))*n);

	return refractDir;
}

vec choosePath(double Kd, double Kt, vec n, vec dir) {
	
	double choice = (1 + Kt) * random();

	if (choice < Kd) {
		return pathDiffuse(n);
	}
	else if (choice < 1.0) {
		return pathSpecular(n,dir);
	}
	else {
		return pathTransparent(n, dir);
	}
}


void printVec(vec A) {
	printf("%f, %f, %f \n", A.x, A.y, A.z);
}

//Parent Class
struct Light {
	vec color;

	//Constructor
	Light(vec m_color) : color(m_color) {}

	//Lighting
	virtual vec getDirection(vec p)=0;
	virtual double getDistance(vec p) = 0;
};

struct dirLight: Light {
	vec dir;

	//Constructor
	dirLight(vec m_dir, vec m_color) : dir(m_dir), Light(m_color){}

	//Lighting
	vec getDirection(vec p) {
		return normalize(dir);
	}

	double getDistance(vec p) {
		return maxNum;
	}
};

struct pointLight: Light {
	vec pos;

	pointLight(vec m_pos, vec m_color) : pos(m_pos), Light(m_color) {}

	vec getDirection(vec p) {
		return normalize(p - pos);
	}

	double getDistance(vec p) {
		return norm(p - pos);
	}
};

struct areaLight: Light {

private: 
	vec light_point;

public:
	vec topLeft;
	vec topRight;
	vec bottomRight;

	areaLight(vec tl, vec tr, vec br, vec col) : topLeft(tl), topRight(tr), bottomRight(br), Light(col) {}

	vec getDirection(vec p) {

		// Get a random location for the area light
		light_point = topRight + ((topLeft - topRight)*random()) + ((bottomRight - topRight)*random());
		
		return normalize(p - light_point);
	}

	double getDistance(vec p) {
		return norm(p - light_point);
	}
};

struct material {
	vec Cd;
	vec Cs;
	double phong;
	double Kd;
	double Kt;
	CImg<double>* texture;

	material(vec m_Cd, vec m_Cs, double m_phong, double m_Kd, double m_Kt, char* texture_fn) : Cd(m_Cd), Cs(m_Cs), phong(m_phong), Kd(m_Kd), Kt(m_Kt) {
		if (texture_fn != "") {
			texture = new CImg<double>(texture_fn);
		}
		else {
			texture = NULL;
		}
	}
};

struct sphere {
	vec cen;
	double rad;
	int mat;
};

struct rect {
	vec topLeft;
	vec topRight;
	vec bottomRight;
	int mat;

	//These are to be calculated
	vec bottomLeft;
	vec normal;

	rect(vec tl, vec tr, vec br, int m) : topLeft(tl), topRight(tr), bottomRight(br), mat(m) {
		
		//Calculate the corner by taking vector differences
		bottomLeft = topLeft + (bottomRight - topRight);

		//Calculate the normal using the cross product
		normal = normalize(vCross(topLeft - topRight,bottomLeft - topRight));
	}
};

struct BoundingBox {
	double xmin;
	double xmax;
	double ymin;
	double ymax;
	double zmin;
	double zmax;

	void printBox() {
		printf(" %f, %f \n %f, %f \n %f, %f ", xmin, xmax, ymin, ymax, zmin, zmax);
	}
};

bool crossProductTest(vec p, rect r) {
	
	vec side0 = r.topLeft - r.topRight;
	vec side1 = r.topRight - r.bottomRight;
	vec side2 = r.bottomRight - r.bottomLeft;
	vec side3 = r.bottomLeft - r.topLeft;

	vec center0 = p - r.topRight;
	vec center1 = p - r.bottomRight;
	vec center2 = p - r.bottomLeft;
	vec center3 = p - r.topLeft;

	vec r0 = vCross(side0, center0);
	vec r1 = vCross(side1, center1);
	vec r2 = vCross(side2, center2); 
	vec r3 = vCross(side3, center3);

	double d0 = vDot(r0, r.normal);
	double d1 = vDot(r1, r.normal);
	double d2 = vDot(r2, r.normal);
	double d3 = vDot(r3, r.normal);

	//Three cases
	if (d0 > 0 && d1 > 0 && d2 > 0 && d3 > 0) { return true; }
	else if (d0 < 0 && d1 < 0 && d2 < 0 && d3 < 0) { return true; }
	else { return false; }
}

vec getTexture(CImg<double>* texture, vec tex_coord) {

	//Find the x,y coordinates of the image
	double x = tex_coord.x * texture->width();
	double y = tex_coord.y * texture->height();

	//Grab the surrounding pixels
	int lx = floor(x);
	int rx = ceil(x);
	int ty = floor(y);
	int by = ceil(y);
	
	//Check out of bounds
	if (rx > texture->width() - 1) { rx = texture->width() - 1;}
	if (by > texture->height() - 1) { by = texture->height() - 1;}

	//Grab the image at each location
	vec tl = toVec(texture->data(ty, lx));
	vec tr = toVec(texture->data(ty, rx));
	vec bl = toVec(texture->data(by, lx));
	vec br = toVec(texture->data(by, rx));

	//Interpolate the values
	double dx = x - lx;
	double dy = y - ty;

	vec left = bl*dy + tl*(1 - dy);
	vec right = br*dy + tr*(1 - dy);
	vec result = right*dx + left*(1 - dx);

	//Divide by 255 for formating
	return result / 255;
}

BoundingBox generateBoundingBox(sphere* spheres, int numSpheres) {

	double xmin = maxNum;
	double xmax = -maxNum;
	double ymin = maxNum;
	double ymax = -maxNum;
	double zmin = maxNum;
	double zmax = -maxNum;


	for (int i = 0; i < numSpheres; i++) {
		sphere s = spheres[i];

		//Dimensions check
		if (s.cen.x - s.rad < xmin)
			xmin = s.cen.x - s.rad;
		if (s.cen.x + s.rad > xmax)
			xmax = s.cen.x + s.rad;
		if (s.cen.y - s.rad < ymin)
			ymin = s.cen.y - s.rad;
		if (s.cen.y + s.rad > ymax)
			ymax = s.cen.y + s.rad;
		if (s.cen.z - s.rad < zmin)
			zmin = s.cen.z - s.rad;
		if (s.cen.z + s.rad > zmax)
			zmax = s.cen.z + s.rad;
	}

	return{ xmin,xmax,ymin,ymax,zmin,zmax };
};

struct scene {
	vec background;
	vec ambient;
	vec lookFrom;
	vec lookAt;
	vec lookUp;
	double fovx;
	double fovy;
	int numLights;
	Light** lights;
	int numMaterials;
	material *mats;
	int numSpheres;
	sphere *spheres;
	int numRectangles;
	rect *rects;
};


/*
################################################Scene Setups########################################
*/

dirLight dLight1 = { {-.1,-.1,-1},{1.0,1.0,1.0} };
dirLight dLight2 = { {-1,1,0},{ .5,.5,.5 } };
dirLight dLight3 = { {0,1,0.1}, {1,1,1} };
//pointLight pLight1 = { { 0,0,0 },{ 1,1,1 } };
pointLight pLight1 = { {3,-7,-2}, {1,1,1} };
pointLight pLight2 = { {-2,-2,0}, {1,1,1} };
pointLight pLight3 = { {-1,-1,1}, {1,1,1} };
areaLight aLight1 = { {-1, -12, -20}, { -1, 12, -21 } ,{ 1, -12, -21 }, {1,1,1} };
areaLight aLight2 = { { -1, -15, -2 },{ -1, -15, -8 } ,{ 1, -15, -8 },{ 1,1,1 } };
Light* lights1[] = { &dLight1 };
Light* lights2[] = { &dLight1, &dLight2 };
Light* lights3[] = { &pLight1, &dLight1, &dLight2 };
Light* lights4[] = { &pLight2 };
Light* lights5[] = { &aLight1 };
//Light* lights6[] = { &pLight3, &aLight2 };
Light* lights6[] = { &aLight2 };
material mat1 = { {0,1,0}, {.5, 1, .5}, 4, 1.0, 0, "" };
material mat2 = { {1,1,0},{ .5, 1, .5 }, 4, .7, 0, "" };
material mat3 = { {0,0,1},{ .5, 1, .5 }, 4, 1.0, 0, "wood.bmp" };
material mat4 = { { 1,0,0 },{ 1, 1, 1 }, 4, 1.0, 0, "" };
material mat5 = { { .678,0.078,.2 },{ 1, 1, 1 }, 4, .8, 0, "" };
material mat6 = { { 0,1,1 },{ 1, 1, 1 }, 4, 1.0, 0, "" };
material mat7 = { { 1,1,1 },{ 1, 1, 1 }, 4, 1.0, 0, "" };
material mat8 = { { .1,.1,0 },{ 1, 1, 1 }, 4, 1.0, .8, "" };
material mat9 = { { 1,1,1 },{ 1, 1, 1 }, 4, 1.0, 0, "Granite.bmp" };
material mat10 = { { 1,1,1 },{ 1, 1, 1 }, 4, .7, 0, "escher.bmp" };
material mat11 = { { .4,.4,.4},{ 1, 1, 1 }, 4, .8, .8, "left.bmp" };
material mat12 = { { .7,.7,.7 },{ 1, 1, 1 }, 4, 1.0, 0, "" };
material mat13 = { { 0, 0, 0 }, { 1, 1, 1 }, 4, 1, 1.0, "" };
material mat14 = { { 1, 1, 1 },{ 1, 1, 1 }, 4, .9, 0, "CheckerboardPattern.bmp" };
material mat15 = { { 0, 0, 0 }, {1, 1, 1}, 4, .1, 0, "" };
material mat16 = { { 1, 1, 1 },{ 1, 1, 1 }, 4, 1.0, 0, "Sky.bmp" };
material mats[] = { mat1, mat2, mat3, mat4, mat5, mat6, mat7, mat8, mat9, mat10, mat11, mat12, mat13, mat14, mat15, mat16};
sphere sphere1 = { {-2,0,-20}, 1, 1};
sphere sphere2 = { {0.5,0,-22}, 1, 2};
sphere sphere3 = { {4,0,-24}, 1, 3};
sphere sphere4 = { {-1.25, -.5, -1.5}, .5, 11 };
sphere sphere5 = { {0, -.5, -1.5}, .5, 10 };
sphere sphere6 = { {1.25, -.5, -1.5}, .5, 12 };
sphere sphere7 = { {-1, 1, -9}, .8, 5 };
sphere sphere8 = { { 2, 0, -7 }, .8, 15 };
sphere sphere9 = { { -.5, -2, -6 }, .8, 15 };
sphere spheres[] = { sphere1, sphere2, sphere3 };
sphere escher[] = { sphere4, sphere5, sphere6 };
sphere checker[] = { sphere7, sphere8, sphere9 };
rect rects1 = { {10, -10, -30}, {10,-10,0}, {10, 10, 0}, 4 };
rect rects2 = { { -11, -10, 0 },{ -11,-10,-30 },{ 11, -10, -30 }, 5 };
rect rects3 = { { -10, -10, 0 },{ -10,-10,-30 },{ -10, 10, -30 }, 6 };
rect rects4 = { { -11, 10, 0 },{ -11,10,-30 },{ 11, 10, -30 }, 14 };
rect rects5 = { { -11, -11, -30 },{ 11,-11,-30 },{ 11, 11, -30 }, 1};
rect rects6 = { { -1, -1, -7 },{ 1,-1,-7 },{ 1, 1, -7 }, 8 };
rect rects[] = { rects3, rects4, rects5, rects1, rects2, rects6 };
rect table1 = { { -4, .5, 0 },{-4, .5, -5},{4, .5, -5}, 9};
rect table[] = { table1 };
rect checkerboard = { {-10,2, 0}, {-10, 2, -10}, {10, 2, -10 }, 14 };
rect mirror = { {-3,2,0}, {-3,-8, 0}, {-3, -8, -10}, 15 };
rect sky = { {-10,2,-10}, {-10,-12,-10},{10,-12,-10 }, 16 };
rect board[] = { checkerboard, mirror, sky };

scene scene1 = {
	{ .2, .2, .2 },
	{ .1, .1, .1 },
	{ 0, 0, 1 },
	{ 0, 0, 0 },
	{ 0, 1, 0 },
	30.0,
	30.0,
	2,
	lights2,
	10,
	mats,
	3,
	spheres,
	0,
	NULL,
};

scene scene2 = {
	{ .2, .2, .2 },
	{ .1, .1, .1 },
	{ 0, 0, 1 },
	{ 0, 0, 0 },
	{0, 1, 0},
	30.0,
	30.0,
	1,
	lights3,
	10,
	mats,
	3,
	spheres,
	5,
	rects
};

scene scene3 = {
	{ .2, .2, .2 },
	{ .1, .1, .1 },
	{ 0, -2.2, 1 },
	{ 0, -1, 0 },
	{ 0, 1, 0 },
	35.0,
	35.0,
	1,
	lights4,
	12,
	mats,
	3,
	escher,
	1,
	table
};

scene scene4 = {
	{ .2, .2, .2 },
	{ .1, .1, .1 },
	{ 0, 0, 1 },
	{ 0, 0, 0 },
	{ 0, 1, 0 },
	30.0,
	30.0,
	1,
	lights5,
	10,
	mats,
	3,
	spheres,
	3,
	rects
};

scene scene5 = {
	{ 0, .2, .8 },
	{ .1, .1, .1 },
	{ 0, 0, 1 },
	{ 0, 0, 0 },
	{ 0, 1, 0 },
	30.0,
	30.0,
	1,
	lights6,
	14,
	mats,
	3,
	checker,
	3,
	board
};

/*
################################################Actual Code########################################
*/

void saveImage(double *picture, int res) {

	std::ofstream myfile;
	myfile.open("output.ppm", std::ofstream::out | std::ofstream::trunc);
	myfile << "P3\n";
	myfile << res << " " << res <<"\n";
	myfile << 255 << "\n";

	for (int i = 0; i < res*res*3; i++) {
		myfile << (int)(picture[i] * 255.0) << "\n";
	}

	myfile.close();

	printf("Image saved!");

}

bool hitBoundingBox(vec ro, vec rd, BoundingBox box) {

	double t_near = -maxNum;
	double t_far = maxNum;

	//x-direction
	if (abs(rd.x) < .0001) {
		if (ro.x < box.xmin || ro.x > box.xmax) {
			return false;
		}
	}
	else {
		double t1 = (box.xmin - ro.x) / rd.x;
		double t2 = (box.xmax - ro.x) / rd.x;
		if (t1 > t2) {
			double temp = t1;
			t1 = t2;
			t2 = temp;
		}
		if (t1 > t_near) {
			t_near = t1;
		}
		if (t2 < t_far) {
			t_far = t2;
		}
		if (t_near > t_far) {
			return false;
		}
		if (t_far < 0) {
			return false;
		}
	}

	//y-direction
	if (abs(rd.y) < .0001) {
		if (ro.y < box.ymin || ro.y > box.ymax) {
			return false;
		}
	}
	else {
		double t1 = (box.ymin - ro.y) / rd.y;
		double t2 = (box.ymax - ro.y) / rd.y;
		if (t1 > t2) {
			double temp = t1;
			t1 = t2;
			t2 = temp;
		}
		if (t1 > t_near) {
			t_near = t1;
		}
		if (t2 < t_far) {
			t_far = t2;
		}
		if (t_near > t_far) {
			return false;
		}
		if (t_far < 0) {
			return false;
		}
	}

	//z-direction
	if (abs(rd.z) < .0001) {
		if (ro.z < box.zmin || ro.z > box.zmax) {
			return false;
		}
	}
	else {
		double t1 = (box.zmin - ro.z) / rd.z;
		double t2 = (box.zmax - ro.z) / rd.z;
		if (t1 > t2) {
			double temp = t1;
			t1 = t2;
			t2 = temp;
		}
		if (t1 > t_near) {
			t_near = t1;
		}
		if (t2 < t_far) {
			t_far = t2;
		}
		if (t_near > t_far) {
			return false;
		}
		if (t_far < 0) {
			return false;
		}
	}

	//Survived all tests
	return true;
}

bool isInShadow(vec p, vec dir, double distance, scene sc, BoundingBox box) {

	// Send ray to light
	if (hitBoundingBox(p, dir, box)) {

		for (int i = 0; i < sc.numSpheres; i++) {
			sphere s = spheres[i];

			//1. Determine wherther the origin is outside the sphere
			if (norm(p - s.cen) < s.rad) { continue; }

			//2. Find the closet approach to the sphere's center
			vec oc = s.cen - p;
			double tca = vDot(dir, oc);

			//3. If tca < 0, the ray does not intersect
			if (tca < 0) { continue; }

			//4. Compute thc, the distance from the approach to the surface
			double thc2 = s.rad*s.rad - mag(oc) + tca*tca;

			//5. If thc2 < 0, the ray does not intersect
			if (thc2 < 0) { continue; }

			//6. Otherwise, calculate the intersection distance
			double t = tca - sqrt(thc2);

			//Check to see if this distance is smaller than the distance to the light
			if (t < distance) {
				return true;
			}
		}
	}

	for (int i = 0; i < sc.numRectangles; i++) {
		rect r = rects[i];

		//1. Computer the normal vector
		vec pn = r.normal;

		//2. Compute vd
		double vd = vDot(pn, dir);

		//3. Check if it is parallel to plane
		if (abs(vd) < 0.001) { continue; }

		//4. Compute d, v0, and t
		vec origin = p;//{ 0.0, 0.0, 0.0 };
		double d = vDot(origin - r.topLeft, pn);
		double v0 = -(vd + d);
		double t = v0 / vd;

		//5. Check to see if the plane is behind you
		if (t < 0) { continue; }

		//6. Compute intersection location
		vec intersection = p + dir*t;

		//7. Complete cross product test to determine if it is inside the rectangle
		if (crossProductTest(intersection, r)) {

			if (t < distance) {
				return true;
			}
		}
	}

	return false;
}

vec rayTrace(vec ro, vec rd, scene sc, int count, BoundingBox box);

vec lighting(vec p, vec n, material mat, vec rd, scene sc, int count, bool shape, vec tex_coord, BoundingBox box) {

	vec ambient = sc.ambient;
	vec diffuse = { 0.0, 0.0, 0.0 };
	vec specular = { 0.0, 0.0, 0.0 };

	// For each light in the scene
	for (int i = 0; i < sc.numLights; i++) {
		Light* light = sc.lights[i];

		for (int k = 0; k < num_sub_rays; k++) {
			vec dir = light->getDirection(p);
			vec color = light->color;
			double dist = light->getDistance(p);

			//Determine if it is in shadow
			if (isInShadow(p + epsilon*n, -jitter(dir, sub_jit), dist, sc, box)) { continue; }

			// Calculate the diffuse dot product
			double theta1 = vDot(n, -dir);

			// Not visible from the light
			if (theta1 < 0) { continue; }

			// Phong Lighting Model
			vec color_diffuse = { 0,0,0 };
			if (mat.texture == NULL) {
				color_diffuse = color * (mat.Cd * mat.Kd * theta1);
			}
			else { //Texture based coloring
				color_diffuse = color * (getTexture(mat.texture, tex_coord) * mat.Kd * theta1);
			}
			diffuse = diffuse + color_diffuse/num_sub_rays;

			// Calculate the reflection vector and specular dot product
			vec reflection = normalize(dir - (n * 2.0 * vDot(dir, n)));
			double theta2 = vDot(-rd, reflection);
			if (theta2 < 0) { continue; }

			// Phong Lighting Model
			vec color_specular = color *  (mat.Cs * (1 - mat.Kd) * pow(theta2, mat.phong));
			specular = specular + color_specular/num_sub_rays;
		}


	}

	/*
	// Compute Reflective color
	vec reflectionDir = normalize(rd - (n * 2.0 * vDot(rd, n)));
	vec reflective = { 0.0, 0.0, 0.0 };
	if (mat.Kd < .99) {
		for (int k = 0; k < num_sub_rays; k++) {
			reflective = (1 - mat.Kd)*rayTrace(p + epsilon*reflectionDir, jitter(reflectionDir, sub_jit), sc, count + 1, box);
		}
		reflective = reflective / num_sub_rays;
	}
		
	// Compute Refractive color
	vec refractive = { 0.0, 0.0, 0.0 };
	
	// If it is a sphere
	if (shape && mat.Kt > .001) {
		
		// Refraction Direction Calculation
		double angle = vDot(-normalize(rd), normalize(n));
		double nit = 1/indexOfRefraction;

		// Flip index if exiting
		if (angle < 0) {
			nit = 1 / nit;
			angle = -angle;
		}

		vec refractDir = normalize(nit * normalize(rd) + (nit*angle - sqrt(1 + nit*nit*(angle*angle - 1)))*n);

		for (int k = 0; k < num_sub_rays; k++) {
			refractive = mat.Kt * rayTrace(p + epsilon*refractDir, jitter(refractDir, sub_jit), sc, count + 1, box);
		}

		refractive = refractive / num_sub_rays;
	}
	// If it is a rectangle
	else if(!shape && mat.Kt > .001) {
		for (int k = 0; k < num_sub_rays; k++) {
			refractive = mat.Kt*rayTrace(p + epsilon * rd, jitter(rd, sub_jit), sc, count + 1, box);
		}

		refractive = refractive / num_sub_rays;
	}

	vec total = ambient + diffuse + specular + reflective + refractive;

	*/

	// Path Tracing
	vec path = choosePath(mat.Kd, mat.Kt, rd, n);
	vec pathColor = dilution * rayTrace(p + epsilon * path, path, sc, count + 1, box);

	vec total = ambient + diffuse + specular + pathColor;

	return clip(total, 0.0, 1.0);
}

vec rayTrace(vec ro, vec rd, scene sc, int count, BoundingBox box) {

	//Stop infinite loops
	if (count >= maxCount) { return{ 0,0,0 }; }

	double tmin = maxNum;
	bool hit = false;
	sphere *spheres = sc.spheres;
	sphere front;
	rect *rects = sc.rects;
	//Save rectangle stats seperately
	vec pmin;
	vec nmin;
	int mmin;
	vec tl;
	vec tr;
	vec bl;

	//Determine if a sphere or rectangle is closer
	bool shapeFlag;

	if (hitBoundingBox(ro, rd, box)) {

		for (int i = 0; i < sc.numSpheres; i++) {
			sphere s = spheres[i];

			bool inside = false;

			//1. Determine wherther the origin is outside the sphere
			if (norm(ro - s.cen) < s.rad) { inside = true; }

			//2. Find the closet approach to the sphere's center
			vec oc = s.cen - ro;
			double tca = vDot(rd, oc);

			//3. If tca < 0, the ray does not intersect
			if (tca < 0 && !inside) { continue; }

			//4. Compute thc, the distance from the approach to the surface
			double thc2 = s.rad*s.rad - mag(oc) + tca*tca;

			//5. If thc2 < 0, the ray does not intersect
			if (thc2 < 0) { continue; }

			//6. Otherwise, calculate the intersection distance
			double t = tca - sqrt(thc2);

			if (inside) {
				t = tca + sqrt(thc2);
			}

			//Check to see if this the smallest t so far
			if (t < tmin) {
				tmin = t;
				front = s;
				hit = true;
				shapeFlag = true;
			}
		}
	}

	for (int i = 0; i < sc.numRectangles; i++) {
		rect r = rects[i];

		//1. Computer the normal vector
		vec pn = r.normal;

		//2. Compute vd
		double vd = vDot(pn, rd);

		//3. Check if it is parallel to plane
		if (abs(vd) < 0.001) { continue; }

		//4. Compute d, v0, and t
		vec origin = ro; //{ 0.0, 0.0, 0.0 };
		double d = vDot(origin - r.topLeft, pn);
		double v0 = -(vd + d);
		double t = v0 / vd;

		//5. Check to see if the plane is behind you
		if (t < 0) { continue; }

		//6. Compute intersection location
		vec p = ro + rd*t;

		//7. Complete cross product test to determine if it is inside the rectangle
		if (crossProductTest(p, r)) {
			if (t < tmin) {
				tmin = t;
				pmin = p;
				//8. Flip the planes normal if necessary
				if (vd > 0) { pn = -pn; }
				nmin = pn;
				mmin = r.mat;
				hit = true;
				shapeFlag = false;
				tl = r.topLeft;
				tr = r.topRight;
				bl = r.bottomLeft;
			}
		}
	}

	if (!hit) {
		return sc.background;
	}
	
	if (shapeFlag) {
		//7. Calculate the intersection point
		vec p = ro + (rd*tmin);

		//8. Calculate the normal
		vec n = normalize(p - front.cen);

		//9. Grab the material from the sphere
		material mat = sc.mats[front.mat - 1];

		//If it is a texture, determine the texture coordinate
		vec tex_coord = { 0,0,0 };
		if (mat.texture != NULL) {
			//Graham-Schmidt to find axes
			vec zdir = normalize(sc.lookAt - sc.lookFrom);
			vec xdir = normalize(vCross(zdir, sc.lookUp));
			vec ydir = normalize(vCross(xdir, zdir));

			double x = (vDot(xdir, n) + 1)/2.0;
			double y = (vDot(ydir, n) + 1)/2.0;
			tex_coord = { y, x, 0 };
		}

		//Determine the lighting
		return lighting(p, n, mat, rd, sc, count, shapeFlag, tex_coord, box);
	}

	else {
		//8. Grab the material
		material mat = sc.mats[mmin-1];

		//If it is a texture, determine the texture coordinate
		vec tex_coord = { 0,0,0 };
		if (mat.texture != NULL) {
			double x = vDot(normalize(tr - tl), pmin - tl)/norm(tr-tl);
			double y = vDot(normalize(bl - tl), pmin - tl)/norm(bl-tl);
			tex_coord = { x, y, 0 };
		}

		//Determine the lighting
		return lighting(pmin, nmin, mat, rd, sc, count, shapeFlag, tex_coord, box);
	}
}

int main() {
	scene sc = the_scene;
	const int res = the_res;

	double d = norm(sc.lookAt - sc.lookFrom);
	double deltax = d*tan(sc.fovx*PI/180);
	double deltay = d*tan(sc.fovx*PI/180);

	//Graham-Schmidt to find axes
	vec zdir = normalize(sc.lookAt - sc.lookFrom);
	vec xdir = normalize(vCross(zdir, sc.lookUp));
	vec ydir = normalize(vCross(xdir, zdir));

	double *picture = new double[res*res*3];
	int h = res / 2;

	BoundingBox box = generateBoundingBox(sc.spheres, sc.numSpheres);
	box.printBox();

	for (int i = 0; i < res; i++) {

		printf("%d \n",i);

		for (int j = 0; j < res; j++) {

			//Determine intersecting ray
			double dx = deltax*(j - h + .5) / h;
			double dy = deltay*(i - h + .5) / h;

			vec ray_origin = sc.lookAt + (xdir * dx) + (ydir * dy);
			vec ray_direction = normalize(ray_origin - sc.lookFrom);

			vec color = { 0.0,0.0,0.0 };

			for (int k = 0; k < num_rays; k++) {
				color = color + rayTrace(ray_origin, jitter(ray_direction, jit), sc, 0, box);
			}

			color = color / num_rays;

			//Save the value to the picture
			int pixel = 3*res*i + 3*j;
			picture[pixel+0] = color.x;
			picture[pixel+1] = color.y;
			picture[pixel+2] = color.z;
		}
	}

	// Output the file
	saveImage(picture, res);
	delete picture;

	int wait;
	std::cin >> wait;

    return 0;
}
