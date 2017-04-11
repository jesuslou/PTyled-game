#include <application/CPTyledGameApplication.h>
#include <application/SApplicationWindowParameters.h>

CPTyledGameApplication application; // This class is your starting point

int main(int argc, char** argv)
{
	SApplicationWindowParameters applicationWindowParameters(800, 600, "PTyledGame");
	application.Init(applicationWindowParameters);
	application.Update();
	application.Destroy();
}
