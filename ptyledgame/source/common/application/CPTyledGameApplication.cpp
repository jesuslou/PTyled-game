#include <application/CPTyledGameApplication.h>
#include <entity/CEntityManager.h>
#include <handle/CHandle.h>
#include <component/CComponent.h>
#include <component/CComponentFactory.h>
#include <component/CComponentFactoryManager.h>

#include <components/CCompLocation.h>
#include <components/CCompCamera.h>

class CCompFoo : public CComponent
{
public:
	CCompFoo() : m_p(10) {}
	int m_p;
};

CPTyledGameApplication::CPTyledGameApplication()
{
}

bool CPTyledGameApplication::InitProject(CGameSystems& gameSystems)
{
	CComponentFactoryManager* cfm = CSystems::GetSystem<CComponentFactoryManager>();

	ADD_COMPONENT_FACTORY("loc", CCompLocation, 2);
	ADD_COMPONENT_FACTORY("cam", CCompCamera, 2);

	CCompLocation* compLoc = static_cast<CCompLocation*>(cfm->CreateComponent<CCompLocation>());
	CCompCamera* compCam = static_cast<CCompCamera*>(cfm->CreateComponent<CCompCamera>());

	CHandle h = cfm->CreateComponent<CCompCamera>();

	CHandle compCamHandle;
	compCamHandle.m_elementType = CHandle::EElementType::Component;
	compCamHandle.m_componentIdx = 1;
	compCamHandle.m_elementPosition = 0;
	compCamHandle.m_version = 0;

	CComponent* compCam33 = h;
	CComponent* compCam2 = compCamHandle;

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
