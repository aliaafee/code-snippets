 /*
    Calculating pi by Monte Carlo Method
    ------------------------------------

    Assumes a 1x1 square with inscribed 1/4 circle of radius 1.
    The ratio of the area of the circle to the area of the square
    if pi/4.

    By Monte Carlo method we randomly pick points in the square
    and calculate the ratio of the points that lie in the circle
    to those the total number of points.

    The ratio divided by 4 gives the value of pi.
*/


#include <iostream>
#include <math.h>

using namespace std;


int main()
{
    double x, y, d2, in, out, pi;

    double iterations = 1000000;

    for (int i=0; i < iterations; i++)
    {
        x = double((double)rand()/RAND_MAX);
        y = double((double)rand()/RAND_MAX);

        d2 = x*x + y*y;

        if ( d2 <= 1 )
            in += 1.0;
    }

    pi = in/iterations * 4.0;

    cout << "pi after " << iterations << " iterations is " << pi << endl;

    return 0;
}
