#include "systemc.h"
#include "design.cpp"

using namespace std;

#define RUN_CLOCK(duration) \
		for (i = 0; i < duration; i++) { \
				clock = 0; \
				sc_start(1, SC_NS); \
				clock = 1; \
				sc_start(1, SC_NS);\
		} \

int sc_main (int argc, char* argv[]) 
{
		sc_signal<bool> clock;
		sc_signal<bool> switch_p1;
		sc_signal<bool> switch_p2;

		sc_signal<bool> light_l1;
		sc_signal<bool> light_l2;
		sc_signal<bool> light_l3;

		int i = 0;
		// Connect the DUT
		my_house house("house");
		//house.clock(clock);
		house.switch_p1(switch_p1);
		house.switch_p2(switch_p1);
		house.light_l1(light_l1);
		house.light_l2(light_l2);
		house.light_l3(light_l3);

		cout << "@" << sc_time_stamp() <<" Starting Simulation" << endl;
		sc_start(1, SC_NS);
		switch_p1 = 0;
		switch_p2 = 0;

		RUN_CLOCK(5);
		cout << "@" << sc_time_stamp() <<" Press Switch: P1" << endl;
		switch_p1 = 1;    // Press P1
		RUN_CLOCK(5);
		cout << "@" << sc_time_stamp() <<" Release Switch: P1" << endl;
		switch_p1 = 0;    // Release P1

		RUN_CLOCK(10);
		cout << "@" << sc_time_stamp() <<" Press Switch: P1" << endl;
		switch_p1 = 1;    // Press P1
		RUN_CLOCK(5);
		cout << "@" << sc_time_stamp() <<" Release Switch: P1" << endl;
		switch_p1 = 0;    // Release P1

		RUN_CLOCK(10);
		cout << "@" << sc_time_stamp() <<" Press Switch: P2" << endl;
		switch_p2 = 1;    // Press P1
		RUN_CLOCK(5);
		cout << "@" << sc_time_stamp() <<" Release Switch: P2" << endl;
		switch_p2 = 0;    // Release P2

		RUN_CLOCK(5);
		cout << "@" << sc_time_stamp() <<" Press Switch: P2" << endl;
		switch_p2 = 1;    // Press P2
		RUN_CLOCK(5);
		cout << "@" << sc_time_stamp() <<" Release Switch: P2" << endl;
		switch_p2 = 0;    // Release P2

		RUN_CLOCK(10);
		cout << "@" << sc_time_stamp() <<" Press Switch: P2" << endl;
		switch_p2 = 1;    // Press P2
		RUN_CLOCK(5);
		cout << "@" << sc_time_stamp() <<" Release Switch: P2" << endl;
		switch_p2 = 0;    // Release P2

		RUN_CLOCK(10);
		cout << "@" << sc_time_stamp() <<" Press Switch: P1" << endl;
		switch_p1 = 1;    // Press P1
		RUN_CLOCK(5);
		cout << "@" << sc_time_stamp() <<" Release Switch: P1" << endl;
		switch_p1 = 0;    // Release P1

		RUN_CLOCK(20);

		sc_start(-1);
		return 0;// Terminate simulation
}

