#pragma once

#include <application/CApplication.h>

class CPTyledGameApplication : public CApplication
{
public:
	CPTyledGameApplication();

protected:
	bool InitProject(CGameSystems& gameSystems) override;
	void UpdateProject(float dt) override;
	void DestroyProject() override;
	void RegisterComponentsProject() override;
};
