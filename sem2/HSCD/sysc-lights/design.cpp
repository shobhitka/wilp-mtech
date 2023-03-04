#include "systemc.h"

using namespace std;

// System State definitions
typedef enum {
	STATE_0,
	STATE_1,
	STATE_2,
	STATE_3,
	STATE_MAX,
} house_state;

// Possible signals - switches
typedef enum {
	SIGNAL_P1,
	SIGNAL_P2,
	SIGNAL_MAX
} house_events;

// Initialize static light states based on the system states
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

// Define the state transition for every signal
static int machine[STATE_MAX][SIGNAL_MAX] = {
	{ STATE_1, STATE_1 },
	{ STATE_2, STATE_3 },
	{ STATE_0, STATE_0 },
	{ STATE_0, STATE_0 }
};

SC_MODULE(my_house) {

	// define the module input, output and clock signals
	sc_in_clk clock;
	sc_in<bool> switch_p1;
	sc_in<bool> switch_p2;

	sc_out<bool> light_l1;
	sc_out<bool> light_l2;
	sc_out<bool> light_l3;

	int curr_signal, curr_state;
	int change_state, pressed;

	void control_lights() {
		// when any of the signal is asserted, read state of each signal to
		// know which one is asserted
		int sw1 = switch_p1.read();
		int sw2 = switch_p2.read();

		if (sw1 == 1 && pressed == 0) {
			// only if sw1 is asserted and it was not just help 
			// high but pressed first time this will also ensure
			// if this was pressed first in case of simultaneous
			// switch presses, sw1 will be tracked for state change
			curr_signal = SIGNAL_P1;
			pressed = 1;
		} else if (sw2 == 1 && pressed == 0) {
			// only if sw2 is asserted and it was not just help high
			// but pressed first time this will also ensure if this
			// was pressed first in case of simultaneous switch presses,
			// sw2 will be tracked for state change
			curr_signal = SIGNAL_P2;
			pressed = 1;
		} else if (sw1 == 0 && curr_signal == SIGNAL_P1) {
			// track release of sw1 as state change trigger if it was
			// already asserted high
			change_state = 1;
		} else if (sw2 == 0 && curr_signal == SIGNAL_P2) {
			// track release of sw2 as state change trigger if it was
			// already asserted high
			change_state = 1;
		} else {
			return;
		}

		if (!change_state) {
			// No state change recorded yet
			return;
		}

		// Based on current state and final signal determined
		// for state change go to next state as per state machine
		curr_state = machine[curr_state][curr_signal];

		// based on the current state, get what should be the
		// light status and assert the output signal for the 
		// lights accordingly
		light_state lt_state = lights[curr_state];
		light_l1.write(lt_state.l1);
		light_l2.write(lt_state.l2);
		light_l3.write(lt_state.l3);

		cout << "@" << sc_time_stamp() << " L1: " << lt_state.l1 << ", L2: " << lt_state.l2 << ", L3: " << lt_state.l3 << "\n" << endl;

		// reset the tracking variables
		curr_signal = SIGNAL_MAX;
		change_state = 0;
		pressed = 0;
	}

	SC_CTOR(my_house) {
		cout << "Initializing the house" << endl;
		curr_state = STATE_0;
		curr_signal = SIGNAL_MAX;
		pressed = 0;
		change_state = 0;

		// main method to handle signals
		SC_METHOD(control_lights);

		// set sensitivity to both the input signals
		sensitive << switch_p1;
		sensitive << switch_p2;
	}
};
