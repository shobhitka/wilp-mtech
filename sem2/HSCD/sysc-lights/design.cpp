#include "systemc.h"

using namespace std;

typedef enum {
	STATE_0,
	STATE_1,
	STATE_2,
	STATE_3,
	STATE_MAX,
} house_state;

typedef enum {
	SIGNAL_P1,
	SIGNAL_P2,
	SIGNAL_MAX
} house_events;

typedef struct {
	int l1;
	int l2;
	int l3;
} light_state;

static light_state lights[STATE_MAX] = {
	{ 0, 0, 0 },
	{ 1, 0, 0 },
	{ 0, 1, 0 },
	{ 0, 0, 1 },
};

static int machine[STATE_MAX][SIGNAL_MAX] = {
	{ STATE_1, STATE_1 },
	{ STATE_2, STATE_3 },
	{ STATE_0, STATE_0 },
	{ STATE_0, STATE_0 }
};

SC_MODULE(my_house) {

	sc_in_clk clock;
	sc_in<bool> switch_p1;
	sc_in<bool> switch_p2;

	sc_out<bool> light_l1;
	sc_out<bool> light_l2;
	sc_out<bool> light_l3;

	int signal_p1, signal_p2;
	int curr_signal, curr_state;

	void control_lights() {

		if (switch_p1.read() == 1) {
			signal_p1 = 1;
		} else if (signal_p1 == 1) {
			// was pressed and released
			curr_signal = SIGNAL_P1;
		} else if (switch_p2.read() == 1) {
			signal_p2 = 1;
		} else if (signal_p2 == 1) {
			// was pressed and released
			curr_signal = SIGNAL_P2;
		} else {
			return;
		}

		signal_p1 = 0;
		signal_p2 = 0;

		curr_state = machine[curr_state][curr_signal];
		light_state lt_state = lights[curr_state];
		light_l1.write(lt_state.l1);
		light_l1.write(lt_state.l2);
		light_l1.write(lt_state.l3);

		//cout << "L1: " << lt_state.l1 ? "ON" : "OFF" << ", L2: " << lt_state.l2 ? "ON" : "OFF" << ", L3: " << lt_state.l3 ? "ON" : "OFF" << endl;
		cout << "L1: " << lt_state.l1 << ", L2: " << lt_state.l2 << ", L3: " << lt_state.l3 << endl;

		curr_signal = -1;
	}

	SC_CTOR(my_house) {
		cout << "Initializing the house" << endl;
		curr_state = STATE_0;
		signal_p1 = 0;
		signal_p2 = 0;
		curr_signal = -1;

		SC_METHOD(control_lights);
		sensitive << clock.pos();
	}
};
