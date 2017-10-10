#include <application/CPTyledGameApplication.h>
#include <entity/CEntityManager.h>
#include <handle/CHandle.h>

CPTyledGameApplication::CPTyledGameApplication()
{
}

bool CPTyledGameApplication::InitProject(CGameSystems& gameSystems)
{
	CEntity *e = CSystems::GetSystem<CEntityManager>()->CreateEntity();
	CHandle h0 = CSystems::GetSystem<CEntityManager>()->CreateEntity();
	CHandle h1 = CSystems::GetSystem<CEntityManager>()->CreateEntity();

	CHandle h = e;

	if (h0)
	{
		printf("h0");
	}

	if (h1)
	{
		printf("h0");
	}

	CEntity* e2 = h;
	CEntity* e3 = h1;

	CSystems::GetSystem<CEntityManager>()->DestroyEntity(e);
	if (h)
	{
		printf("h0");
	}
	e = CSystems::GetSystem<CEntityManager>()->CreateEntity();


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

void CPTyledGameApplication::RegisterComponentsProject()
{
}
