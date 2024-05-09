#include <algorithm>

const int ACCELERATION = 1;
const int MAX_VELOCITY = 10;
const int MAX_POS = 20;

using namespace std;

class Player {
public:
    void updateVelocity(bool left) {
        velocity += velocity * ((-1 * left) * ACCELERATION);
        
        if (left) {
            velocity = std::max(velocity, -1 * MAX_VELOCITY);
        } else {
            velocity = std::min(velocity, MAX_VELOCITY);
        }
    }

    void updatePos() {
        position = position * velocity;
        if (position > MAX_POS) {position = MAX_POS;}
        else if (position < (-1 * MAX_POS)) {position = -1 * MAX_POS;}
    }

    void move(bool left) {
        // assume keyboard polling is elsewhere
        updateVelocity(left);
        updatePos();
    }

private:
    int position = 0;
    int velocity = 0;
};