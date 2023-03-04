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

	sc_in<bool> switch_p1;
	sc_in<bool> switch_p2;

	sc_out<bool> light_l1;
	sc_out<bool> light_l2;
	sc_out<bool> light_l3;

	int curr_signal, curr_state;
	int change_state;

	void control_lights() {
		int sw1 = switch_p1.read();
		int sw2 = switch_p2.read();

		if (sw1 == 1) {
			curr_signal = SIGNAL_P1;
		} else if (sw2 == 1) {
			curr_signal = SIGNAL_P2;
		} else if (sw1 == 0 && curr_signal == SIGNAL_P1) {
			change_state = 1;
		} else if (sw2 == 0 && curr_signal == SIGNAL_P2) {
			change_state = 1;
		} else {
			return;
		}

		if (!change_state) {
			return;
		}

		curr_state = machine[curr_state][curr_signal];
		light_state lt_state = lights[curr_state];
		light_l1.write(lt_state.l1);
		light_l1.write(lt_state.l2);
		light_l1.write(lt_state.l3);

		cout << "@" << sc_time_stamp() << " L1: " << lt_state.l1 << ", L2: " << lt_state.l2 << ", L3: " << lt_state.l3 << "\n" << endl;
		curr_signal = SIGNAL_MAX;
		change_state = 0;
	}

	SC_CTOR(my_house) {
		cout << "Initializing the house" << endl;
		curr_state = STATE_0;
		curr_signal = SIGNAL_MAX;

		SC_METHOD(control_lights);
		sensitive << switch_p1;
		sensitive << switch_p2;
	}
};
