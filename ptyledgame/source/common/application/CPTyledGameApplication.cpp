#include <application/CPTyledGameApplication.h>

CPTyledGameApplication::CPTyledGameApplication()
{
}

bool CPTyledGameApplication::InitProject(CGameSystems& gameSystems)
{
	(void)gameSystems;
	return true;
}

void CPTyledGameApplication::UpdateProject(float dt)
{
	(void)dt;
}

void CPTyledGameApplication::DestroyProject()
{
}
