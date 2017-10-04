#include <application/CPTyledGameApplication.h>
#include <entities/CEntityManager.h>
#include <entities/components/CComponentFactoryManager.h>

#include <components/SPositionComponent.h>
#include <components/SRotationComponent.h>

#include <components/SPTyledFooComponent.h>

CPTyledGameApplication::CPTyledGameApplication()
{
}

bool CPTyledGameApplication::InitProject(CGameSystems& gameSystems)
{
	CEntity e = CSystems::GetSystem<CEntityManager>()->CreateNewEntity();
	CSystems::GetSystem<CComponentFactoryManager>()->AddComponentByStr("position", e);
	CSystems::GetSystem<CComponentFactoryManager>()->AddComponentByStr("rotation", e);
	CSystems::GetSystem<CComponentFactoryManager>()->AddComponentByStr("foo", e);

	SPositionComponent* p1 = e.component<SPositionComponent>().get();
	SRotationComponent* p2 = e.component<SRotationComponent>().get();
	SPTyledFooComponent* p3 = e.component<SPTyledFooComponent>().get();

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
	REGISTER_COMPONENT_FACTORY("foo", SPTyledFooComponent);
}
