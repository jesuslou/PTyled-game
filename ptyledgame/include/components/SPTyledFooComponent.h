#pragma once

#include <entities/components/IComponent.h>

struct SPTyledFooComponent : public IComponent
{
	SPTyledFooComponent() : m_x(0.f), m_y(0.f), m_z(0.f) {}

	void ParseAtts() override
	{
		m_x = 1.f;
		m_y = 2.f;
		m_z = -1.f;
	}

	float m_x;
	float m_y;
	float m_z;
};
